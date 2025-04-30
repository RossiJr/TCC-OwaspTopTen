# A05 – Security Misconfiguration

## 1. Introduction  
Security Misconfiguration (A05) occurs when an application, server, database, or service is deployed with insecure default settings, unnecessary features, or incomplete setup procedures. These vulnerabilities often arise not from code flaws but from failure to securely configure systems and components. In research, exploring this vulnerability involves detecting exposed ports, weak or default credentials, verbose error handling, unprotected resources, and inadequate hardening across services and frameworks.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify misconfigured security points
- Provide manual techniques for scanning and exploitation
- Document exposed services, configuration files, default endpoints, and security headers

## 3. Repository Structure  
```plaintext
05-Security_Misconfiguration/
├── docs/
│   └── flow-diagram.png         # Visual flowchart of the exploration 
├── payloads/
│   └── misconfig-checklist.txt  # Checklist of common misconfigurations
├── scanner/
│   └── misconfig_scanner.py     # Script to detect open ports, weak headers, and sensitive files
└── README.md                    # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - `nmap`, `nikto`, `gobuster`, `curl`
    - Python 3.9
    - Postman
    - Burp Suite

## 5. Techniques and Tactics

1. **Service Enumeration**
   - Identify exposed services via port scanning (`nmap`)
   - Detect open admin panels and sensitive paths (`gobuster` or `dirb`)

2. **Header & Certificate Inspection**
   - Fetch response headers with `curl -I` or browser dev tools
   - Evaluate use of HTTPS, HSTS, and TLS version

3. **File & Directory Discovery**
   - Common targets: `.env`, `.git/`, `config.php`, `backup.zip`, `wp-config.php`
   - Look for accidental leaks and hardcoded secrets

4. **Credential Testing**
   - Try default or weak passwords for services like FTP, MySQL, Jenkins, Tomcat
   - Use automated tools for brute-force attempts

5. **Cloud Misconfig Testing**
   - Enumerate open S3 buckets (`s3scanner`, or other tools, or manually)
   - Inspect permissions, object access policies

6. **Verbose Error Analysis**
   - Trigger application errors and review stack traces, debug paths, or SQL errors

## 6. Exploration Flow
1. **Scan Ports and Services:**  Use `nmap -sV` to detect exposed ports and banners.
2. **Inspect Security Headers:** Analyze whether proper HTTP security headers are used.
3. **Probe Common Files:**  Attempt access to `.env`, `.git/config`, `debug.log`, etc.
4. **Check Admin Panels:** Test URLs like `/admin`, `/phpmyadmin`, `/server-status`.
5. **Brute-force Entry Points:** Try known credentials on login forms or exposed UIs.
6. **Test Cloud Resources:** Identify publicly accessible cloud buckets or misconfigured CDN.
7. **Document Exposures:** Log each misconfigured point and its exploitability.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. Payload Collections
   - **Common File Names and Paths:**
       - `.git/`, `.env`, `debug.log`, `config.json`, `admin.php`, `phpinfo.php`, `wp-config.php`
   - **Admin Interfaces:**
       - `/admin`, `/login`, `/console`, `/jenkins`, `/phpmyadmin`, `/server-status`
   - **Common Ports:**
       - `21` (FTP), `22` (SSH), `23` (Telnet), `80` (HTTP), `443` (HTTPS), `3306` (MySQL), `6379` (Redis), `27017` (MongoDB)
   - **Checklists & Wordlists:**
       - https://github.com/danielmiessler/SecLists
       - https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal


## 8. References
1. **OWASP Top 10 – Security Misconfiguration:** https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
2. **Nmap Scripting Engine (NSE):** https://nmap.org/nsedoc/
3. **TestSSL for TLS Config Checks:** https://github.com/testssl/testssl.sh
4. **AWS S3 Bucket Scanner:** https://github.com/sa7mon/S3Scanner