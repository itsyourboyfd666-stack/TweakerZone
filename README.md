# Grok MemoryOps Custom Model

This repository provides a ready-to-load custom instruction package for Grok that emphasizes disciplined instruction following, high-signal memory, and crisp responses.

## What is included
- **`config/grok_custom_model.json`** – declarative definition of persona, goals, memory policy, formatting rules, and escalation paths.
- **`scripts/export_grok_payload.py`** – utility that converts the configuration into a single payload suitable for Grok's Custom Instructions field.

## Usage
1. Generate the payload:
   ```bash
   python scripts/export_grok_payload.py --config config/grok_custom_model.json --pretty
   ```
2. Open **Grok → Settings → Custom Instructions** and paste the `system_prompt` from the generated JSON.
3. Use the `session_summary_template` as your running note after each chat, and keep the `persistent_memory_template` pinned for future sessions.

## Customization
- Update `config/grok_custom_model.json` to refine instructions, memory policies, or tone.
- Re-run the export script to regenerate the payload after any adjustments.

## Model focus
The MemoryOps model keeps track of goals, decisions, constraints, risks, and open questions. It leads with answers, surfaces assumptions, and asks targeted clarifications when context is missing. Memory summaries stay concise and date-stamped to help Grok recall the most relevant information across sessions.
