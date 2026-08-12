"""Resolve configurable model and effort choices for agentic work."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROLES = ("implementation", "planning", "review")
EFFORTS = ("low", "medium", "high", "max")
DEFAULT_CONFIG = Path(__file__).with_name("models.json")
DEFAULT_TASK_REGISTER = Path(__file__).resolve().parents[3] / "TASKS.md"


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    """Load and validate a user-editable model roster and route table."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load model roster: {exc}") from exc
    validate_config(data)
    return data


def validate_config(config: dict[str, Any]) -> None:
    """Validate roster shape, capabilities, efforts, and configured routes."""
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError("model roster schema_version must be 1")
    models = config.get("models")
    if not isinstance(models, list) or not models:
        raise ValueError("model roster must contain at least one model")

    ids: set[str] = set()
    for model in models:
        if not isinstance(model, dict):
            raise ValueError("each model roster entry must be an object")
        model_id = model.get("id")
        if not isinstance(model_id, str) or not model_id:
            raise ValueError("each model must have a non-empty id")
        if model_id in ids:
            raise ValueError(f"duplicate model id: {model_id}")
        ids.add(model_id)
        if not isinstance(model.get("label"), str) or not model["label"]:
            raise ValueError(f"model {model_id} needs a label")
        if not isinstance(model.get("provider"), str) or not model["provider"]:
            raise ValueError(f"model {model_id} needs a provider label")
        if not isinstance(model.get("available"), bool):
            raise ValueError(f"model {model_id} needs an available flag")
        capabilities = model.get("capabilities")
        if not isinstance(capabilities, list) or not set(capabilities).issubset(ROLES):
            raise ValueError(f"model {model_id} has invalid capabilities")
        efforts = model.get("efforts")
        if not isinstance(efforts, list) or not efforts or not set(efforts).issubset(EFFORTS):
            raise ValueError(f"model {model_id} has invalid efforts")

    routes = config.get("routes")
    if not isinstance(routes, dict) or set(routes) != set(ROLES):
        raise ValueError(f"routes must define exactly: {', '.join(ROLES)}")
    for role in ROLES:
        route = routes[role]
        if not isinstance(route, dict):
            raise ValueError(f"route {role} must be an object")
        model_id = route.get("model")
        effort = route.get("effort")
        if model_id not in ids:
            raise ValueError(f"route {role} selects unknown model: {model_id}")
        model = next(item for item in models if item["id"] == model_id)
        if not model["available"]:
            raise ValueError(f"route {role} selects unavailable model: {model_id}")
        if role not in model["capabilities"]:
            raise ValueError(f"model {model_id} cannot perform role {role}")
        if effort not in model["efforts"]:
            raise ValueError(f"model {model_id} does not support effort {effort}")
        if not isinstance(route.get("reason"), str) or not route["reason"]:
            raise ValueError(f"route {role} needs a reason")

    tag_routes = config.get("tag_routes", [])
    if not isinstance(tag_routes, list):
        raise ValueError("tag_routes must be a list")
    seen_tags: set[tuple[str, str]] = set()
    for tag_route in tag_routes:
        if not isinstance(tag_route, dict):
            raise ValueError("each tag route must be an object")
        tag = tag_route.get("tag")
        role = tag_route.get("role")
        if not isinstance(tag, str) or not tag:
            raise ValueError("each tag route needs a non-empty tag")
        if role not in ROLES:
            raise ValueError(f"tag route {tag} has invalid role: {role}")
        if (tag, role) in seen_tags:
            raise ValueError(f"duplicate tag route: {tag}/{role}")
        seen_tags.add((tag, role))
        model_id = tag_route.get("model")
        effort = tag_route.get("effort")
        model = next((item for item in models if item["id"] == model_id), None)
        if model is None:
            raise ValueError(f"tag route {tag} selects unknown model: {model_id}")
        if not model["available"]:
            raise ValueError(f"tag route {tag} selects unavailable model: {model_id}")
        if role not in model["capabilities"]:
            raise ValueError(f"model {model_id} cannot perform tag role {role}")
        if effort not in model["efforts"]:
            raise ValueError(f"model {model_id} does not support tag effort {effort}")
        if not isinstance(tag_route.get("reason"), str) or not tag_route["reason"]:
            raise ValueError(f"tag route {tag} needs a reason")


