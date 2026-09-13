# Security policy

Only the latest published beta or stable release receives security fixes.

Please do not publish a working privilege-escalation report in a public issue.
Use [GitHub private vulnerability reporting](https://github.com/EmmeGeen-lab/battery-threshold/security/advisories/new)
to contact the maintainer without disclosing the report publicly.

The privileged helper must remain root-owned and not writable by ordinary users.
It validates all input and intentionally supports only integer thresholds from
50 through 100.
