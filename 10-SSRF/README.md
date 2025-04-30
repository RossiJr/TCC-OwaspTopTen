# A10 - Server Side Request Forgery (SSRF)

## 1. Introduction  
Server-Side Request Forgery (SSRF) (A10) arises when an attacker can coerce a server-side application to send HTTP requests to arbitrary destinations—often internal systems or protected resources the attacker cannot reach directly. Unlike traditional injection bugs, SSRF exploits the server as a proxy, enabling enumeration of internal services, access to sensitive metadata endpoints, and potential pivoting deeper into the network.

## 2. Objectives  
- Define a repeatable workflow (“flow”) to discover SSRF-vulnerable endpoints
- Combine manual and automated techniques to inject SSRF payloads
- Capture out-of-band interactions (DNS/HTTP callbacks) and map internal services
- Document all tested parameters, discovered endpoints, and observed behaviors

## 3. Repository Structure  
```plaintext
10-Server_Side_Request_Forgery/
├── docs/
│   └── flow-diagram.png         # Illustrated SSRF testing workflow
├── scripts/
│   └── ssrf_scanner.py          # Automated scanner for common SSRF vectors
├── payloads/
│   ├── ssrf_dns_payloads.txt    # DNS-based callback payloads for OOB detection
│   └── ssrf_urls.txt            # URL schemes (& fuzzing patterns) to test
└── README.md                    # This document
```

## 4. Prerequisites
- **Languages and Tools:**
    - Python 3.9x for custom scripts
    - Burp Suite
    - SSRFmap (for quick payload generation)
    - Curl or Postman for manual request crafting
    - DNS/HTTP OOB logging service

## 5. Techniques and Tactics

1. **Parameter Profiling**
   - Enumerate all inputs that accept URLs or hostnames (uploaders, image fetchers, PDF generators).
   - Record default behavior (e.g., what URL is fetched, any errors).

2. **Payload Injection & Fuzzing**
   - Inject crafted payloads (e.g., http://\<domain\>, file:///etc/passwd).
   - Use SSRFmap or Burp Intruder to automate permutations `(http://127.0.0.1`, `http://[::1]`

3. **Out-of-Band (OOB) Callback Detection**
   - Monitor DNS or HTTP interactions
   - Identify successful SSRF when the server resolves or connects back.

4. **Internal Service Discovery**
   - Target common internal ports (e.g., 127.0.0.1:5984, 169.254.169.254 for metadata).
   - Leverage HTTP, gopher, and file schemes to probe internal APIs or metadata endpoints.

5. **Metadata & Cloud Exploit**
   - Extract tokens, instance identities, or SSH keys.

6. **Full Chain Exploitation**
   - Once metadata is retrieved, use credentials to pivot (e.g., AWS CLI calls to S3).

## 6. Exploration Flow
1. **Discovery:**  Crawl the application: identify all URL-accepting parameters and endpoints.
2. **Baseline Testing:** Send benign requests (e.g., your own public URL) to confirm SSRF proxying.
3. **OOB Payload Injection:** Inject DNS/HTTP callback payloads; monitor for interactions.
4. **Fuzz & Bypass Filters:** Test alternate address formats (hex, octal, IPv6), URL schemes (file, gopher).
5. **Internal Scanning:** Sequentially probe internal services/ports; log any successful connections.
6. **Metadata Enumeration:** Target cloud metadata endpoints; capture and analyze responses.
7. **Document & Report:** Record each payload, parameter, detected behavior, and remediation recommendation.

> See docs/flow-diagram.png for an illustrated walkthrough.

## 7. Payload Collections
- **PayloadsAllTheThings – SSRF:** https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery
- **SSRFmap:** https://github.com/swisskyrepo/SSRFmap
- **OOB Interaction Service - Interact.sh:** https://github.com/projectdiscovery/interactsh

## 8. References
1. **OWASP Top 10 – SSRF:** https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/
2. **SSRF Testing Guide (PortSwigger):** https://portswigger.net/web-security/ssrf