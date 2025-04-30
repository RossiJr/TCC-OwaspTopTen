# A07 – Identification and Authentication Failures

## 1. Introduction  
Identification and Authentication Failures (A07) occur when applications do not properly protect authentication mechanisms, allowing attackers to compromise credentials, take over accounts, or manipulate session tokens. Unlike simple bugs, these flaws typically stem from weak credential policies, poor session handling, missing multi-factor authentication, or insufficient protection against brute-force and credential stuffing attacks.

In research, exploring this vulnerability involves testing authentication workflows, analyzing session behavior, and probing for login or reset flaws that can be exploited to gain unauthorized access.

## 2. Objectives  
- Develop a step-by-step methodology to test authentication flows  
- Enumerate weaknesses in login, session, and credential recovery processes  
- Document user roles, password policies, session controls, and abuse cases  

## 3. Repository Structure  
```plaintext
07-Auth_Failures/
├── docs/
│   └── flow-diagram.png           # Visual flowchart of the exploration steps
├── payloads/
│   ├── brute-force-user-pass.txt  # Sample usernames/passwords
│   └── token-reuse-cases.txt      # Known patterns for session and reset token abuse
├── automated_attacks/
│   └── hydra_bruteforce.sh        # Automated brute-force example using Hydra
└── README.md                      # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Burp Suite or OWASP ZAP (proxy and manual testing)
    - Python + Requests (for scripting session or login abuse)
    - A test environment with user login, password reset, and session management

## 5. Techniques and Tactics

1. **Brute-force Attack Simulation**
   - Use wordlists to test login endpoints.
   - Check for rate-limiting, lockouts, or CAPTCHA bypass.

2. **Credential Stuffing**
   - Try leaked credentials against login forms.
   - Observe if common passwords or reused tokens are accepted.

3. **Session Hijacking**
   - Intercept cookies and test reuse of session IDs or tokens.

4. **Token Manipulation**
   - Test password reset and remember-me tokens for guessability or reuse.

5. **Multi-Factor Authentication Bypass**
   - Analyze whether MFA is enforced consistently.
   - Attempt reusing valid session tokens to skip MFA flow.

## 6. Exploration Flow
1. **Identify Authentication Endpoints:** Login, logout, password reset, "remember me", MFA.
2. **Test Login Controls:** Attempt brute force and stuffing using Hydra, Burp Intruder, or other automated tool.
3. **Review Password and Session Policies:** Check length, reuse, expiration, reset logic.
4. **Capture and Replay Sessions:** Use Burp/ZAP to analyze cookie behavior and header configs.
5. **Check for Abuse Vectors:** Missing MFA, insecure remember-me, replay of password reset links.
6. **Document and Reproduce:** Log attack vectors that led to successful unauthorized access.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. Payload Collections
- **Authentication Bypass and Brute-force Lists:**
  - https://github.com/danielmiessler/SecLists/tree/master/Passwords
  - https://github.com/duyet/bruteforce-database
- **Session Attack Cases and Token Reuse:**
  - https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/JSON%20Web%20Token


## 8. References
1. **OWASP Top 10 – A07 Identification and Authentication Failures:**
https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
2. **OWASP Authentication Cheat Sheet:**
https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html