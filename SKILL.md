---
name: wrong-answer-diagnostic-trainer
description: Diagnose mistakes in primary-school arithmetic or word problems, explain the likely cause without labelling the learner, and generate verified same-type, contrast, transfer, and spaced-review practice. Use when a parent or teacher provides a wrong answer, marked worksheet, or batch of student responses and wants targeted remediation rather than a generic test.
---

# Wrong Answer Diagnostic Trainer

Turn evidence from a learner's work into a checked remediation loop:

`wrong answer -> first divergence -> evidence-based diagnosis -> child-friendly reteach -> graduated variants -> delayed review`

## Inputs

Ask only for missing information that changes the result:

- Required: original question and the learner's answer or working.
- Strongly preferred: grade, correct answer or marking result, and whether this is a repeated error.
- Optional: recent similar errors, allowed number range, curriculum version, desired question count, output format, and learner name or nickname.

If the original question is visible in an image, transcribe it and confirm ambiguous symbols before diagnosing. Do not guess whether a faint mark is `1`, `7`, `+`, `-`, `x`, or `÷`.

## Modes

- **Single-error diagnosis:** Analyse one item deeply and generate a compact practice ladder.
- **Batch diagnosis:** Group several errors by shared underlying cause; do not produce a separate long report for every item.
- **Practice-only:** When the diagnosis is already supplied, generate and verify the requested variants without repeating the analysis.
- **Printable report:** Produce structured JSON and render the polished HTML report described below.

## Workflow

1. Solve the original question independently before reading the learner's reasoning as an explanation.
2. Locate the first step where the learner's work diverges from a valid solution. Later errors may be consequences, not causes.
3. Read [references/diagnostic-taxonomy.md](references/diagnostic-taxonomy.md) and classify the strongest supported cause. Report:
   - observed evidence;
   - likely cause;
   - confidence: high, medium, or low;
   - one plausible alternative when confidence is not high.
4. Never use character labels such as "粗心", "基础差", or "不认真" as a diagnosis. Describe the observable action instead.
5. Give a child-friendly explanation using the smallest useful worked example. Contrast the incorrect move with the correct move.
6. Read [references/variation-design.md](references/variation-design.md) and build a graduated practice set. Unless the user specifies otherwise, create:
   - 2 same-structure questions;
   - 2 contrast questions that require choosing the right method;
   - 2 transfer questions with changed surface features;
   - 2 delayed-review questions for later reuse.
7. Solve every generated item independently. Check that the answer is unique, grade-appropriate, within the requested number range, and does not accidentally introduce an unrequested concept.
8. Separate learner pages from the answer key. Do not reveal answers beside practice questions unless the user explicitly requests guided practice.

## Output

For ordinary chat output, use this order:

1. **一句话结论** — neutral summary of the learning gap.
2. **证据与判断** — first divergence, likely cause, confidence, and alternative explanation if needed.
3. **给孩子的讲解** — short, concrete, and non-judgmental.
4. **示范题** — one fully worked example with the critical step highlighted.
5. **分层变式训练** — same-structure, contrast, then transfer.
6. **延迟复习** — specify when to retry, normally the next day and 3–7 days later.
7. **答案与核验** — separate section containing answers and brief checking notes.
8. **家长/教师建议** — one thing to observe next time; avoid generic encouragement.

Do not claim a stable misconception from one answer. Phrase a single-item conclusion as a hypothesis to test with contrast questions.

## Printable UI

When the user asks for a polished, printable, or product-style result:

1. Read [references/report-schema.md](references/report-schema.md).
2. Write UTF-8 JSON matching that schema.
3. Run:

```text
python scripts/render_report.py report.json report.html
```

4. Open or preview the generated HTML when the environment supports it. Verify that question pages and answer pages print separately and that no answer appears on a learner page.

If Python execution is unavailable, return the same content as well-structured Markdown instead of blocking the task.

## Quality Gates

- Mathematical correctness is mandatory; regenerate any ambiguous or invalid item.
- Diagnosis must cite evidence from the learner's work, not personality assumptions.
- Variants must target the diagnosed skill rather than merely changing numbers.
- Change one major difficulty dimension at a time in early practice.
- Use age-appropriate Chinese and notation.
- Preserve privacy: omit full names and unnecessary personal details from reports.
- For high uncertainty, ask for one additional contrast response or present the diagnosis as provisional.

