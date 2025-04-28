# A03 – Injection

## 1. Introduction  
Injection (A03) occurs when untrusted input is interpreted as part of a command or query, allowing attackers to alter the intended execution flow of an application or database. In research, exploring this vulnerability involves systematically testing various injection vectors (SQL, OS commands, NoSQL, LDAP, XPath, etc.) and evaluating how inputs are handled, sanitized, and parameterized.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify injection points  
- Provide manual and automated techniques to enumerate and exploit injection flaws  
- Document relevant endpoints, parameters, and query structures for reproducibility  

## 3. Repository Structure  
```plaintext
03-Injection/
├── docs/
│   └── flow-diagram.png          # Visual flowchart of the exploration steps
├── payloads/
│   ├── sql-payloads.txt          # Common SQL injection payloads
│   ├── command-payloads.txt      # OS command injection payloads
│   └── nosql-payloads.txt        # NoSQL injection payloads
└── README.md                     # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Python 3.9+
    - SQLMap, Burp Suite, OWASP ZAP
    - Netcat (for manual OS command injection)

## 5. Techniques and Tactics

1. **SQL Injection**
   - Manual: Inject delimiters (', ") to trigger errors; use UNION SELECT to enumerate tables.
   - Automated: Run SQLMap to fingerprint the DBMS and extract data.

2. **OS Command Injection**
   - Manual: Append shell metacharacters (;, &&, |) to execute arbitrary commands.
   - Automated: Use Burp Intruder or custom Python scripts to batch-test payloads.

3. **NoSQL Injection**
   - Test JSON inputs for unvalidated operators (e.g., {"\$ne": null}, {"\$gt": ""}).

4. **LDAP Injection**
   - Inject filter metacharacters (*, |, &) to manipulate LDAP queries and bypass authentication.

5. **XPath Injection**
   - Use payloads (e.g., ' or '1'='1) to alter XML query logic and retrieve unauthorized data.

## 6. Exploration Flow
1. **Identify Input Vectors:** Map all user-controlled inputs (forms, headers, API parameters).
2. **Probe for Injection:** Inject basic delimiters (', ", ;) and observe errors or behavioral anomalies.
3. **Enumerate and Exploit:** For SQL: perform error-based, UNION-based, blind, and time-based techniques. For OS: test command separators and environment variable dumps.
4. **Automate Testing:** Execute automated_injection_tester.py against identified endpoints.
5. **Privilege Escalation & Data Exfiltration:** Extract credentials, configuration files, or execute system commands where possible.
6. **Reporting:** Log successful payloads, vulnerable endpoints, and all extracted data for analysis.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. Payload Collections
- **SecLists – SQL Injection:**
https://github.com/InfoSecWarrior/Offensive-Payloads/blob/main/SQL-Injection-Payloads.txt
- **PayloadBox – Command Injection:**
https://github.com/payloadbox/command-injection-payload-list

## 8. References
1. **OWASP Top 10 – Injection:** https://owasp.org/Top10/A03_2021-Injection/
2. **SQL Injection Prevention Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
3. **SQLMap Documentation:** https://sqlmap.org/ 