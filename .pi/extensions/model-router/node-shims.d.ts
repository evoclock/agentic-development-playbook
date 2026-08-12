declare module "node:fs" {
  export function readFileSync(path: string, encoding: "utf8"): string;
  export function readFileSync(path: string, options: { encoding: "utf8" }): string;
}

declare module "node:path" {
  export function join(...paths: string[]): string;
}

declare module "@earendil-works/pi-ai" {
  export type Api = string;
  export interface Model<TApi extends Api = Api> {
    id: string;
    name: string;
    provider: string;
    reasoning: boolean;
    thinkingLevelMap?: Partial<Record<"off" | "minimal" | "low" | "medium" | "high" | "xhigh" | "max", string | null>>;
  }
}

declare module "@earendil-works/pi-agent-core" {
  export type ThinkingLevel = "off" | "minimal" | "low" | "medium" | "high" | "xhigh" | "max";
}

declare module "@earendil-works/pi-coding-agent" {
  import type { Api, Model } from "@earendil-works/pi-ai";
  import type { ThinkingLevel } from "@earendil-works/pi-agent-core";

  type PiModel = Model<Api>;
  type ExtensionEventArgs = {
    session_start: [event: unknown, ctx: ExtensionContext];
    session_tree: [event: unknown, ctx: ExtensionContext];
    model_select: [event: { model: PiModel }, ctx: ExtensionContext];
    before_agent_start: [event: { systemPrompt: string }, ctx: ExtensionContext];
  };

  export interface ExtensionContext {
    cwd: string;
    mode: "tui" | "rpc" | "json" | "print";
    model?: PiModel;
    thinkingLevel?: ThinkingLevel;
    modelRegistry: { getAvailable(): PiModel[] };
    sessionManager: { getBranch(): unknown[] };
    ui: {
      select(title: string, options: string[]): Promise<string | undefined>;
      notify(message: string, type?: "info" | "warning" | "error"): void;
      setStatus(key: string, text: string | undefined): void;
    };
  }

  export interface ExtensionAPI {
    appendEntry(type: string, data?: unknown): void;
    setModel(model: PiModel): Promise<boolean>;
    setThinkingLevel(level: ThinkingLevel): void;
    registerCommand(name: string, options: {
      description?: string;
      getArgumentCompletions?: (prefix: string) => Array<{ value: string; label: string }> | null;
      handler: (args: string, ctx: ExtensionContext) => Promise<void> | void;
    }): void;
    on<K extends keyof ExtensionEventArgs>(event: K, handler: (...args: ExtensionEventArgs[K]) => unknown): void;
  }
}

declare module "node:assert/strict" {
  interface StrictAssert {
    equal(actual: unknown, expected: unknown, message?: string): void;
    deepEqual(actual: unknown, expected: unknown, message?: string): void;
  }

  const assert: StrictAssert;
  export default assert;
}

declare module "node:test" {
  type TestFunction = () => void | Promise<void>;
  const test: (name: string, fn: TestFunction) => void;
  export default test;
}
