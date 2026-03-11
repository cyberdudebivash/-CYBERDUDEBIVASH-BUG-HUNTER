# 🛡️ CyberDudeBivash Sentinel APEX
### Enterprise-Grade Asynchronous Reconnaissance & Threat Intelligence Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Security](https://img.shields.io/badge/Security-Hardened-green.svg)](#)

**Sentinel APEX** is the flagship reconnaissance engine of the **CyberDudeBivash Ecosystem**. Designed for elite cybersecurity researchers and enterprises, it automates large-scale asset discovery, technology fingerprinting, and continuous attack surface monitoring using a high-concurrency asynchronous architecture.

---

## 🚀 Key Features

* **Swarm DNS Engine:** High-speed asynchronous subdomain brute-forcing.
* **Passive CT Scraper:** Stealthy asset discovery via Certificate Transparency logs.
* **Web Tech Fingerprinter:** Real-time identification of Nginx, Apache, WordPress, and more.
* **Persistent Intelligence:** Full SQLModel/PostgreSQL integration for historical asset tracking.
* **Tiered SaaS API:** Built-in rate limiting and API key management for Pro/Enterprise levels.
* **Production Ready:** Fully containerized with Docker Compose and Nginx SSL.

---

## 🛠️ Architecture

Sentinel APEX utilizes a modern, non-blocking stack to handle thousands of concurrent scans:



- **Frontend/API:** FastAPI (Python 3.12)
- **Database:** PostgreSQL (Relational persistence)
- **Cache/Shield:** Redis (Rate limiting)
- **Gateway:** Nginx Proxy Manager (SSL/TLS Termination)

---

## 🚥 Quick Start

### Prerequisites
- Docker & Docker Compose
- A registered domain (for SSL/Proxy setup)

### Deployment
1. Clone the repository:
   ```bash
   git clone [https://github.com/CyberDudeBivash/sentinel-apex.git](https://github.com/CyberDudeBivash/sentinel-apex.git)
   cd sentinel-apex

Launch the ecosystem:

Bash
docker-compose up -d --build
Access the Admin Panel at http://your-ip:81 to configure your SSL and Proxy.

💼 Commercial & SaaS Use
Sentinel APEX is built to be monetized. For high-volume API access, custom integrations, or white-label solutions, please visit the CyberDudeBivash Developer Portal.

📜 License
Distributed under the MIT License. See LICENSE.md for more information.

👨‍💻 Developed By
Bivash Kumar
Founder & CEO, CyberDudeBivash Pvt. Ltd.
Website | LinkedIn