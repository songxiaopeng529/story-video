# Security Policy

## Supported versions

Security fixes are applied to the current `main` branch. After tagged releases begin, this table will identify any additional supported release lines.

## Report a vulnerability

Do not include sensitive details in a public issue.

Use GitHub private vulnerability reporting for this repository when it is enabled. If that channel is unavailable, open a minimal public issue titled `Private security contact requested` without technical details, exploit steps, secrets, or personal data; a maintainer can then establish a private channel.

Include privately, when relevant:

- Affected file and revision
- Impact and realistic threat scenario
- Minimal reproduction steps
- Any prompt, reference, or asset needed to reproduce the issue after removing secrets and personal data
- Suggested mitigation, if known

Maintainers will communicate acknowledgement, triage, remediation, and disclosure timing through the private channel. Please allow a reasonable remediation period before public disclosure.

## Security scope

Relevant reports include:

- Instructions or references that cause unintended tool execution or privilege expansion
- Prompt-injection content hidden in bundled examples, references, or assets
- Leakage of secrets, personal data, or inaccessible source material
- CI or validation behavior that executes untrusted content
- Dependency or installation behavior that differs materially from the documentation
- A safety boundary that reliably turns benign script generation into materially harmful operational guidance

Ordinary writing-quality problems, format preferences, and feature requests can use public issues.
