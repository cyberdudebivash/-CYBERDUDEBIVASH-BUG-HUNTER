# CYBERDUDEBIVASH BUG HUNTER — Installation Guide

CYBERDUDEBIVASH BUG HUNTER is an automated reconnaissance and attack-surface discovery platform designed for bug bounty hunters and security researchers.

This guide explains how to install and run the platform.

---

## System Requirements

Recommended environment:

* Python 3.11
* 8GB RAM minimum
* Linux / Windows / macOS
* Internet connection
* Git (optional but recommended)

---

## Step 1 — Download the Platform

If you purchased from Gumroad:

1. Download the ZIP package
2. Extract it to a folder

Example:

```
CYBERDUDEBIVASH_BUG_HUNTER/
```

---

## Step 2 — Create Virtual Environment (Recommended)

Navigate to the project directory.

```
cd CYBERDUDEBIVASH_BUG_HUNTER
```

Create a virtual environment.

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

Install all required libraries.

```
pip install -r requirements.txt
```

This installs:

* aiohttp
* aiodns
* sqlmodel
* fastapi
* uvicorn
* other platform dependencies

---

## Step 4 — Verify Installation

Run the help command:

```
python main.py -h
```

You should see command options.

---

## Step 5 — Run First Scan

Example:

```
python main.py -d example.com -w subdomains.txt
```

Example with real target:

```
python main.py -d cloudflare.com -w subdomains.txt
```

---

## Step 6 — Launch Dashboard (Optional)

Start API backend:

```
uvicorn dashboard.backend.api_server:app --reload
```

Open in browser:

```
http://localhost:8000/docs
```

---

## Installation Complete

You are now ready to run automated reconnaissance scans.

For usage instructions see **USAGE.md**
