# Publication policy

This repository is public. Treat every tracked file as public material.

## Include

- synthetic data and examples;
- public documentation and links;
- generic procedures that do not reveal internal operations;
- claims with a clear source or an explicit limitation;
- short instructions that a reader can repeat safely.

## Do not include

- personal data or identifying details;
- credentials, tokens, keys, or secrets;
- private file paths, hostnames, endpoints, or infrastructure details;
- internal procedures or unpublished work information;
- commercial product details that are not already public;
- claims of DfE endorsement or official status;
- local recording files or unedited session output;
- generated pipeline runs under `synthetic-project/runs/`.

Use placeholders such as `YOUR_TOKEN` and `https://example.invalid` when an
example needs them.

## DfE wording

Use this statement when the context is relevant:

> This material was prepared for a Department for Education demonstration. It
> is independent. It is not official DfE guidance.

Do not imply that the Department has approved, adopted, or tested the material.

## Writing rules

- Use short sentences.
- Use one instruction per line.
- Prefer active voice.
- Define specialist terms at first use.
- Remove repetition and promotional wording.
- State limits and uncertainty.
- Use British English where practical.

## Constructive language

Keep critique impersonal and evidence-based.

- Focus on processes, controls, evidence, and outputs.
- Describe people and teams with respect.
- Describe gaps as current boundaries or learning opportunities.
- Use factual terms such as "not yet covered", "requires review", "out of
  scope", and "needs evidence".

## Pre-publish check

Before a commit or push:

1. Read every changed file.
2. Inspect the complete diff.
3. Check for personal data, secrets, private paths, and internal details.
4. Check every external claim and link.
5. Run the relevant tests and rendering checks.
6. Obtain explicit human approval.

No automated agent may approve its own publication.
