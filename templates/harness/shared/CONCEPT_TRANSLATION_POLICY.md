# Concept Translation Policy

Status: generated policy for user-facing output quality

Treat the user's request as intent, constraint, and concept. Do not treat the request text as copy that belongs in the delivered artifact.

## Core Rule

User-facing output should satisfy the concept without announcing that it
satisfies the concept.

Do not place the raw request, prompt wording, task label, or self-description
into the artifact unless the user explicitly asks for that exact wording. Do
not ban ordinary domain words only because the user used them.

## Avoid

- exact prompt phrases as headings, hero copy, button text, slogans, captions,
  or product labels when they read like assignment text instead of natural
  artifact language;
- meta-copy such as `as requested`, `here is`, `this is a`, `this website is`,
  `이것은`, `요청하신`, `요청에 따라`, `사용자가 요청한`, or equivalent
  task-fulfillment wording when it announces that the artifact satisfies the
  prompt;
- labels that describe the artifact from outside instead of speaking in the
  artifact's own domain voice;
- feature names that merely restate the assignment;
- portfolio or report text that reveals internal prompt wording when the output
  is meant to stand alone.

## Prefer

- domain-native names, headings, claims, flows, examples, and visual language;
- specific audience language instead of assignment language;
- concrete outcomes, objects, states, or choices that make the concept legible;
- task artifacts that store the prompt separately from public or user-facing
  copy.

## Allowed Exceptions

- PRD, anti-PRD, worker brief, evaluation report, benchmark, or internal task
  artifact that needs to quote the goal for traceability;
- legal, academic, or data task where exact wording is required evidence;
- user explicitly requests a literal title, slogan, label, or quoted phrase.

## Review Gate

Before closure, evaluation checks whether user-facing artifacts look like
finished domain output rather than an answer that repeats the prompt.

When available, run:

```sh
python3 scripts/harnessctl.py concept-check --task-id TASK --artifact-path PATH --forbidden-phrase "prompt phrase"
```

`concept-check` is a literal leakage guard. It also checks simple derived
phrases from the project goal, such as a goal with request verbs removed, as
contextual signals. Derived phrases are not universal bans by default. They are
flagged when paired with self-descriptive announcement language or when an
assignment-style phrase is used as prominent artifact copy. The helper does not
replace human design, writing, or domain judgment.
