/// <reference path="./node-shims.d.ts" />

import assert from "node:assert/strict";
import test from "node:test";
import {
  compatibleEfforts,
  modelKey,
  normalizeTags,
  roleForTags,
  taskTagsFromRegister,
  type ModelLike,
} from "./logic.ts";

const reasoningModel: ModelLike = {
  provider: "test",
  id: "reasoning",
  name: "Reasoning",
  reasoning: true,
  thinkingLevelMap: { xhigh: "xhigh", max: "max" },
};

const plainModel: ModelLike = {
  provider: "test",
  id: "plain",
  name: "Plain",
  reasoning: false,
};

test("model keys preserve provider and model id", () => {
  assert.equal(modelKey(reasoningModel), "test/reasoning");
});

test("effort choices follow model reasoning support", () => {
  assert.deepEqual(compatibleEfforts(plainModel), ["off"]);
  assert.deepEqual(compatibleEfforts(reasoningModel), [
    "off", "minimal", "low", "medium", "high", "xhigh", "max",
  ]);
});

test("tags are normalized and mapped to the first configured role", () => {
  assert.deepEqual(normalizeTags(" #Ambiguous,python ambiguous "), ["ambiguous", "python"]);
  const roles = new Map([["ambiguous", "planning" as const], ["review", "review" as const]]);
  assert.equal(roleForTags(["python", "#ambiguous"], roles), "planning");
});

test("task register rows provide hash tags without creating a second board", () => {
  const register = "| `ROUTER-REVIEW-001` | Review a diff | `#reviewer #security` |\n";
  assert.deepEqual(taskTagsFromRegister(register, "ROUTER-REVIEW-001"), ["reviewer", "security"]);
  assert.equal(taskTagsFromRegister(register, "MISSING"), undefined);
});
