export const ROUTES = ["implementation", "planning", "review"] as const;
export type RouteRole = (typeof ROUTES)[number];

export const EFFORTS = ["off", "minimal", "low", "medium", "high", "xhigh", "max"] as const;
export type RouteEffort = (typeof EFFORTS)[number];

export interface ModelLike {
  provider: string;
  id: string;
  name: string;
  reasoning: boolean;
  thinkingLevelMap?: Partial<Record<RouteEffort, string | null>>;
}

export function modelKey(model: Pick<ModelLike, "provider" | "id">): string {
  return `${model.provider}/${model.id}`;
}

export function compatibleEfforts(model: ModelLike): RouteEffort[] {
  if (!model.reasoning) return ["off"];

  const standard = EFFORTS.slice(0, 5).filter(
    (effort) => model.thinkingLevelMap?.[effort] !== null,
  );
  const extended = EFFORTS.slice(5).filter(
    (effort) => Object.prototype.hasOwnProperty.call(model.thinkingLevelMap ?? {}, effort)
      && model.thinkingLevelMap?.[effort] !== null,
  );
  return [...standard, ...extended];
}

export function normalizeTag(value: string): string {
  return value.trim().replace(/^#+/, "").toLowerCase();
}

export function roleForTags(
  tags: readonly string[],
  tagRoles: ReadonlyMap<string, RouteRole>,
): RouteRole | undefined {
  return tags
    .map(normalizeTag)
    .filter(Boolean)
    .map((tag) => tagRoles.get(tag))
    .find((role): role is RouteRole => role !== undefined);
}

export function normalizeTags(value: string): string[] {
  return [...new Set(value.split(/[\s,]+/).map(normalizeTag).filter(Boolean))];
}

export function taskTagsFromRegister(content: string, taskId: string): string[] | undefined {
  const wanted = taskId.trim();
  if (!wanted) return undefined;

  const row = content.split(/\r?\n/).find((line) => {
    if (!line.includes("|")) return false;
    const cells = line.split("|").slice(1).map((cell) => cell.trim());
    const firstCell = cells[0]?.replace(/^`|`$/g, "");
    return firstCell === wanted;
  });
  if (!row) return undefined;

  const hashTags = row.match(/#[A-Za-z0-9][A-Za-z0-9_-]*/g) ?? [];
  return normalizeTags(hashTags.join(" "));
}
