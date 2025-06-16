# A Practical OWASP Top 10–Based Framework for Assessing Web Application Security

This repository contains tools and scripts that support the thesis *"A Practical OWASP Top 10–Based Framework for Assessing Web Application Security"* by _José Fernando Rossi Júnior_ and _Matheus Alcântara Souza_.

## Overview

This project guides you through finding, testing, and documenting the OWASP Top Ten vulnerabilities in web applications. It follows a four-step process:

1. **Enumerating and Mapping**
   Locate all web endpoints, parameters, and input points.

2. **Defining Tests**
   Select and adapt attack payloads for each vulnerability.

3. **Exploiting and Verifying**
   Run proof-of-concept attacks and confirm whether each vulnerability exists.

4. **Reporting and Fixing**
   Generate clear reports with detailed findings and recommendations.

You will also find curated lists of example payloads for each vulnerability.

## Repository Structure

```
01-Broken_Access_Control/
02-Cryptographic_Failures/
03-Injections/
04-Insecure_Design/
05-Security_Misconfiguration/
06-Vulnerable_And_Outdated_Components/
07-Identification_And_Authentication_Failures/
08-Software_And_Data_Integrity_Failures/
09-Security_Logging_And_Monitoring_Failures/
10-SSRF/
docker-compose.yml
README.md
```

* **01–10 folders:** Each folder targets one OWASP Top Ten category.
* **docker-compose.yml:** Configuration to launch a vulnerable instance of OWASP Juice Shop.
* **README.md:** This file.

## Requirements

* Python 3.8 or newer
* Docker & Docker Compose
* Git

## Quick Start

1. **Clone and install dependencies**:

   ```bash
   git clone https://github.com/RossiJr/TCC-OwaspTopTen.git
   cd TCC-OwaspTopTen
   ```
2. **Launch the vulnerable target**:

   ```bash
   docker-compose up -d
   ```
3. **Run tests for a chosen category** (example: Cryptographic Failures)

4. **Review reports**

## Payload Examples

In some categories is possible to find the `payloads.txt` file for sample payloads. For additional examples, visit [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings).

