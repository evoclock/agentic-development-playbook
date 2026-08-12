/// <reference path="./model-router/node-shims.d.ts" />

import { readFileSync } from "node:fs";
import { join } from "node:path";
import type { Api, Model } from "@earendil-works/pi-ai";
import type { ThinkingLevel } from "@earendil-works/pi-agent-core";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import {
  EFFORTS,
  ROUTES,
  compatibleEfforts,
  modelKey,
  normalizeTags,
  roleForTags,
  taskTagsFromRegister,
  type RouteEffort,
  type RouteRole,
} from "./model-router/logic.ts";

const ROUTER_CONFIG = [".github", "skills", "model-routing", "models.json"];
const TASK_REGISTER = "TASKS.md";
const STATE_TYPE = "model-router";

type PiModel = Model<Api>;

type RoleAssignment = {
  model: string;
  effort: RouteEffort;
};

type ActiveRoute = {
  taskId?: string;
  role: RouteRole;
  tags: string[];
};

type RouterState = {
  assignments: Partial<Record<RouteRole, RoleAssignment>>;
  active?: ActiveRoute;
};

type RouterSessionEntry = {
  type: string;
  customType?: string;
  data?: unknown;
};

function roleLabel(role: RouteRole): string {
  return role.charAt(0).toUpperCase() + role.slice(1);
}

function modelLabel(model: PiModel): string {
  const key = modelKey(model);
  return model.name && model.name !== model.id ? `${key} — ${model.name}` : key;
}

function loadTagRoles(cwd: string): Map<string, RouteRole> {
  const path = join(cwd, ...ROUTER_CONFIG);
  try {
    const config = JSON.parse(readFileSync(path, "utf8")) as {
      tag_routes?: Array<{ tag?: unknown; role?: unknown }>;
    };
    const result = new Map<string, RouteRole>();
    for (const route of config.tag_routes ?? []) {
      const tag = typeof route.tag === "string" ? normalizeTags(route.tag)[0] : undefined;
      if (tag && ROUTES.includes(route.role as RouteRole) && !result.has(tag)) {
        result.set(tag, route.role as RouteRole);
      }
    }
    return result;
  } catch {
    return new Map();
  }
}

function loadTaskTags(cwd: string, taskId: string): string[] | undefined {
  try {
    const path = join(cwd, TASK_REGISTER);
    return taskTagsFromRegister(readFileSync(path, "utf8"), taskId);
  } catch {
    return undefined;
  }
}

function latestState(ctx: ExtensionContext): RouterState | undefined {
  const entries = ctx.sessionManager.getBranch() as RouterSessionEntry[];
  for (let i = entries.length - 1; i >= 0; i -= 1) {
    const entry = entries[i];
    if (entry.type !== "custom" || entry.customType !== STATE_TYPE) continue;
    const data = entry.data as Partial<RouterState> | undefined;
    if (!data || typeof data !== "object" || !data.assignments) continue;
    return {
      assignments: data.assignments,
      active: data.active,
    };
  }
  return undefined;
}

