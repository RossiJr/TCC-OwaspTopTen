# A02 – Cryptographic Failures

## 1. Introduction 
Cryptographic Failures (A02) occur when sensitive data is not adequately protected due to the incorrect implementation, configuration, or usage of cryptographic systems.
In the context of research, exploring this vulnerability involves a detailed analysis of how applications protect data at rest, in transit, and during processing, ensuring that strong algorithms, key management, and secure protocols are enforced.

## 2. Objectives
- Build a structured methodology (“flow”) to identify broken access control;
- Provide manual techniques to enumerate insecure encryption practices;
- Document relevant certificates, key storage practices, and cryptographic configurations.

## 3. Repository Structure  
```plaintext
02-Cryptographic_Failures/
├── docs/
│   └── flow-diagram.png         # Visual flowchart of the exploration steps
├── automated_cracker.py         # Automated script to detect weak ciphers,
|                                  missing HTTPS, and insecure certificates
├── payloads/
│   └── rainbow_table.txt        # List of known weak hashes for password 
|                                  cracking
│   └── rockyou.txt              # List of common weak passwords
└── README.md                    # This document
```

## 4. Prerequisites
- **Languages and Tools:**
  - Python 3.9+
  - Burp Suite and Wireshark (in case of manual verification)

## 5. Techniques and Tactics
1. Insecure Data Transmission
   - Use Wireshark or Burp Suite to analyze unencrypted traffic (HTTP vs HTTPS).
   - Check SSL/TLS configurations with SSL Labs or testssl.sh.
2. Weak Cipher Usage
   - Inspect the encryption algorithms being used (e.g., avoid RC4, MD5, SHA-1).
   - Enumerate supported cipher suites on HTTPS servers.
3. Improper Key Management
   - Search source code or public repositories for hard-coded keys or credentials.
   - Analyze server-side key management practices (e.g., key rotation, storage).
4. Weak or No Encryption at Rest
   - Review databases or storage to ensure sensitive data (passwords, personal info) is encrypted.
   - Check if strong cryptographic standards (AES-GCM, PBKDF2, bcrypt) are used.
5. Misconfigured Certificates
   - Check for self-signed, expired, or invalid certificates.
   - Analyze if applications properly validate server certificates.
6. Predictable Randomness
   - Review random number generation for weak sources (e.g., Math.random() instead of a cryptographically secure PRNG).
  
## 6. Exploration Flow
1. **Reconnaissance and Information Gathering:** 
    Use tools like Shodan, SSL Labs, or manual browsing to detect SSL/TLS weaknesses and visible encryption flaws.
2. **Network Traffic Inspection:**
    Capture and analyze traffic with Wireshark to identify data sent in plaintext or poorly encrypted.
3. **Configuration and Certificate Review:**
    Inspect server certificates for expiration, weak hashing algorithms (e.g., SHA-1), and improper issuer settings.
4. **Source Code and Key Exposure Review:**
    Perform code analysis to search for hardcoded secrets, exposed private keys, or insecure cryptographic operations.

5. **Storage Analysis:**
    Examine backups, databases, and local storage for plaintext sensitive data or usage of weak hash functions.

6. **Weakness Exploitation:**
    Attempt to decrypt captured data, crack hashed passwords, forge or tamper with session tokens, or exploit weak session management.

7. **Defense Evasion:**
    If traffic inspection or certificate validation is weak, attempt SSL stripping, man-in-the-middle attacks, or downgrades to weaker cipher suites.

8. **Data Collection:**
    After successful exploitation, gather sensitive data such as credentials, personal information, session tokens, or payment data.

> See docs/flow-diagram.png for an illustrated walkthrough of these steps.

## 7. Payload Collections
- **Commom weak/leaked passwords**
   This repository constains many leaked and weak auto-generated passwords. This is an important tool when cracking passwords.
   **URL:** https://github.com/danielmiessler/SecLists/tree/master/Passwords

## 8. References

1. **OWASP Top 10 - Cryptographic Failures:** https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
2. **SSL Labs – SSL Server Test:** https://www.ssllabs.com/ssltest/
3. **NIST - Cryptographic Standards:** https://csrc.nist.gov/Projects/Cryptographic-Standards-and-Guidelines
4. **OWASP Cryptographic Storage Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html