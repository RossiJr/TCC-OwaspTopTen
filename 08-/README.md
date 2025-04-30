# A08 – Software and Data Integrity Failures

## 1. Introduction  
Software and Data Integrity Failures (A08) refer to vulnerabilities where critical updates, dependencies, or CI/CD pipelines are not validated, exposing systems to tampering and supply chain attacks. These flaws often emerge when software is installed or updated without integrity verification or when infrastructure blindly trusts unverified sources. In research, this vulnerability is explored by examining update mechanisms, analyzing dependency chains, and simulating attacks like dependency confusion and malicious package injection.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify integrity validation gaps  
- Simulate tampering scenarios in CI/CD, package updates, and software fetchers
- Document weak trust boundaries, unverified sources, and impact from compromised artifacts

## 3. Repository Structure  
```plaintext
08-Software_Integrity_Failures/
├── docs/
│   └── flow-diagram.png           # Visual walkthrough of exploitation steps
├── demo/
│   ├── client.py                  # Simulated update client
│   ├── server.py                  # Malicious or trusted update server
│   └── update.py                  # Update content (clean or backdoored)
└── README.md                      # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Python 3.9x with `requests` and `http.server`
    - Burp Suite and OWASP Dependency-Check

## 5. Techniques and Tactics

1. **Unsigned Update Simulation**
   - Test how an application reacts when downloading unsigned files.
   - Replace real updates with tampered files served by an attacker..

2. **CI/CD Pipeline Abuse**
   - Check for lack of validation in automated build scripts.
   - Inject malicious content into artifacts via weak GitHub Actions or Jenkins steps.

3. **Dependency Confusion**
   - Mimic an internal package in public repositories (e.g., npm, PyPI) to trigger unintentional downloads.

4. **Hash Bypass and SRI Checks**
   - Remove or spoof hash/SRI enforcement on external scripts and test execution.

5. **Unverified Executable Downloads**
   - Identify and intercept endpoints that deliver `.exe`, `.jar`, or `.py` files.

## 6. Exploration Flow
1. **Identify Download Mechanism:**  Locate scripts, endpoints, or packages that fetch external resources or updates.
2. **Test for Integrity Validation:** Modify update content or package source and observe whether it is accepted/executed.
3. **Replace Trusted Source:** Run a local or rogue server that mimics the trusted update endpoint.
4. **Inject Malicious Payloads:** Craft backdoors in Python scripts, npm modules, or CI/CD pipeline steps.
5. **Simulate Installation or Build:** Trigger execution or build steps and observe behavior.
6. **Document Impact:** Log cases where tampering succeeds without detection or warning.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. References
1. **OWASP A08: Software and Data Integrity Failures:** https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
2. **OWASP Dependency-Check (SCA Tool):** https://owasp.org/www-project-dependency-check/