export default function modelRouterExtension(pi: ExtensionAPI): void {
  let assignments: Partial<Record<RouteRole, RoleAssignment>> = {};
  let active: ActiveRoute | undefined;
  let tagRoles = new Map<string, RouteRole>();

  function persistState(): void {
    const state: RouterState = { assignments, active };
    pi.appendEntry(STATE_TYPE, state);
  }

  function updateStatus(ctx: ExtensionContext): void {
    if (active) {
      const route = assignments[active.role];
      const model = route?.model.split("/").slice(1).join("/") ?? "unconfigured";
      ctx.ui.setStatus(
        "model-router",
        `router:${active.role} ${model} (${route?.effort ?? "?"})`,
      );
      return;
    }
    const configured = ROUTES.filter((role) => assignments[role]).length;
    ctx.ui.setStatus("model-router", configured > 0 ? `router:${configured}/3 configured` : undefined);
  }

  function availableModels(ctx: ExtensionContext): PiModel[] {
    return ctx.modelRegistry.getAvailable();
  }

  function ensureAssignment(
    role: RouteRole,
    models: readonly PiModel[],
    ctx: ExtensionContext,
  ): RoleAssignment | undefined {
    const existing = assignments[role];
    const existingModel = existing
      ? models.find((model) => modelKey(model) === existing.model)
      : undefined;
    if (existing && existingModel && compatibleEfforts(existingModel).includes(existing.effort)) {
      return existing;
    }

    const current = ctx.model ? models.find((model) => modelKey(model) === modelKey(ctx.model!)) : undefined;
    const fallback = current ?? models[0];
    if (!fallback) return undefined;
    const efforts = compatibleEfforts(fallback);
    const currentEffort = ctx.model && modelKey(ctx.model) === modelKey(fallback)
      ? (ctx.thinkingLevel as RouteEffort)
      : undefined;
    const assignment = {
      model: modelKey(fallback),
      effort: currentEffort && efforts.includes(currentEffort) ? currentEffort : efforts[0],
    };
    assignments[role] = assignment;
    return assignment;
  }

  async function configure(ctx: ExtensionContext): Promise<void> {
    if (ctx.mode !== "tui") {
      ctx.ui.notify("/router requires TUI mode", "error");
      return;
    }

    const models = availableModels(ctx);
    if (models.length === 0) {
      ctx.ui.notify("No authenticated models are available to configure", "error");
      return;
    }

    const next: Partial<Record<RouteRole, RoleAssignment>> = { ...assignments };
    for (const role of ROUTES) {
      const current = next[role];
      const orderedModels = [...models].sort((left, right) => {
        const leftCurrent = modelKey(left) === current?.model ? 0 : 1;
        const rightCurrent = modelKey(right) === current?.model ? 0 : 1;
        return leftCurrent - rightCurrent || modelLabel(left).localeCompare(modelLabel(right));
      });
      const modelOptions = orderedModels.map(modelLabel);
      const selectedModelLabel = await ctx.ui.select(
        `${roleLabel(role)} model`,
        modelOptions,
      );
      if (!selectedModelLabel) {
        ctx.ui.notify("Router configuration cancelled", "info");
        return;
      }
      const selectedModel = orderedModels.find((model) => modelLabel(model) === selectedModelLabel);
      if (!selectedModel) return;

      const efforts = compatibleEfforts(selectedModel);
      const currentEffort = current?.model === modelKey(selectedModel) && efforts.includes(current.effort)
        ? current.effort
        : efforts[0];
      const orderedEfforts = [currentEffort, ...efforts.filter((effort) => effort !== currentEffort)];
      const selectedEffort = await ctx.ui.select(
        `${roleLabel(role)} effort for ${modelKey(selectedModel)}`,
        orderedEfforts,
      );
      if (!selectedEffort || !EFFORTS.includes(selectedEffort as RouteEffort)) {
        ctx.ui.notify("Router configuration cancelled", "info");
        return;
      }
      next[role] = {
        model: modelKey(selectedModel),
        effort: selectedEffort as RouteEffort,
      };
    }

    assignments = next;
    persistState();
    updateStatus(ctx);
    ctx.ui.notify("Configured implementation, planning, and review routes", "info");
  }

  function show(ctx: ExtensionContext): void {
    const lines = ROUTES.map((role) => {
      const assignment = assignments[role];
      return `${role}: ${assignment ? `${assignment.model} (${assignment.effort})` : "(unconfigured)"}`;
    });
    if (active) {
      lines.push(`active: ${active.role}${active.taskId ? ` for ${active.taskId}` : ""}${active.tags.length ? ` [${active.tags.join(", ")}]` : ""}`);
    }
    ctx.ui.notify(lines.join("\n"), "info");
  }

  async function useRole(ctx: ExtensionContext, role: RouteRole, taskId?: string, tags: string[] = []): Promise<void> {
    const models = availableModels(ctx);
    const assignment = ensureAssignment(role, models, ctx);
    if (!assignment) {
      ctx.ui.notify("No available model can be assigned; use /router first", "error");
      return;
    }
    const model = models.find((candidate) => modelKey(candidate) === assignment.model);
    if (!model) {
      ctx.ui.notify(`Assigned model is unavailable: ${assignment.model}`, "error");
      return;
    }

    const success = await pi.setModel(model);
    if (!success) {
      ctx.ui.notify(`Pi could not activate ${assignment.model}`, "error");
      return;
    }
    pi.setThinkingLevel(assignment.effort as ThinkingLevel);
    active = { role, taskId, tags };
    persistState();
    updateStatus(ctx);
    ctx.ui.notify(
      `${roleLabel(role)} route active: ${assignment.model} (${assignment.effort})${taskId ? ` for ${taskId}` : ""}`,
      "info",
    );
  }

  function usage(ctx: ExtensionContext): void {
    ctx.ui.notify(
      "/router — configure all roles\n/router show\n/router use <implementation|planning|review>\n/router task <task-id> [optional tags]\n\nTask tags are read from TASKS.md and mapped through .github/skills/model-routing/models.json.",
      "info",
    );
  }

  pi.registerCommand("router", {
    description: "Configure and activate implementation, planning, and review model routes",
    getArgumentCompletions: (prefix) => {
      const options = ["configure", "show", "use", "task", ...ROUTES];
      const matches = options
        .filter((option) => option.startsWith(prefix.trim()))
        .map((value) => ({ value, label: value }));
      return matches.length > 0 ? matches : null;
    },
    handler: async (args, ctx) => {
      tagRoles = loadTagRoles(ctx.cwd);
      const input = args.trim();
      if (!input || input === "configure") {
        await configure(ctx);
        return;
      }
      if (input === "show") {
        show(ctx);
        return;
      }

      const [command, value, ...rest] = input.split(/\s+/);
      if (command === "use" || (ROUTES as readonly string[]).includes(command)) {
        const role = (command === "use" ? value : command) as RouteRole;
        if (!(ROUTES as readonly string[]).includes(role)) {
          usage(ctx);
          return;
        }
        await useRole(ctx, role, undefined, normalizeTags(rest.join(" ")));
        return;
      }
      if (command === "task") {
        if (!value) {
          usage(ctx);
          return;
        }

        const taskTags = loadTaskTags(ctx.cwd, value);
        if (taskTags === undefined) {
          ctx.ui.notify(`Task ${value} was not found in ${TASK_REGISTER}`, "error");
          return;
        }

        const suppliedTags = normalizeTags(rest.join(" "));
        const taskRole = roleForTags(taskTags, tagRoles);
        const suppliedRole = roleForTags(suppliedTags, tagRoles);
        if (taskRole && suppliedRole && taskRole !== suppliedRole) {
          ctx.ui.notify(
            `Task tags select ${taskRole}; supplied tags select ${suppliedRole}. Resolve the conflict in ${TASK_REGISTER}.`,
            "error",
          );
          return;
        }

        const tags = normalizeTags([...taskTags, ...suppliedTags].join(" "));
        const role = taskRole ?? suppliedRole;
        if (!role) {
          ctx.ui.notify(`Task ${value} has no mapped routing tag in ${TASK_REGISTER}`, "error");
          return;
        }
        await useRole(ctx, role, value, tags);
        return;
      }
      usage(ctx);
    },
  });

  pi.on("session_start", async (_event, ctx) => {
    tagRoles = loadTagRoles(ctx.cwd);
    const state = latestState(ctx);
    if (state) {
      assignments = state.assignments;
      active = state.active;
    }
    updateStatus(ctx);
  });

  pi.on("session_tree", async (_event, ctx) => {
    const state = latestState(ctx);
    assignments = state?.assignments ?? {};
    active = state?.active;
    updateStatus(ctx);
  });

  pi.on("model_select", async (event, ctx) => {
    if (!active) return;
    const assignment = assignments[active.role];
    if (assignment && assignment.model !== modelKey(event.model)) {
      active = undefined;
      updateStatus(ctx);
      ctx.ui.notify("Active router role cleared because the model changed outside /router", "warning");
    }
  });

  pi.on("before_agent_start", async (event) => {
    if (!active) return;
    const assignment = assignments[active.role];
    if (!assignment) return;
    const tags = active.tags.length > 0 ? active.tags.join(", ") : "(none)";
    return {
      systemPrompt: `${event.systemPrompt}\n\n[MODEL ROUTER]\nActive task: ${active.taskId ?? "(session task)"}\nRole: ${active.role}\nTags: ${tags}\nConfigured route: ${assignment.model} at ${assignment.effort} effort. Treat this as routing context; do not change roles without the user's direction.`,
    };
  });
}
