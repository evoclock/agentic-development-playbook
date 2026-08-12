/// <reference path="./model-router/node-shims.d.ts" />

import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

const LOG = "state/reconciliation-log.v1.jsonl";
const TASKS = "TASKS.md";
const HANDOVER = "HANDOVER.md";

export function writeLike(event: any): boolean {
  if (event?.toolName === "edit" || event?.toolName === "write") return true;
  if (event?.toolName === "bash") {
    const command = event.input?.command;
    return typeof command === "string" && /(?:>|>>|tee\b|cp\b|mv\b|rm\b|mkdir\b|touch\b|python(?:3)?\b|node\b|sed\s+-i\b)/.test(command);
  }
  if (event?.toolName === "ipython") {
    const code = event.input?.code ?? event.input?.command ?? event.input?.input;
    return typeof code === "string" && /(?:write_text|write_bytes|open\s*\([^)]*,\s*["'](?:w|a|x|r\+)|to_csv|to_json|savefig|writefile|os\.(?:remove|rename|mkdir|makedirs)|shutil\.(?:copy|move|rmtree)|!\s*(?:cp|mv|rm|mkdir|touch)\b)/s.test(code);
  }
  return false;
}

function notify(ctx: ExtensionContext, text: string, type: "info" | "warning" = "info") {
  if (ctx.hasUI) ctx.ui.notify(text, type);
}

function reconcile(ctx: ExtensionContext, toolName: string) {
  try {
    if (!existsSync(join(ctx.cwd, TASKS))) return;
    const taskHash = Buffer.from(readFileSync(join(ctx.cwd, TASKS))).toString("base64").slice(0, 32);
    const record = {
      schema: "playbook.post-write-reconciliation.v1",
      event: "post_write",
      tool: toolName,
      task_file: TASKS,
      handover_file: HANDOVER,
      task_observation: taskHash,
      board_mutation: false,
      recorded_at: new Date().toISOString(),
    };
    mkdirSync(join(ctx.cwd, "state"), { recursive: true });
    appendFileSync(join(ctx.cwd, LOG), JSON.stringify(record) + "\n");
  } catch (error) {
    notify(ctx, `Post-write reconciliation unavailable; completed write preserved: ${error}`, "warning");
  }
}

export default function reliabilityWatchdog(pi: ExtensionAPI) {
  let lastStatus = "READY";
  pi.registerCommand("reliability", {
    description: "Show the local reliability watchdog status",
    handler: async (_args, ctx) => {
      const text = [
        "Reliability watchdog",
        "  Harness: Pi-compatible",
        `  Status: ${lastStatus}`,
        "  Retrigger: off",
        "  Recovery: supervised",
        "  Board mutation: off",
      ].join("\n");
      notify(ctx, text);
    },
  });
  pi.on("session_start", async (_event, ctx) => {
    lastStatus = "READY";
    notify(ctx, "Reliability watchdog loaded; supervised recovery active");
  });
  pi.on("tool_execution_end", async (event, ctx) => {
    if (event.isError === true || !writeLike(event)) return;
    reconcile(ctx, event.toolName);
  });
  pi.on("turn_end", async (event, ctx) => {
    const status = event.message && "stopReason" in event.message ? event.message.stopReason : undefined;
    if (status === "aborted" || status === "error") {
      lastStatus = "REVIEW_REQUIRED";
      notify(ctx, `Turn ${status}; split the task into one bounded step. Automatic retrigger is disabled.`, "warning");
    }
  });
}
