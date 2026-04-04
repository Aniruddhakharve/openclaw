<div align="center">

# 🦞 OpenClaw

### A Self-Healing Docker Container Monitoring Tool

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-Multi--Service-2496ED?style=for-the-badge&logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=githubactions)
![AWS EC2](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonaws)
![DockerHub](https://img.shields.io/badge/DockerHub-Registry-2496ED?style=for-the-badge&logo=docker)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=for-the-badge&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?style=for-the-badge&logo=grafana)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform)

</div>

---

## 📌 What is OpenClaw?

**OpenClaw** is a self-healing Docker container monitoring tool built with Python.
It watches your Docker containers 24/7 and automatically restarts them if they stop unexpectedly.

It also logs every event, sends real-time alerts to Slack or Telegram, visualizes metrics using **Prometheus and Grafana**, is secured with a full **DevSecOps CI/CD pipeline** powered by GitHub Actions, and provisions AWS infrastructure using **Terraform Modules**.

> Built as a hands-on DevOps learning project covering monitoring, automation, logging, alerting, metrics visualization, security pipelines, and Infrastructure as Code.

---

## 🎯 Project Goals

- ✅ Monitor Docker containers continuously
- ✅ Auto-restart stopped or crashed containers
- ✅ Log all events with timestamps
- ✅ Support multiple containers via a config file
- ✅ Send real-time alerts via Slack / Telegram
- ✅ Visualize container metrics using Prometheus and Grafana
- ✅ Secure automated CI/CD pipeline with DevSecOps best practices
- ✅ Provision AWS infrastructure using Terraform Modules (IaC)

---

## 🏗️ Architecture
```
Your Code (GitHub)
        |
        ▼
GitHub Actions Pipeline
  ├── Lint           (flake8)
  ├── SAST           (bandit)
  ├── Secrets Scan   (gitleaks)
  ├── Dependency     (pip-audit)
  ├── Dockerfile     (hadolint)
  ├── Docker Build   (build & push to DockerHub)
  ├── Image Scan     (trivy)
  └── Deploy         (SSH to AWS EC2)
                |
                ▼
         AWS EC2 Server
         └── provisioned by Terraform Modules
               └── Docker Compose
                     ├── OpenClaw Container
                     │     ├── Watches Docker containers
                     │     ├── Auto-restarts crashed ones
                     │     ├── Writes logs
                     │     ├── Exposes metrics
                     │     └── Sends Slack / Telegram alerts
                     │
                     ├── Prometheus Container
                     │     └── Scrapes and stores metrics
                     │         from OpenClaw
                     │
                     └── Grafana Container
                           └── Visualizes metrics on
                               a live dashboard
```

---

## 🔁 CI/CD Pipeline Flow
```
Push to GitHub
      |
      ▼
pipeline.yml  ← Master Workflow
  │
  ├── calls lint.yml              ─┐
  ├── calls sast.yml               │
  ├── calls secrets-scan.yml       ├── Run in Parallel
  ├── calls dependency-scan.yml    │
  ├── calls dockerfile-lint.yml   ─┘
  │         │
  │         ▼ (all pass?)
  ├── calls docker-build.yml      ← Build & Push to DockerHub
  │         │
  │         ▼ (build passes?)
  ├── calls image-scan.yml        ← Trivy scans the Docker image
  │         │
  │         ▼ (scan passes?)
  └── calls deploy.yml            ← SSH deploy to AWS EC2
```

---

## 🐳 Docker Compose Services
```
docker-compose.yml
├── openclaw       ← Core monitoring + self-healing tool
├── prometheus     ← Scrapes and stores metrics from OpenClaw
└── grafana        ← Visualizes metrics on a live dashboard
```

| Service | Purpose | Port |
|---|---|---|
| `openclaw` | Monitors containers, auto-restarts, sends alerts | - |
| `prometheus` | Collects and stores OpenClaw metrics | 9090 |
| `grafana` | Live dashboard for container health metrics | 3000 |

---

## 🏗️ Terraform Modules Structure
```
terraform/
├── main.tf                    ← calls all modules
├── variables.tf               ← global input variables
├── outputs.tf                 ← outputs like EC2 public IP
├── terraform.tfvars           ← actual variable values
└── modules/
      ├── ec2/                 ← EC2 instance module
      │     ├── main.tf
      │     ├── variables.tf
      │     └── outputs.tf
      │
      ├── security_group/      ← firewall rules module
      │     ├── main.tf
      │     ├── variables.tf
      │     └── outputs.tf
      │
      └── key_pair/            ← SSH key pair module
            ├── main.tf
            ├── variables.tf
            └── outputs.tf
```

---

## 📁 Project Structure
```
openclaw/
├── README.md                          ← Project documentation
├── monitor.py                         ← Core monitoring script
├── alerts.py                          ← Slack / Telegram alerts
├── requirements.txt                   ← Python dependencies
├── Dockerfile                         ← Single stage Dockerfile
├── docker-compose.yml                 ← OpenClaw + Prometheus + Grafana
├── config.yaml                        ← Containers to monitor (Phase 4)
├── .gitignore                         ← Git ignore rules
├── logs/                              ← Container event logs
├── terraform/                         ← Infrastructure as Code (Phase 7)
│     ├── main.tf
│     ├── variables.tf
│     ├── outputs.tf
│     ├── terraform.tfvars
│     └── modules/
│           ├── ec2/
│           ├── security_group/
│           └── key_pair/
└── .github/
    └── workflows/
        ├── pipeline.yml               ← Master pipeline (calls all workflows)
        ├── lint.yml                   ← Python code linting (flake8)
        ├── sast.yml                   ← Static security analysis (bandit)
        ├── secrets-scan.yml           ← Secret/key leak detection (gitleaks)
        ├── dependency-scan.yml        ← Package vulnerability scan (pip-audit)
        ├── dockerfile-lint.yml        ← Dockerfile validation (hadolint)
        ├── docker-build.yml           ← Docker build & push to DockerHub
        ├── image-scan.yml             ← Container image scan (trivy)
        └── deploy.yml                 ← Deploy to AWS EC2 via SSH
```

---

## 🚀 Project Phases

### 🔵 Phase 1 — Container Monitoring
- Use Docker CLI (`docker ps`) to check if containers are running
- Poll containers on a set interval (every N seconds)
- Print status to console — running ✅ or stopped ❌
- **Files:** `monitor.py`, `requirements.txt`, `Dockerfile`, `.gitignore`

---

### 🔵 Phase 2 — Auto Restart
- Detect stopped containers from Phase 1
- Automatically run `docker start <container_name>`
- Verify the container came back up successfully
- Flag containers that fail to restart
- **Files:** Updates to `monitor.py`

---

### 🔵 Phase 3 — Logging System
- Log every event (started, stopped, restarted, failed) to a file
- Include timestamps on every log entry
- Store logs inside the container, exportable via Docker volumes
- **Files:** Updates to `monitor.py`, new `logs/` directory

---

### 🔵 Phase 4 — Config File
- Move all hardcoded values into `config.yaml`
- Define which containers to monitor
- Set check intervals, restart limits, log paths
- No code changes needed — just edit the config
- **Files:** `config.yaml`, updates to `monitor.py`

---

### 🔵 Phase 5 — Alerts
- Send real-time notifications when containers crash or fail to restart
- Support Slack webhooks and Telegram bot
- Alert message includes container name, event type, and timestamp
- **Files:** Updates to `monitor.py`, new `alerts.py`

---

### 🔵 Phase 6 — DevSecOps CI/CD Pipeline
- Full GitHub Actions pipeline with a master workflow calling reusable workflows
- Each security/lint/build/deploy stage is in its own workflow file
- Docker Compose deploys all 3 services (OpenClaw + Prometheus + Grafana) to EC2

| Stage | Tool | Purpose |
|---|---|---|
| Code Lint | `flake8` | Python code style check |
| SAST | `bandit` | Python security vulnerability scan |
| Secrets Scan | `gitleaks` | Detect leaked API keys or passwords |
| Dependency Scan | `pip-audit` | Check packages for known CVEs |
| Dockerfile Lint | `hadolint` | Validate Dockerfile best practices |
| Docker Build | `docker` | Build and push image to DockerHub |
| Image Scan | `trivy` | Scan Docker image for vulnerabilities |
| Deploy | SSH | Deploy to AWS EC2 automatically |

---

### 🔵 Phase 7 — Terraform Modules (IaC)
- Provision entire AWS infrastructure using Terraform Modules
- Each infrastructure component is a separate reusable module
- Root `main.tf` calls all modules and passes outputs between them

| Module | What it Creates |
|---|---|
| `ec2` | t2.micro EC2 instance on AWS free tier |
| `security_group` | Firewall rules for ports 22, 3000, 9090 |
| `key_pair` | SSH key pair for EC2 access |

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.11 |
| Containerization | Docker & Docker Desktop |
| Container Orchestration | Docker Compose |
| Metrics Collection | Prometheus |
| Metrics Visualization | Grafana |
| Cloud | AWS EC2 |
| Image Registry | DockerHub |
| CI/CD | GitHub Actions |
| Alerting | Slack / Telegram |
| Infrastructure as Code | Terraform Modules |
| Code Lint | flake8 |
| SAST | bandit |
| Secrets Scan | gitleaks |
| Dependency Scan | pip-audit |
| Dockerfile Lint | hadolint |
| Image Scan | trivy |

---

## 👤 Author

**Aniruddha Kharve**
DevOps Engineer in Progress 🚀
GitHub: [@Aniruddhakharve](https://github.com/Aniruddhakharve)

---

<div align="center">
Built with 🦞 and a lot of DevOps love
</div>
