# Confident AI Error Detector (Self-Contradiction)

An LLM-based verification tool designed to catch subtle, fluent, and highly confident self-contradictions in text—the type of logical hallucinations that easily bypass human readers and standard keyword filters.

---

## What Was Built
I built a Python-based evaluation framework that leverages an LLM (e.g., GPT-4o / Claude 3.5 Sonnet) forced into a strict Chain-of-Thought (CoT) reasoning path. The system ingests text blocks, isolates distinct logical claims, cross-references them for compatibility, and outputs a structured JSON evaluation containing a boolean flag and a specific diagnostic reason.

## Key Engineering Decisions & Why
1. **JSON Enforcement via System Prompting:** Instead of letting the model reply with freeform text, the prompt forces a strict JSON schema (`is_contradictory` and `reason`). This ensures the detector can easily be integrated into automated CI/CD pipelines or database workflows.
2. **Mandatory Step-by-Step Analysis:** The prompt instructs the model to explicitly execute three logical steps *before* rendering the JSON verdict. This significantly mitigates "recency bias", where an LLM might otherwise only remember the last sentence it read.
3. **Deterministic Settings:** The model is configured with a `temperature` of `0.0` to minimize creative variance and ensure consistent evaluation passes.

---

## Where the AI Gave Wrong/Weak Output & How I Fixed It

During initial iterations, the AI model acting as the detector suffered from two major flaws when trying to identify confident errors:

### 1. The "Nuance vs. Contradiction" False Positive
* **The Weakness:** When given a test case with a valid rhetorical pivot (e.g., *"The algorithm generally prioritizes speed, but under heavy server loads, it shifts entirely to data preservation"*), an early version of the prompt flagged it as a contradiction. The LLM lazily equated the word "but" and a shift in system state with a logical flaw.
* **How I Caught It:** I ran a clean, nuanced technical narrative through the detector. It falsely flagged it with `true`, proving it couldn't differentiate between conditional logic and actual self-negation.
* **The Fix:** I updated the system instructions to explicitly define a self-contradiction as a state where *"Claim A and Claim B cannot both be true simultaneously under any condition."* I also added a step requiring the model to check for conditional shifts before throwing a flag.

### 2. Failure on Mathematical / Timeline Mismatches
* **The Weakness:** When tested on a subtle timeline error (Amelia Earhart departing May 20th and disappearing June 2nd after a *"two-month journey"*), a basic prompt missed the contradiction completely. The text was so fluent and authoritative that the LLM fell into a "praise bias" and passed it.
* **How I Caught It:** Systematic boundary testing with historical text cases containing intentionally broken arithmetic.
* **The Fix:** I altered the prompt's structural checklist, explicitly commanding the LLM to: *"Calculate the mathematical and chronological differences between any dates, percentages, or metrics mentioned to verify their alignment."*

---

## Measuring Reliability & False-Positive Risks
*(Include a brief summary of the Half-Page Reliability Note we generated in the previous step here to complete the requirement.)*