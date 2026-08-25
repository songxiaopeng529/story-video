# Contributing

Thank you for helping improve `write-video-scripts`. Contributions can refine instructions, add format knowledge, improve safety and factual handling, strengthen evaluation cases, or fix repository tooling.

## Before you start

- Open an issue first for a large workflow change, a new dependency, or a compatibility-breaking proposal.
- Keep the Skill client-neutral unless a file is explicitly product-specific, such as `agents/openai.yaml`.
- Do not add copyrighted scripts, lyrics, footage, images, fonts, music, or brand assets without a license that permits redistribution.
- Remove private, confidential, or personally identifying data from prompts and examples.

## Make a change

1. Fork the repository and create a focused branch.
2. Edit `skills/write-video-scripts/SKILL.md` only for core workflow instructions.
3. Put detailed patterns in a directly linked file under `references/`.
4. Keep `SKILL.md` under 500 lines and keep reference links one level deep.
5. Add or update an evaluation case when behavior changes.
6. Update both READMEs when user-facing behavior or installation changes.

Use imperative language in Skill instructions. Put trigger conditions in the frontmatter description, because clients read that metadata before loading the body.

## Validate locally

Run the self-contained checks:

```bash
python3 scripts/validate_repo.py
```

If the Agent Skills reference tool is available, also run:

```bash
skills-ref validate skills/write-video-scripts
```

Manually try at least one relevant prompt from `evals/cases.json`. Evaluate the listed invariants; do not require an exact-output snapshot from a generative model.

## Pull request checklist

- [ ] The Skill name still matches its directory.
- [ ] The description explains both capability and trigger contexts.
- [ ] Every referenced path exists and uses a relative link.
- [ ] No placeholder, invented source, or unverifiable claim remains.
- [ ] New examples are original or redistributable under this repository's license.
- [ ] Evaluation cases cover any new behavior or safety boundary.
- [ ] `python3 scripts/validate_repo.py` passes.
- [ ] User-facing changes appear in both READMEs.

## AI-assisted contributions

Disclose material AI assistance in the pull request description, including what the tool generated and what a human verified. Contributors remain responsible for correctness, licensing, safety, and factual review.

## License of contributions

Unless explicitly stated otherwise, contributions intentionally submitted to this project are licensed under the Apache License 2.0, consistent with section 5 of that license.
