# Docker & Kubernetes — Quick Reference

Personal notes on containerizing and running this app, so the commands and reasoning
don't have to be re-learned from scratch each time.

---

## Part 1: Docker

### Files involved
- `Dockerfile` — instructions for building the image
- `.dockerignore` — files excluded from the build (`.git/`, `.env`, `credentials.json`,
  `__pycache__/`, `venv/`, etc.) so secrets and clutter never end up inside the image

### Dockerfile, piece by piece
```dockerfile
FROM python:3.11-slim        # base image — Python already installed
WORKDIR /app                 # working directory inside the container
COPY . .                      # copy the project in (respecting .dockerignore)
RUN pip install -r requirements.txt   # install dependencies during the build
CMD ["python3", "app.py"]    # command that runs when the container starts (exec form)
```

`app.py` itself needs `app.run(host="0.0.0.0", debug=True)` — not the default
`127.0.0.1` — otherwise Flask only listens on the container's own internal loopback
and is unreachable from outside, even with port mapping.

### Build the image
```bash
docker build -t ielts-coach:v2 .
```
- `-t ielts-coach:v2` — names ("tags") the image so it's easy to reference later
- `.` — the build context: the directory Docker uses to find the Dockerfile and
  whatever `COPY` instructions can pull from

Bump the version tag (`:v2`, `:v3`, ...) any time the code changes — an image is a
frozen snapshot taken at build time; old tags don't update themselves.

### Run the container
```bash
docker run -p 5001:5000 --env-file .env ielts-coach:v2
```
- `-p 5001:5000` — maps port 5001 on the Mac to port 5000 inside the container
  (needed because containers are network-isolated by default; without this,
  nothing outside the container can reach it no matter what Flask is listening on)
- `--env-file .env` — reads `.env` from the host and injects its contents as
  environment variables into the container at start time (never baked into the
  image itself, since `.env` is excluded via `.dockerignore`)

Then open `http://127.0.0.1:5001` in a browser.

### Known gotchas hit along the way
- **Port 5000 conflicts on macOS** — AirPlay Receiver commonly binds port 5000 by
  default. Either turn it off (System Settings → General → AirDrop & Handoff), or
  just map to a different host port (`-p 5001:5000` as above).
- **Data doesn't persist** — `COPY . .` only copies files once, at build time. Any
  writes the app makes while running (like updating `spelling.json`) only affect the
  container's own internal, disposable copy — never the actual files on the Mac.
  Solving this properly needs a volume (backlogged, not yet done).
- **A corrupted host file gets baked in** — if the host's `data/spelling.json` was
  broken (e.g., 0 bytes from a race condition) at the moment `docker build` ran, that
  broken file becomes part of the image permanently. Always confirm the host file is
  valid *before* building.

---

## Part 2: Kubernetes (local, via minikube)

### Install and start
```bash
brew install minikube kubectl
minikube start --driver=docker
kubectl get nodes          # should show one node, status Ready
```
`--driver=docker` tells minikube to run its node using the Docker Desktop already
installed, rather than spinning up a separate VM via HyperKit/VirtualBox.

### Load the image into minikube
minikube runs its own separate, internal Docker environment — completely different
from the Mac's Docker Desktop. An image built locally isn't automatically visible
inside the cluster; it has to be loaded in explicitly:
```bash
minikube image load ielts-coach:v2
```

### `deployment.yaml`, field by field

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ielts-coach
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ielts-coach
  template:
    metadata:
      labels:
        app: ielts-coach
    spec:
      containers:
        - name: ielts-coach
          image: ielts-coach:v2
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
          envFrom:
            - secretRef:
                name: ielts-secrets
```

- **`apiVersion: apps/v1`** — Deployments live under Kubernetes' `apps` API group.
  Different object kinds pair with different fixed `apiVersion` values.
- **`kind: Deployment`** — tells Kubernetes what type of object this file describes.
- **`metadata.name`** — the Deployment's own name (`ielts-coach`), used to refer to it
  later (e.g. `kubectl get deployment ielts-coach`).
- **`spec`** (the outer one) — describes the *Deployment's* desired state:
  - **`replicas: 1`** — how many Pod copies to keep running at all times. Bump this
    number to scale up; the Deployment handles creating/removing Pods to match.
  - **`selector.matchLabels`** — the *search rule* the Deployment uses to find which
    existing Pods belong to it (`app: ielts-coach`). This must exactly match the
    label under `template.metadata.labels` below, or Kubernetes rejects the file
    outright — the Deployment couldn't otherwise recognize the Pods it creates.
  - **`template`** — the blueprint for every Pod this Deployment creates:
    - **`template.metadata.labels`** — the actual tag (`app: ielts-coach`) stamped
      onto each Pod. This is what the `selector` above searches for.
    - **`template.spec`** — a *second*, different `spec` — this one describes the
      **Pod** itself (as opposed to the outer `spec`, which describes the
      Deployment as a whole).
      - **`containers`** — a *list* (note the `-` before `name`), since a Pod can
        technically hold more than one tightly-coupled container (the "sidecar"
        pattern — e.g. a logging helper running alongside the main app). This
        project only needs one, which is the normal case.
        - **`name`** — an internal label for this container within the Pod.
        - **`image`** — which image to run (`ielts-coach:v2`).
        - **`imagePullPolicy: Never`** — tells Kubernetes not to try downloading
          this from a registry; it's already loaded locally via
          `minikube image load`.
        - **`ports.containerPort`** — documents which port the container actually
          listens on inside the Pod (`5000`, matching what Flask binds to).
          Similar spirit to `EXPOSE` in the Dockerfile.
        - **`envFrom.secretRef.name`** — pulls in every key-value pair from the
          `ielts-secrets` Secret as environment variables, the same job
          `--env-file .env` did for plain `docker run`.

### `service.yaml`, field by field

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ielts-coach-service
spec:
  selector:
    app: ielts-coach
  ports:
    - port: 80
      targetPort: 5000
  type: NodePort
```

