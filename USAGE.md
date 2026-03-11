# CYBERDUDEBIVASH BUG HUNTER — Usage Guide

This document explains how to use the platform for reconnaissance and asset discovery.

---

## Basic Scan

Run a full reconnaissance pipeline.

```
python main.py -d target.com -w subdomains.txt
```

Example:

```
python main.py -d hackerone.com -w subdomains.txt
```

---

## Command Options

| Option | Description        |
| ------ | ------------------ |
| -d     | Target domain      |
| -w     | Subdomain wordlist |
| -c     | Concurrency level  |

Example:

```
python main.py -d target.com -w subdomains.txt -c 200
```

---

## Recon Pipeline Stages

The system automatically executes the following stages:

1. Subdomain intelligence gathering
2. DNS brute-force discovery
3. HTTP service probing
4. Port scanning
5. Technology fingerprinting
6. JavaScript endpoint extraction
7. Subdomain takeover detection

---

## Example Output

```
Subdomains discovered: 53
Resolved hosts: 41
HTTP services: 33
Open ports: 22
```

---

## Running Individual Modules

### DNS Recon

```
python swarm_recon_engine.py -d target.com -w subdomains.txt
```

### HTTP Probe

```
python http_probe_engine.py
```

### Port Scan

```
python port_scanner.py
```

---

## Database Storage

Results are stored in:

```
assets.db
```

You can inspect the database with SQLite tools.

---

## Recommended Wordlists

High-quality wordlists improve discovery.

Recommended:

```
subdomains-top1million-5000.txt
```

---

## Ethical Usage

Only scan systems you are authorized to test.

Use within:

* bug bounty programs
* authorized penetration tests
* research environments