def normalize_tag(value: str) -> str:
    """Normalize hash-prefixed task tags for cross-harness routing."""
    return value.strip().lstrip("#").lower()


def task_tags_from_register(path: Path, task_id: str) -> list[str] | None:
    """Read hash tags from a task row in the authoritative task register."""
    wanted = task_id.strip()
    if not wanted:
        return None
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot load task register: {exc}") from exc

    for line in content.splitlines():
        if "|" not in line:
            continue
        cells = [cell.strip() for cell in line.split("|")[1:]]
        first_cell = cells[0].strip("`") if cells else ""
        if first_cell != wanted:
            continue
        tags = re.findall(r"#[A-Za-z0-9][A-Za-z0-9_-]*", line)
        return list(dict.fromkeys(normalize_tag(tag) for tag in tags))
    return None


def _first_tag_route(config: dict[str, Any], tags: list[str], role: str | None = None) -> dict[str, Any] | None:
    normalized = {normalize_tag(tag) for tag in tags}
    return next(
        (
            rule for rule in config.get("tag_routes", [])
            if (role is None or rule["role"] == role)
            and normalize_tag(rule["tag"]) in normalized
        ),
        None,
    )


def roster(config: dict[str, Any], *, available_only: bool = False) -> list[dict[str, Any]]:
    """Return the configured roster for user inspection."""
    models = config["models"]
    if available_only:
        models = [model for model in models if model["available"]]
    return models


def _selection(
    config: dict[str, Any],
    role: str,
    route: dict[str, Any],
    *,
    model_id: str | None,
    effort: str | None,
    selection: str,
) -> dict[str, Any]:
    selected_model_id = model_id or route["model"]
    model = next((item for item in config["models"] if item["id"] == selected_model_id), None)
    if model is None:
        raise ValueError(f"unknown model: {selected_model_id}")
    if not model["available"]:
        raise ValueError(f"model is unavailable: {selected_model_id}")
    if role not in model["capabilities"]:
        raise ValueError(f"model {selected_model_id} cannot perform role {role}")
    selected_effort = effort or route["effort"]
    if selected_effort not in model["efforts"]:
        raise ValueError(f"model {selected_model_id} does not support effort {selected_effort}")
    return {
        "role": role,
        "model_id": selected_model_id,
        "label": model["label"],
        "provider": model["provider"],
        "cost_tier": model.get("cost_tier", "unspecified"),
        "effort": selected_effort,
        "selection": selection,
        "reason": route["reason"],
    }


def select_route(
    config: dict[str, Any],
    role: str,
    *,
    model_id: str | None = None,
    effort: str | None = None,
) -> dict[str, Any]:
    """Select a configured route, optionally overriding model and effort."""
    validate_config(config)
    if role not in ROLES:
        raise ValueError(f"role must be one of: {', '.join(ROLES)}")
    return _selection(
        config, role, config["routes"][role], model_id=model_id, effort=effort,
        selection="override" if model_id or effort else "configured",
    )


