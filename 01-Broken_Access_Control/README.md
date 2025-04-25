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

## 5. Exploration Methodology
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

> See docs/flow-diagram.png for an illustrated walkthrough of these steps.

## 8. Payload Collections
- **Offensive-Payloads**  
  A general collection of offensive payloads and wordlists, including server config file attack vectors.  
  URL: https://github.com/InfoSecWarrior/Offensive-Payloads
- **Directory Traversal – PayloadsAllTheThings**  
  Enumeration of `../`-based path traversal payloads and examples.  
  URL: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md
- **PayloadsAllTheThings – Insecure Direct Object References**  
  Comprehensive IDOR payloads, methodologies, and Burp Intruder files.  
  URL: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Direct%20Object%20References

## 9. References

1. **OWASP Top 10: Broken Access Control** – https://owasp.org/A01_2021-Broken_Access_Control/