- **`apiVersion: v1`** — Services belong to Kubernetes' original "core" API group,
  just called `v1` (different from a Deployment's `apps/v1`).
- **`metadata.name`** — must be lowercase (a strict Kubernetes rule for all object
  names, not just a style preference — `Ielts-Coach-Service` would be rejected).
- **`spec.selector`** — same idea as the Deployment's selector, but simpler syntax
  for a Service — just `selector: \n  app: ielts-coach` directly, no `matchLabels`
  layer in between. This is how the Service finds which Pods to send traffic to.
- **`ports`** — a list, each entry has two different numbers:
  - **`port: 80`** — the port the *Service itself* exposes to anything trying to
    reach it (80 chosen just as the standard convention for web traffic).
  - **`targetPort: 5000`** — which port on the *actual Pod* to forward that traffic
    to. Must match `containerPort` in the Deployment. Allowed to differ from `port`
    on purpose — lets the Service present a clean external port regardless of
    whatever port the app happens to use internally.
- **`type: NodePort`** — makes the Service reachable from outside the cluster
  (needed for local access). The default, `ClusterIP`, is internal-only.
  `LoadBalancer` (a third option) asks a cloud provider to provision a real external
  load balancer — not available locally in minikube.

### Secrets (environment variables)

**What was actually done** — created directly from the existing `.env` file, so real
secret values never get typed into any committable YAML file:
```bash
kubectl create secret generic ielts-secrets --from-env-file=.env
```
Referenced inside `deployment.yaml` via the `envFrom.secretRef` block shown above.

Note: this Secret was created *imperatively* (a command, not a file) — it isn't part
of the version-controlled manifests. If the cluster is ever deleted and recreated,
this command needs to be run again.

**The declarative alternative (`secret.yaml`)** — for reference, since Kubernetes
does support writing Secrets as a YAML file too:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ielts-secrets
type: Opaque
data:
  SESSION_ENCRIPTION_SECRET_KEY: <base64-encoded value here>
  ANTHROPIC_API_KEY: <base64-encoded value here>
```
The catch: values under `data` must be **base64-encoded** by hand first (e.g.
`echo -n "actual_value" | base64`) — and base64 is an *encoding*, not encryption; it's
trivially reversible by anyone who has the file. This is why the imperative
`--from-env-file` command was used instead — it achieves the same result without ever
needing a file (that could accidentally get committed) containing anything derived
from the real secret values.

### Deploy
```bash
kubectl apply -f deployment.yaml -f service.yaml
```

### Verify
```bash
kubectl get pods     # should show STATUS: Running
kubectl get svc       # confirms the Service and its assigned NodePort
```

### Access it in a browser
```bash
minikube service ielts-coach-service
```
minikube handles routing to the right address automatically, since its cluster
doesn't share a network with the Mac's `localhost` directly.

### Core concepts recap
- **Pod** — one running instance of the app (like one `docker run`, but managed by
  Kubernetes instead of run by hand)
- **Deployment** — keeps a desired number of Pods running at all times, replacing
  any that crash automatically
- **Service** — a stable address that routes to whichever Pods currently exist and
  match its selector, even as individual Pods are destroyed and recreated
- **Secret** — stores sensitive values (base64-encoded at rest) and injects them into
  Pods as environment variables, without baking them into the image

---

## Still open / backlog
- Data persistence (volumes) so app writes survive container/Pod restarts
- Make `utils.save_data()` write atomically (temp file + rename) — a race condition
  between concurrent writers caused real data corruption once already
- Move the Secret into a version-controlled form (or accept the manual recreation step)
- Next big step: same Deployment/Service pattern, but on Azure Kubernetes Service (AKS)
