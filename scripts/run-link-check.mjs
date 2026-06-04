// Cross-platform local link checker.
// Walks docs/**/*.md, checks internal links resolve to existing files.
import { readdirSync, statSync, readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const docsDir = fileURLToPath(new URL('../docs/', import.meta.url));

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (name.endsWith('.md')) out.push(p);
  }
  return out;
}

const linkRe = /\[([^\]]*)\]\(([^)]+)\)/g;
let checked = 0;
let failed = 0;

for (const file of walk(docsDir)) {
  const content = readFileSync(file, 'utf-8');
  const base = dirname(file);
  let m;
  while ((m = linkRe.exec(content)) !== null) {
    const target = m[2];
    if (target.startsWith('http') || target.startsWith('mailto:') || target.startsWith('#')) continue;
    checked += 1;
    // Strip anchor
    const [path] = target.split('#');
    const resolved = join(base, path);
    if (!existsSync(resolved)) {
      console.error(`[link-check] BROKEN: ${file} → ${target}`);
      failed += 1;
    }
  }
}

console.log(`\n[link-check] ${checked} link(s) checked, ${failed} broken`);
if (failed > 0) process.exit(1);
