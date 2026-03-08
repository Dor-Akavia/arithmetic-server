# Arithmetic Calculator — 

DevOps pipeline: Python application → Docker → Terraform/AWS → Jenkins CI/CD.

---

## Project Structure

```
pantera/
├── client/
│   └── client.py          # Process A — interactive CLI client
├── server/
│   ├── server.py          # Process B — TCP arithmetic server
│   ├── operations.py      # OOP operation classes (Addition, Subtraction, …)
│   └── requirements.txt   # No third-party deps; file exists for Docker caching
├── terraform/
│   ├── main.tf            # EC2 instance + security group
│   ├── variables.tf       # Configurable inputs
│   └── outputs.tf         # Printed values after apply
├── Dockerfile             # Multi-stage build for the server image
├── .dockerignore          # Files excluded from the Docker build context
├── docker-compose.yml     # Local deployment (server + client)
├── Jenkinsfile            # CI/CD pipeline (build → push to Docker Hub)
└── README.md              # This file
```

---

### Run Locally (no Docker)

**Terminal 1 — start the server:**
```bash
cd server
python server.py
```

**Terminal 2 — run the client:**
```bash
cd client
python client.py
```

> Note: when running locally without Docker, open `client/client.py` and change
> `SERVER_HOST = "server"` to `SERVER_HOST = "localhost"`.

---

## Phase 2 — Docker

### Build the image

```bash
docker build -t arithmetic-server:latest .
```

### How the Dockerfile is optimised

1. **Multi-stage build** — Stage 1 (`builder`) installs dependencies.
   Stage 2 (`runtime`) copies only the installed packages and source code.
   Build tools and pip cache never end up in the final image.

2. **Layer caching** — `requirements.txt` is copied and `pip install` is run
   *before* the source code is copied. Rebuilding after a code change reuses
   the cached pip layer and skips re-downloading packages.

3. **Non-root user** — the container runs as `appuser`, not root.

### Push to Docker Hub

```bash
docker tag arithmetic-server:latest <your-username>/arithmetic-server:latest
docker push <your-username>/arithmetic-server:latest
```

---

## Phase 3 — Infrastructure as Code (Terraform + AWS)

### Prerequisites

- [Terraform ≥ 1.3](https://www.terraform.io/downloads)
- AWS CLI configured (`aws configure`) or environment variables set
- An existing EC2 key pair (create one in the AWS console)

### Deploy Jenkins on AWS

```bash
cd terraform

# Initialise providers
terraform init

# Preview what will be created
terraform plan -var="key_pair_name=<your-key-pair>"

# Apply (creates EC2 + security group)
terraform apply -var="key_pair_name=<your-key-pair>"
```

After `apply` completes, Terraform prints:
- `jenkins_url`  — open this in a browser to access Jenkins
- `ssh_command`  — use this to SSH into the server

### Unlock Jenkins (first boot)

```bash
# SSH in
ssh -i <your-key.pem> ubuntu@<public-ip>

# Retrieve the initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Paste the password into the Jenkins web UI to complete setup.

### Destroy infrastructure (avoid AWS charges)

```bash
terraform destroy -var="key_pair_name=<your-key-pair>"
```

---

## Phase 4 — Jenkins CI/CD Pipeline

The `Jenkinsfile` at the project root defines a declarative pipeline:

| Stage | What it does |
|-------|--------------|
| Checkout | Clones the repo; prints the commit SHA |
| Lint | Runs `python3 -m py_compile` — catches syntax errors cheaply |
| Build Docker Image | Runs `docker build`; tags with build number + commit SHA |
| Push to Docker Hub | Pushes both a versioned tag and `latest` |
| Cleanup (always) | Removes the local image to free disk space |

### Jenkins Setup

1. Install the **Docker Pipeline** plugin in Jenkins.
2. Add two credentials:
   - `DOCKERHUB_CREDENTIALS` — Username/Password (Docker Hub login)
   - `DOCKERHUB_USERNAME` — Secret text (your Docker Hub username)
3. Create a new Pipeline job pointing at your Git repository.
4. Jenkins will automatically pick up the `Jenkinsfile`.

---

## Phase 5 — Local Deployment with Docker Compose

### Start the server

```bash
docker compose up -d server
```

### Run the client interactively

```bash
docker compose run --rm client
```

You will be prompted for two numbers and an operation:

```
--- Arithmetic Calculator ---

Enter first number : 10
Enter second number: 3
Operation ['+', '-', '*', '/']: /

  Result: 10.0 / 3.0 = 3.3333333333333335

Calculate again? (y/n):
```

### Stop everything

```bash
docker compose down
```

---

## Deliverables Checklist

- [x] `client/client.py` — interactive client (Process A)
- [x] `server/server.py` — arithmetic server (Process B)
- [x] `server/operations.py` — OOP operation classes with ABC
- [x] `Dockerfile` — multi-stage, optimised build
- [x] `docker-compose.yml` — local deployment
- [x] `Jenkinsfile` — Groovy CI/CD pipeline with error handling
- [x] `terraform/` — AWS EC2 + Jenkins infrastructure as code
- [x] `README.md` — this documentation
