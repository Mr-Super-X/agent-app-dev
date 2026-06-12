// Cross-platform local link checker.
// Walks docs/**/*.md, checks internal links resolve to existing files.
// Supports both relative paths and VitePress site-root absolute paths (starting with `/`).
// Excludes paths matching VitePress srcExclude globs (e.g. `**/superpowers/**`).
// Uses forward slashes for fs.existsSync on Windows to avoid Node.js
// backslash + UTF-8 path issues.
import { readdirSync, statSync, readFileSync, existsSync } from 'node:fs';
import { join, dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const docsDir = fileURLToPath(new URL('../docs/', import.meta.url));
const docsDirFs = docsDir.split(sep).join('/');
const srcExcludeGlobs = ['**/superpowers/**'];

function toFs(p) {
  return p.split(sep).join('/');
}

function matchesExclude(relPath) {
  for (const g of srcExcludeGlobs) {
    const m = g.match(/^\*\*\/([^/]+)/);
    if (m && relPath.includes(`/${m[1]}/`)) return true;
  }
  return false;
}

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
let skipped = 0;

for (const file of walk(docsDir)) {
  const content = readFileSync(file, 'utf-8');
  const base = dirname(file);
  const baseFs = toFs(base);
  let m;
  while ((m = linkRe.exec(content)) !== null) {
    const target = m[2];
    if (target.startsWith('http') || target.startsWith('mailto:') || target.startsWith('#')) continue;
    checked += 1;
    const [pathPart] = target.split('#');
    let resolved;
    if (pathPart.startsWith('/')) {
      resolved = join(docsDir, pathPart.replace(/^\//, ''));
    } else {
      resolved = resolve(base, pathPart);
    }
    const resolvedFs = toFs(resolved);
    // srcExclude check: relative path with forward slashes
    const relToDocs = resolvedFs.startsWith(docsDirFs)
      ? resolvedFs.slice(docsDirFs.length + 1)
      : '';
    if (relToDocs.startsWith('superpowers/') || relToDocs.includes('/superpowers/')) { skipped += 1; continue; }
    if (!existsSync(resolvedFs)) {
      // DEBUG: try alternative paths
      const altPath = resolved;
      const existsAlt = existsSync(altPath);
      const utf8Test = resolvedFs.length + ' vs ' + altPath.length;
      console.error(`[link-check] BROKEN: ${file} → ${target}`);
      console.error(`[DEBUG] resolvedFs=${resolvedFs}`);
      console.error(`[DEBUG] resolvedAlt=${altPath} existsAlt=${existsAlt} ${utf8Test}`);
      failed += 1;
    }
  }
}

console.log(`\n[link-check] ${checked} link(s) checked, ${skipped} excluded, ${failed} broken`);
if (failed > 0) process.exit(1);
