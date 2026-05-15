import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const protocolRoot = path.join(root, "next-prompt-protocols");
const manifestPath = path.join(protocolRoot, "manifest.json");
const lockPath = path.join(protocolRoot, ".slice-lock.json");
const readmePath = path.join(protocolRoot, "README.md");

function readJson(filePath) {
  return JSON.parse(readFileSync(filePath, "utf8"));
}

function hashFile(filePath) {
  return `sha256:${createHash("sha256").update(readFileSync(filePath)).digest("hex")}`;
}

function extractObjective(markdown) {
  const match = markdown.match(/## Next objective\s+([\s\S]*?)(\n## |$)/);
  if (!match) {
    throw new Error("active protocol is missing a Next objective section");
  }
  return match[1].trim().replace(/\s+/g, " ");
}

function expectedLock(manifest) {
  const activePath = path.join(protocolRoot, manifest.active_protocol);
  const activeText = readFileSync(activePath, "utf8");
  return {
    lock_version: 1,
    project: manifest.project,
    current_commit: manifest.current_commit,
    current_phase: manifest.current_phase,
    active_protocol: manifest.active_protocol,
    active_protocol_sha256: hashFile(activePath),
    active_objective: extractObjective(activeText),
    allowed_files: manifest.allowed_files,
    verification: manifest.verification,
    stop_condition: manifest.stop_condition
  };
}

function expectedReadme(manifest) {
  return `# Next-Prompt Protocol Scaffold

Project: ${manifest.project}

Current phase: \`${manifest.current_phase}\`

Active protocol:

\`${manifest.active_protocol}\`

Run \`node next-prompt-protocols/tools/sync-protocols.mjs --check\` before executing or handing off a slice.
`;
}

function stableJson(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function main() {
  const check = process.argv.includes("--check");
  const manifest = readJson(manifestPath);
  const lock = expectedLock(manifest);
  const readme = expectedReadme(manifest);

  if (check) {
    const actualLock = readJson(lockPath);
    const actualReadme = readFileSync(readmePath, "utf8");
    const problems = [];

    if (stableJson(actualLock) !== stableJson(lock)) {
      problems.push(".slice-lock.json is stale");
    }
    if (actualReadme !== readme) {
      problems.push("next-prompt-protocols/README.md is stale");
    }
    if (problems.length > 0) {
      console.error(problems.join("\n"));
      process.exit(1);
    }
    console.log("protocol scaffold is synchronized");
    return;
  }

  writeFileSync(lockPath, stableJson(lock));
  writeFileSync(readmePath, readme);
  console.log("protocol scaffold synchronized");
}

main();
