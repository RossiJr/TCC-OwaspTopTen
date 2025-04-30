# A09 – Security Logging and Monitoring Failures

## 1. Introduction  
Security Logging and Monitoring Failures (A09) occur when applications do not generate, store, analyze, or alert on critical security events. Unlike vulnerabilities that enable direct exploitation, this issue affects an organization’s ability to detect and respond to incidents effectively. In research, exploring this vulnerability involves triggering security-relevant actions and verifying if logs are generated, stored securely, and monitored in real-time.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify missing or weak logging and monitoring mechanisms 
- Provide manual techniques to simulate security incidents and analyze log coverage
- Document where logs are generated, how alerts are triggered, and where visibility gaps exist 

## 3. Repository Structure  
```plaintext
09-Logging_Monitoring_Failures/
├── docs/
│   └── flow-diagram.png         # Visual flowchart of the exploration steps
└── README.md                    # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Postman or Curl
    - ELK Stack, Splunk, or any log aggregator

## 5. Techniques and Tactics

1. **Event Simulation**
   - Trigger suspicious events like repeated login failures, forced browsing, and invalid requests.
   - Observe whether these actions are logged and stored.

2. **Log Injection Attempts**
   - Attempt to inject newlines or log-breaking payloads to check if logs are sanitized and stored safely.

3. **Anomaly Reproduction**
   - Perform actions that deviate from normal behavior (e.g., high-rate file downloads, late-night access) to test if alerts are triggered.

4. **Integrity Testing**
   - Try modifying or deleting log files directly (if accessible) to test log protection and retention policies.

5. **Log Review and Visualization**
   - Review logs in dashboards or raw files to ensure they include timestamps, IP addresses, user IDs, and outcomes.

## 6. Exploration Flow
1. **Define Expected Events:** Identify key activities that should be logged (e.g., login failures, file access, privilege use).
2. **Trigger Controlled Incidents:** Manually perform suspicious or malformed actions through HTTP or the UI.
3. **Verify Logging Output:** Check log files or dashboards to confirm whether and how the actions are recorded.
4. **Simulate Alert Conditions:** Attempt brute force or privilege escalation and monitor for alert generation.
5. **Inspect Storage & Integrity:** Review whether logs are tamper-resistant, centrally stored, and preserved over time.
6. **Document Gaps:** Note any missing logs, delayed alerts, or data that lacks sufficient detail for forensics.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. References
1. **OWASP Top 10 – Logging Failures:** https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
2. **NIST SP 800-92 – Log Management:** https://csrc.nist.gov/publications/detail/sp/800-92/final