# 📖 CYBERDUDEBIVASH BUG HUNTER - Operational Manual
### Enterprise Intelligence & Distributed Reconnaissance Guide

This document contains the exact commands and workflows required to operate the world-class Bug Hunter ecosystem.

---

## 🚀 1. Core Execution Modes

### A. Local Deep-Recon (Single Target)
Use this for high-fidelity auditing of a specific domain. This runs the full integrated pipeline (Discovery -> Tech -> BOLA -> Cloud Hunter).
```bash
python main.py --domain example.com --mode local --wordlist wordlists/subdomains_top1000.txt