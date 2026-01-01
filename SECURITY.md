# Security Policy — OperatorX AI
OperatorX AI takes security seriously. This project is under active development, and we welcome responsible disclosure of vulnerabilities.
## Supported Versions
Because OperatorX AI is in early development, only the latest version on the `main` branch is supported.
- **Supported:** `main` (latest)
- **Not supported:** older commits, forks, or unmaintained branches
## Reporting a Vulnerability
If you believe you have found a security vulnerability, please report it responsibly.
### Please include:
- A clear description of the issue and impact
- Steps to reproduce (proof-of-concept if possible)
- Affected files/components
- Any logs or screenshots that help confirm the behavior
- Whether the issue impacts a specific tier (Personal / Business / Government)
### Where to report:
- **Preferred:** GitHub “Security Advisories” (if enabled on this repository)
- **Fallback:** Email: **security@operatorx-ai.net**
> Please do not publicly disclose vulnerabilities until we have had a chance to review and address the issue.
## Response Timeline (Target)
We aim to respond within the timeframes below (best effort for a small team):
- **Initial response:** within 72 hours
- **Triage & severity classification:** within 7 days
- **Fix or mitigation plan:** within 30 days (depending on severity and complexity)
## Security Practices (In Progress)
OperatorX AI is designed to support multiple deployment profiles and regulated environments, so security is planned as a first-class feature.
Current and planned practices include:
- Input validation and structured request models (FastAPI + Pydantic)
- Minimal default logging for privacy-sensitive contexts
- Tier-aware configuration (Personal / Business / Government)
- Dependency management and updates
- CI checks planned for linting, tests, and security scanning
## Out of Scope / Not Accepted
The following are generally out of scope for vulnerability reports:
- Social engineering or phishing attacks
- Physical attacks
- Denial-of-service testing against hosted infrastructure without permission
- Reports without reproducible details
## Responsible Disclosure
We appreciate researchers who follow responsible disclosure standards.
If requested, we can credit contributors in release notes or documentation after a fix is shipped.
Thank you for helping improve the security of OperatorX AI.
