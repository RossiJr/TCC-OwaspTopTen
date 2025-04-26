# A01 – Broken Access Control

## 1. Introduction  
Broken Access Control (A01) occurs when an application does not properly enforce access permissions, thereby allowing attackers to act outside of their intended privileges. In the context of research, exploring this vulnerability involves a systematic examination of both horizontal access controls (same-level roles) and vertical (elevation to higher-privileged roles) access controls.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify broken access control;
- Provide automated and manual techniques to enumerate unauthorized operations;  
- Document relevant database schemas, configuration files, and common service ports.

## 3. Repository Structure  
```plaintext
01-Broken_Access_Control/
├── docs/
│   └── flow-diagram.png       # Visual flowchart of the testing process
├── server/
│   └── main.py                # Built-in server to exemplify those
│                                 vulnerabilities
├── automated_enumerating.py   # Automated script to identify IDOR|Path
│                                 Traversal|Malconfigured files
├── payloads.txt               # Pre-built payload used for Malconfigured
│                                 Files and Path Traversal
└── README.md                  # This document
```

## 4. Prerequisites
- **Languages and Tools:**
  - Python 3.9+
  - Burp Suite (in case of manual verification)
- **Python Libraries:**
  - Flask

## 5. Techniques and Tatics
1. Anonymous Access
   - Attempt to access protected endpoints without credentials
   - Verify HTTP status codes (should return 401 or 403)
2. Horizontal Escalation (IDOR Testing)
   - For an automated exploration, use automated_enumerating.py with IDOR set in the type configuration property.
   - Detect endpoints where changing the resource ID grants unauthorized access
3. Vertical Escalation (Role Manipulation)
   - Intercept a valid JWT for a low-privilege user
   - Modify the role claim to admin with tampering
   - Replay the token against admin-only endpoints
4. Mass Assignment
   - Submit JSON payloads including hidden or privileged fields (e.g., isAdmin: true)
   - Observe whether backend logic filters out unauthorized fields
5. Configuration Review
   - Inspect .env, config/database.yml, or appsettings.json for default creds
   - Examine web server configs (nginx.conf, .htaccess) for directory-level rules

## 6. Exploration Flow

1. **Reconnaissance and Scanning:**
  Use tools such as NMAP, or other semi-automated scanning tool that might reveal endpoints susceptible to access-control testing.
2. **Initial Access:**
  Attempt exploring application misconfigurations or known flaws in web applications. This might grant you with more susceptible endpoints for further testing.
3. **Credential Access (Valid Access):**
  Obtain valid credentials via default credentials, or credential stuffing, or pishing. With valid accounts, you can now bypass superficial access control and define a basis for a deeper exploration.
4. **Discovery:**
  Enumerate user roles and accounts through APIs, predictable endpoints, or error messages. It is possible to perform targeted IDOR and role-based checks when knowing existing accounts.
5. **Execution:**
  Using automated scripts (e.g., Python IDOR Scanners, Burp Intruder Payloads) to interact with the application. Those scripts allow a fast and repeatable testing of resource identifier and parameters.
6. **Defense Evasion:**
  Tamper with or bypass authentication logic by altering session tokens, forging SSO requests, or injecting malicious modules. Then you can evade server-side checks.
7. **Privilige Escalation:**
  Try to intercept and change JSON Web Tokens (JWT) or cookies to change roles and permissions, confirming server-side rejects tampered tokens.
8. **Collection:**
  After gaining the unauthorized access, harverst data from repositories, file shares, databases, and any other data-source exposed via broken controls.  

> See docs/flow-diagram.png for an illustrated walkthrough of these steps.

## 7. Payload Collections
- **Offensive-Payloads**  
  A general collection of offensive payloads and wordlists, including server config file attack vectors.  
  URL: https://github.com/InfoSecWarrior/Offensive-Payloads
- **Directory Traversal – PayloadsAllTheThings**  
  Enumeration of `../`-based path traversal payloads and examples.  
  URL: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md
- **PayloadsAllTheThings – Insecure Direct Object References**  
  Comprehensive IDOR payloads, methodologies, and Burp Intruder files.  
  URL: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Direct%20Object%20References

## 8. References

1. **OWASP Top 10 - Broken Access Control:** https://owasp.org/A01_2021-Broken_Access_Control/
2. **MITRE - Access Token Manipulation:** https://attack.mitre.org/techniques/T1134/
3. **MITRE - Valid Accounts:** https://attack.mitre.org/techniques/T1078/