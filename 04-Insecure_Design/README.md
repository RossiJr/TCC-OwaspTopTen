# A04 – Insecure Design

## 1. Introduction  
Insecure Design (A04) occurs when a system's architecture lacks adequate security controls or uses flawed security assumptions from the start. Unlike implementation bugs, these flaws are embedded in how the application was conceived. In research, exploring this vulnerability involves identifying missing security requirements, reviewing the threat landscape during the design phase, and simulating abuse cases to demonstrate flaws in logic, process, or privilege separation.

## 2. Objectives  
- Build a structured methodology (“flow”) to identify injection points  
- Provide manual techniques to analyze application logic and threat modeling gaps
- Document user roles, business logic, abuse cases, and expected vs. actual behavior 

## 3. Repository Structure  
```plaintext
04-Insecure_Design/
├── docs/
│   └── flow-diagram.png         # Visual flowchart of the exploration 
└── README.md                    # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Threat Dragon or OWASP Threat Modeling Tool
    - Postman (for replaying malformed or unauthorized API requests)

## 5. Techniques and Tactics

1. **Logic Flow Analysis**
   - Identify assumptions in the workflow (e.g., "user must pay before download").
   - Manually tamper with steps to skip validations (e.g., force navigation to success page).

2. **Role & Privilege Testing**
   - Enumerate all user roles.
   - Attempt restricted actions as lower-privileged users (horizontal privilege escalation).

3. **Business Rule Violations**
   - Test for bypassing policy rules like rate limits, spending caps, workflow constraints.

4. **Threat Modeling Rebuild**
   - Reverse-engineer a Data Flow Diagram (DFD) from the app structure.
   - Identify trust boundaries

5. **Client vs. Server Enforcement**
   - Analyze whether input validation or role enforcement exists only on the client-side.

## 6. Exploration Flow
1. **Map User Journeys:**  Identify all business logic flows and decision points (checkout, registration, etc.).
2. **Extract Roles and Permissions:** Document all existing roles and what each should/shouldn't be able to do.
3. **Analyze Enforcement Points:** Identify where and how access, flow, or validations are enforced.
4. **Inject Abuse Cases:** Use crafted HTTP requests to skip steps, modify state transitions, or simulate edge conditions.
5. **Replay and Escalate:** Replay unauthorized actions and check if logic flaws allow privilege escalation or broken workflows.
6. **Document Outcomes:** Capture scenarios where assumptions break and control logic fails.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. Payload Collections
- **Business Logic Exploitation Cases:**
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Business%20Logic%20Errors

## 8. References
1. **OWASP Top 10 – Insecure Design:** https://owasp.org/Top10/A04_2021-Insecure_Design/
2. **OWASP Threat Modeling:** https://owasp.org/www-community/Threat_Modeling_Process
3. **PayloadsAllTheThings – Logic Abuse:** https://github.com/swisskyrepo/PayloadsAllTheThings