def select_for_task(
    config: dict[str, Any],
    task_id: str,
    role: str | None = None,
    *,
    tags: list[str] | tuple[str, ...] = (),
    model_id: str | None = None,
    effort: str | None = None,
    task_register: Path = DEFAULT_TASK_REGISTER,
) -> dict[str, Any]:
    """Resolve task tags from the register, then select the matching role route."""
    validate_config(config)
    if not task_id.strip():
        raise ValueError("task_id must not be empty")

    register_tags = task_tags_from_register(task_register, task_id)
    if register_tags is None:
        raise ValueError(f"task not found in {task_register}: {task_id}")
    supplied_tags = [normalize_tag(tag) for tag in tags if normalize_tag(tag)]
    clean_tags = list(dict.fromkeys([*register_tags, *supplied_tags]))
    task_match = _first_tag_route(config, register_tags)
    supplied_match = _first_tag_route(config, supplied_tags)
    task_role = task_match["role"] if task_match else None
    supplied_role = supplied_match["role"] if supplied_match else None

    if task_role and supplied_role and task_role != supplied_role:
        raise ValueError(
            f"task tags select {task_role}, but supplied tags select {supplied_role}; "
            f"resolve the conflict in {task_register}"
        )
    if task_role and role and task_role != role:
        raise ValueError(f"task tags select {task_role}, not the requested role {role}")
    selected_role = task_role or role or supplied_role
    if selected_role not in ROLES:
        raise ValueError(
            f"task {task_id} has no mapped role; add a role tag or pass --role "
            f"from: {', '.join(ROLES)}"
        )

    matched = _first_tag_route(config, clean_tags, selected_role)
    route = matched or config["routes"][selected_role]
    selection = "override" if model_id or effort else "tag" if matched else "configured"
    result = _selection(
        config, selected_role, route, model_id=model_id, effort=effort, selection=selection,
    )
    result.update({"task_id": task_id, "tags": clean_tags, "matched_tag": normalize_tag(matched["tag"]) if matched else None})
    return result


def interactive_select(config: dict[str, Any], task_id: str, role: str | None, tags: list[str]) -> dict[str, Any]:
    """Show compatible models and prompt for a model and effort in this session."""
    default = select_for_task(config, task_id, role, tags=tags)
    resolved_role = default["role"]
    choices = [
        model for model in config["models"]
        if model["available"] and resolved_role in model["capabilities"]
    ]
    print(f"Task {task_id} | role={resolved_role} | tags={','.join(default['tags']) or '(none)'}")
    print("Available compatible models:")
    for model in choices:
        print(f"- {model['id']}: {model['label']} [{', '.join(model['efforts'])}]")
    selected_model = input(f"Model [{default['model_id']}]: ").strip() or default["model_id"]
    model = next((item for item in choices if item["id"] == selected_model), None)
    if model is None:
        raise ValueError(f"model {selected_model} is not available for role {resolved_role}")
    selected_effort = input(f"Effort [{default['effort']}] ({', '.join(model['efforts'])}): ").strip() or default["effort"]
    return select_for_task(
        config, task_id, resolved_role, tags=tags, model_id=selected_model, effort=selected_effort,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--list", action="store_true", dest="list_models")
    parser.add_argument("--role", choices=ROLES)
    parser.add_argument("--model")
    parser.add_argument("--effort", choices=EFFORTS)
    parser.add_argument("--task-id")
    parser.add_argument("--tags", default="", help="comma-separated task tags")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args(argv)
    if not args.list_models and not args.role and not args.task_id:
        parser.error("choose --list, --role, or --task-id")
    if args.list_models and any((args.role, args.model, args.effort, args.task_id, args.tags, args.interactive)):
        parser.error("--list cannot be combined with a route selection")
    if args.interactive and not args.task_id:
        parser.error("--interactive requires --task-id")
    if args.tags and not args.task_id:
        parser.error("--tags requires --task-id")
    try:
        config = load_config(args.config)
        tags = [normalize_tag(tag) for tag in args.tags.split(",") if normalize_tag(tag)]
        if args.list_models:
            result = {"models": roster(config)}
        elif args.interactive:
            result = interactive_select(config, args.task_id, args.role, tags)
        elif args.task_id:
            result = select_for_task(
                config, args.task_id, args.role, tags=tags,
                model_id=args.model, effort=args.effort,
            )
        else:
            result = select_route(config, args.role, model_id=args.model, effort=args.effort)
    except (EOFError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
