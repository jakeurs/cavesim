from typing import List, Dict, Any, Union, cast
from src.models.content import Ingredient, Decree


def check_compliance(item: Ingredient, decree: Decree) -> bool:
    for req in decree.requirements:
        req_type = req.get("type")
        value = req.get("value")

        if req_type == "has_tag":
            if value not in item.state_tags:
                return False
        elif req_type == "has_no_tag":
            if value in item.state_tags:
                return False
        elif req_type == "stat_gt":
            stat_name = req.get("stat")
            if not isinstance(stat_name, str):
                return False
            stat_value = getattr(item.stats, cast(str, stat_name), None)
            if stat_value is None or stat_value <= value:
                return False
        elif req_type == "stat_lt":
            stat_name = req.get("stat")
            if not isinstance(stat_name, str):
                return False
            stat_value = getattr(item.stats, cast(str, stat_name), None)
            if stat_value is None or stat_value >= value:
                return False
        elif req_type == "texture_is":
            if value not in item.state_tags:
                return False
    return True


def generate_question(decree: Decree) -> Dict[str, Any]:
    template_data = {}
    for token, req_key in decree.token_keys.items():
        for req in decree.requirements:
            if req.get("token_key") == token:
                template_data[token] = req.get(req_key)
                break

    correct_answer = decree.text_template.format(**template_data)

    options = [correct_answer]

    for token, value in template_data.items():
        if len(options) >= 4:
            break

        if isinstance(value, (int, float)):
            options.append(
                decree.text_template.format(**{**template_data, token: value + 10})
            )
            if len(options) < 4:
                options.append(
                    decree.text_template.format(
                        **{**template_data, token: max(0, value - 5)}
                    )
                )
        elif isinstance(value, str):
            options.append(
                decree.text_template.format(
                    **{**template_data, token: "counter-" + value}
                )
            )

    generic_distractors = [
        "Thermal variance exceeds safety margins.",
        "Unauthorized substitution of materials.",
        "Procedural violation: incorrect catalytic agent.",
    ]
    for d in generic_distractors:
        if len(options) >= 4:
            break
        if d not in options:
            options.append(d)

    return {
        "question": f"Regarding {decree.target_tag} in {decree.operation}: Which procedure is compliant?",
        "options": options,
        "answer": correct_answer,
    }
