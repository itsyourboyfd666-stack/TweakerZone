from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def section(title: str, lines: Iterable[str]) -> str:
    body = "\n".join(f"- {line}" for line in lines)
    return f"{title}:\n{body}"


def build_system_prompt(config: Dict[str, Any]) -> str:
    persona = config.get("persona", "A reliable AI assistant")
    goals: List[str] = config.get("goals", [])
    advanced = config.get("advanced_instructions", [])
    memory = config.get("memory", {})
    safety = config.get("safety_and_tone", [])
    escalation = config.get("escalation", [])
    formatting = config.get("output_formatting", {})

    lines: List[str] = [
        f"You are {persona}",
        section("Goals", goals),
        section("Core instructions", advanced),
        section("Memory recall", memory.get("recall_guidelines", [])),
        section("Memory retention", memory.get("retention_policy", [])),
        section("Memory compression", memory.get("compression_rules", [])),
        section("Knowledge slots", memory.get("knowledge_slots", [])),
        section("Safety and tone", safety),
        section("Escalation", escalation),
    ]

    formatting_notes = []
    if formatting.get("facts_first"):
        formatting_notes.append("Lead with the direct answer before details.")
    if formatting.get("numbered_steps_for_actions"):
        formatting_notes.append("Use numbered steps for action plans.")
    if formatting.get("style"):
        formatting_notes.append(formatting["style"])
    if formatting.get("timestamp_format"):
        formatting_notes.append(
            f"Timestamp references using format {formatting['timestamp_format']}."
        )

    if formatting_notes:
        lines.append(section("Response formatting", formatting_notes))

    clarity = config.get("clarity_checks", [])
    if clarity:
        lines.append(section("Clarity checks before finalizing answers", clarity))

    examples = config.get("examples", [])
    example_lines = [
        f"Scenario: {example.get('scenario', '')} -> Behavior: {example.get('modeling', '')}"
        for example in examples
    ]
    if example_lines:
        lines.append(section("Examples", example_lines))

    return "\n\n".join(lines)


def build_payload(config: Dict[str, Any]) -> Dict[str, Any]:
    system_prompt = build_system_prompt(config)
    memory = config.get("memory", {})

    return {
        "name": config.get("name", "Grok Custom Model"),
        "version": config.get("version", "0.0.1"),
        "capabilities": config.get("capabilities", []),
        "loading_notes": config.get("loading_notes", ""),
        "customization": {
            "system_prompt": system_prompt,
            "session_summary_template": memory.get("session_summary_template", ""),
            "persistent_memory_template": memory.get("persistent_memory_template", ""),
        },
        "customization_steps": config.get("customization_steps", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Grok customization payload from the provided config."
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the grok_custom_model.json file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional path to write the payload JSON instead of printing",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the payload with indentation",
    )

    args = parser.parse_args()
    config = load_config(args.config)
    payload = build_payload(config)

    output = json.dumps(payload, indent=2 if args.pretty else None)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
