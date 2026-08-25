# Story Video

[简体中文](README.zh-CN.md)

An open-source Agent Skill for turning a topic, source document, brief, or rough draft into a production-ready video script.

`write-video-scripts` creates and revises short-form scripts, talking-head copy, explainers, tutorials, product demos, ads, interviews, documentary treatments, and narrative shorts. It keeps spoken copy, visible action, on-screen text, audio cues, timing, verification notes, and production constraints separate.

## Highlights

- Produces shootable scripts instead of prose with decorative camera labels
- Adapts structure and pacing to the objective, audience, duration, and format
- Supports scripts in the user's language, including Chinese and English
- Handles both sparse prompts and detailed production briefs
- Checks timing, speakability, visual feasibility, factual support, rights, and safety
- Uses the open [Agent Skills specification](https://agentskills.io/specification)
- Adds optional OpenAI UI metadata in `agents/openai.yaml`
- Requires no runtime package, API key, or model-specific tool

## Install

Copy the skill folder into the skills directory used by your compatible agent client. For Codex, run this from the repository root:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/write-video-scripts "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Open a new task after installation so the client can discover the skill. Other Agent Skills clients may use a different installation directory; copy the same `skills/write-video-scripts` folder without changing its name.

## Use

Invoke it explicitly:

```text
Use $write-video-scripts to create a 45-second vertical video for a neighborhood
coffee shop. One employee, one location, relaxed tone, and a save-oriented CTA.
```

Or ask naturally after installing it:

```text
Turn this product brief into a three-minute Bilibili explainer with narration,
shots, and on-screen text. Do not add performance claims that are not in the brief.
```

```text
Rewrite this 90-second script to fit 60 seconds. Keep the payoff, strengthen the
first three seconds, and explain only the material changes.
```

The default deliverable is a timecoded production script. The skill switches to spoken copy, a beat outline, or a revision format when that better matches the request.

## What it returns

A full production script can include:

- Creative brief and material assumptions
- Continuous estimated time ranges
- Shot or visible action
- Narration or dialogue
- On-screen text
- Music, sound, and transition cues
- Cast, location, prop, and capture notes
- Verified claims, sources, and verification gaps
- A compact delivery check

See the [Chinese coffee-shop example](examples/coffee-shop-45s.zh-CN.md) for one illustrative output. Model wording can vary; the evaluation targets are structural and behavioral invariants, not exact text matches.

## Repository layout

```text
story-video/
├── skills/write-video-scripts/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── evals/cases.json
├── examples/
├── scripts/validate_repo.py
└── .github/workflows/validate.yml
```

The main `SKILL.md` stays concise. Format patterns, output contracts, factual safeguards, and the quality rubric load only when relevant, following the progressive-disclosure guidance in the open specification.

## Validate

Run the repository-owned offline checks:

```bash
python3 scripts/validate_repo.py
```

These checks cover repository health files, frontmatter and naming constraints, OpenAI metadata, relative links, required references, unresolved markers, and the evaluation corpus.

For an additional conformance check, use the official reference implementation described by Agent Skills:

```bash
skills-ref validate skills/write-video-scripts
```

`skills-ref` is a demonstration reference library rather than a production dependency, so this repository's CI remains self-contained.

## Evaluation approach

The cases in `evals/cases.json` cover:

- A constrained short social video
- Adaptation that must remain within supplied facts
- A two-character vertical microdrama
- A deliberately underspecified request
- An unsafe medical-advertising request

They test invariants such as constraint coverage, non-fabrication, sensible defaults, production feasibility, and safe transformation. They intentionally avoid brittle whole-output snapshots.

## Safety and limitations

The skill does not render, edit, or publish video. Timing remains an estimate until a real read-through or edit. Current platform limits and regulated claims still require authoritative verification. The skill marks unsupported claims instead of inventing evidence and avoids deceptive real-person endorsements, unsafe guarantees, exact imitation of a living creator, and unlicensed third-party assets.

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), then run the validator before opening a pull request.

## License

Licensed under the [Apache License 2.0](LICENSE).
