// Cross-platform runner for examples/ smoke tests.
// Walks examples/*/tests/test_smoke.py, runs pytest in each.
import { readdirSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const examplesDir = fileURLToPath(new URL('../examples/', import.meta.url));
const dirs = readdirSync(examplesDir, { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name);

// 跨平台 Python 命令：Windows 用 `python`，Linux/macOS 用 `python3`
const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

let failed = 0;
for (const name of dirs) {
  const testFile = join(examplesDir, name, 'tests', 'test_smoke.py');
  if (!existsSync(testFile)) continue;
  console.log(`\n[smoke] ${name}`);
  const r = spawnSync(pythonCmd, ['-m', 'pytest', 'tests/', '-q'], {
    cwd: join(examplesDir, name),
    stdio: 'inherit',
    shell: true,
  });
  if (r.status !== 0) failed += 1;
}

if (failed > 0) {
  console.error(`\n${failed} example(s) failed smoke tests`);
  process.exit(1);
}
console.log('\nAll example smoke tests passed');
