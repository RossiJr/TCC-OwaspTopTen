# A06 – Vulnerable and Outdated Components

## 1. Introduction  
Vulnerable and Outdated Components (A06) refer to the usage of libraries, frameworks, containers, or other software modules that contain known security flaws. These components often become security liabilities when not updated, improperly configured, or used without awareness of publicly disclosed vulnerabilities (e.g., CVEs). In research, exploring this vulnerability involves enumerating all third-party and system-level components, verifying their versioning against vulnerability databases, and simulating real-world attacks based on known exploits.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify outdated or vulnerable components
-Provide manual and automated techniques to enumerate and analyze component versions
- Simulate exploitation of high-risk libraries (e.g., Log4Shell, Struts2, etc.)
- Document vulnerable versions, affected inputs, and patching strategies

## 3. Repository Structure  
```plaintext
06-Vulnerable_Outdated_Components/
├── docs/
│   └── flow-diagram.png             # Visual flowchart of the exploration process
├── scanners/
│   ├── pip_audit_scan.sh            # Bash script using pip-audit (Python projects)
│   ├── npm_audit_scan.sh            # Bash script using npm audit (Node.js projects)
│   └── trivy_scan.sh                # Container scanner for Docker images
├── vulnerable-simulations/
│   └── log4shell-demo/              # Proof-of-concept vulnerable Log4j app
└── README.md                        # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Python 3.9+, Node.js, Java (for scanning different ecosystems)
    - Trivy, Grype, pip-audit, npm audit, OWASP Dependency-Check, etc
    - Access to CVE databases (NVD, OSV, MITRE)
    - Docker (for container image analysis)

## 5. Techniques and Tactics

1. **Dependency Enumeration**
   - Use `pip freeze`, `npm ls`, or `mvn dependency:tree` to list direct and transitive dependencies.
   - Output package names and versions for scanning.

2. **Vulnerability Scanning**
   - Cross-reference component versions with CVEs on https://cve.mitre.org or https://osv.dev.

3. **Service & Banner Grabbing**
   - Use `nmap -sV` to identify exposed service versions on open ports (e.g., Apache 2.4.29).
   - Look for outdated CMS versions (WordPress, Drupal) via metadata or HTTP headers.

4. **Container & OS-Level Analysis**
   - Use `trivy` or `grype` to analyze Docker images or system packages

5. **Exploit Simulation**
   - Deploy a known vulnerable application (e.g., Log4Shell) and use crafted inputs to simulate exploitation.

## 6. Exploration Flow
1. **Inventory Components:** Scan the codebase, Dockerfiles, and deployment scripts to list software used.
2. **Run Scanners:** Use automated tools to generate vulnerability reports.
3. **Validate Vulnerabilities:** Compare reported versions with CVE proof-of-concept code or exploit DBs.
4. **Simulate Attacks:** Recreate known attacks using available test environments or crafted payloads.
5. **Mitigation and Patch Verification:** Apply updates and rerun scans to ensure vulnerabilities are resolved.
6. **Reporting:** Record outdated versions, affected attack surfaces, and proposed upgrade paths.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. References
1. **OWASP Top 10 – A06:** https://owasp.org/Top10/en/A06_2021-Vulnerable_and_Outdated_Components/
2. **OWASP Dependency-Check:** https://owasp.org/www-project-dependency-check/
3. **Trivy (Container Scanner):** https://github.com/aquasecurity/trivy
4. **Grype (SBOM Scanner):** https://github.com/anchore/grype
5. **OSV (Open Source Vulnerabilities):** https://osv.dev/
6. **CVE Database:** https://cve.mitre.org/