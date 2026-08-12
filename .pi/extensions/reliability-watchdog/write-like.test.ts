/// <reference path="../model-router/node-shims.d.ts" />

import assert from "node:assert/strict";
import test from "node:test";
import { writeLike } from "../reliability-watchdog.ts";

test("detects Pi edit and write tool events", () => {
  assert.equal(writeLike({ toolName: "edit", input: {} }), true);
  assert.equal(writeLike({ toolName: "write", input: {} }), true);
});

test("detects write-like Bash commands without blocking read-only commands", () => {
  assert.equal(writeLike({ toolName: "bash", input: { command: "printf x > notes.txt" } }), true);
  assert.equal(writeLike({ toolName: "bash", input: { command: "rg router README.md" } }), false);
});

test("detects IPython-style file and artifact writes", () => {
  assert.equal(writeLike({ toolName: "ipython", input: { code: "Path('x').write_text('ok')" } }), true);
  assert.equal(writeLike({ toolName: "ipython", input: { code: "print('ok')" } }), false);
});
