# Security policy

Only the latest published beta or stable release receives security fixes.

Please do not publish a working privilege-escalation report in a public issue.
Contact the maintainer privately through the security-reporting method shown on
the repository profile. A dedicated address will be added before publication.

The privileged helper must remain root-owned and not writable by ordinary users.
It validates all input and intentionally supports only integer thresholds from
50 through 100.
