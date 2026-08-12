#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mode="${1:-plan}"
if [[ $# -gt 0 ]]; then shift; fi

case "$mode" in
  plan)
    tool_args=(--no-tools)
    ;;
  work)
    tool_args=(--tools read,bash,edit,write)
    ;;
  *)
    printf 'Usage: %s {plan|work} [prompt ...]\n' "$0" >&2
    exit 2
    ;;
esac

if [[ $# -eq 0 ]]; then
  set -- "Read the task and relevant runbook. State a bounded plan, acceptance checks, and stopping point. Do not edit files."
fi

exec pi --no-session "${tool_args[@]}" \
  --skill "$repo_root/.github/skills/pipeline-run-triage/SKILL.md" \
  "@$repo_root/AGENTS.md" \
  "@$repo_root/.github/copilot-instructions.md" \
  "@$repo_root/synthetic-project/DEMO-TICKET.md" \
  "$@"
