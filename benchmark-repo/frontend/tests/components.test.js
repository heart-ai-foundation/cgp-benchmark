import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const testDir = path.dirname(fileURLToPath(import.meta.url));

async function importJsx(relativePath) {
  const source = await readFile(path.join(testDir, relativePath), "utf8");
  return import(`data:text/javascript,${encodeURIComponent(source)}`);
}

test("renderUserList prints names and email addresses", async () => {
  const { renderUserList } = await importJsx("../src/components/UserList.jsx");
  assert.equal(
    renderUserList([{ name: "Ada", email: "ada@example.com" }]),
    "Ada <ada@example.com>"
  );
});

test("renderItemList joins item names", async () => {
  const { renderItemList } = await importJsx("../src/components/ItemList.jsx");
  assert.equal(renderItemList([{ name: "Notebook" }, { name: "Pen" }]), "Notebook, Pen");
});

test("submitLogin delegates valid credentials", async () => {
  const { submitLogin } = await importJsx("../src/components/LoginForm.jsx");
  const result = submitLogin(
    { email: "ada@example.com", password: "secret" },
    (payload) => ({ ok: true, payload })
  );

  assert.equal(result.ok, true);
  assert.equal(result.payload.email, "ada@example.com");
});
