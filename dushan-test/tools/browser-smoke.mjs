import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { isAbsolute, join, relative, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = process.cwd();
const credentialsFile = resolve(process.env.DUSHAN_SMOKE_CREDENTIALS);
const within = relative(resolve(root, 'Temp'), credentialsFile);
assert.ok(within && !isAbsolute(within) && !within.startsWith('..'));
const credentials = JSON.parse(await readFile(credentialsFile, 'utf8'));
const origin = new URL(credentials.origin).origin;
const work = resolve(root, 'Temp', `browser-smoke-${Date.now()}`);
await mkdir(work, { recursive: true });
for (const name of ['TEMP', 'TMP', 'TMPDIR']) process.env[name] = work;
process.env.PLAYWRIGHT_BROWSERS_PATH = join(work, 'browser-cache');
const { chromium } = await import(
  pathToFileURL(process.env.PLAYWRIGHT_ENTRY).href
);
const errors = [];
const results = [];
let accessToken;
let menus = [];
const redact = (value) => {
  let text = String(value).replaceAll(credentials.admin, '[REDACTED]');
  if (accessToken) text = text.replaceAll(accessToken, '[REDACTED]');
  return text;
};
const context = await chromium.launchPersistentContext(join(work, 'profile'), {
  channel: process.env.DUSHAN_SMOKE_BROWSER || 'chrome',
  chromiumSandbox: true,
  headless: true,
  acceptDownloads: true,
  downloadsPath: join(work, 'downloads'),
  viewport: { width: 1600, height: 1000 },
});
try {
  const page = context.pages()[0];
  page.setDefaultTimeout(20_000);
  page.on('pageerror', (error) => errors.push(redact(error.message)));
  await page.goto(origin);
  await page.locator('input[type="password"]').waitFor();
  await page.locator('#__app-loading__').waitFor({ state: 'hidden' });
  await page.screenshot({ path: join(work, 'login.png'), fullPage: true });
  const inputs = await page.locator('input').evaluateAll((elements) =>
    elements.map((element) => ({
      name: element.name,
      type: element.type,
      placeholder: element.placeholder,
    })),
  );
  const named = page.locator('input[name="username"]');
  assert.equal(await named.count(), 1, JSON.stringify(inputs));
  await named.fill(credentials.admin_username);
  await page.locator('input[type="password"]').fill(credentials.admin);
  const [loginResponse, permissionResponse] = await Promise.all([
    page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname === '/admin-api/system/auth/login',
    ),
    page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname ===
        '/admin-api/system/auth/get-permission-info',
    ),
    page.getByRole('button', { name: 'login', exact: true }).click(),
  ]);
  const login = await loginResponse.json();
  assert.equal(login.code, 0, login.message);
  accessToken = login.data.accessToken;
  const permissionInfo = await permissionResponse.json();
  assert.equal(permissionInfo.code, 0);
  menus = permissionInfo.data.menus;
  const routePath = (url) =>
    url.hash.startsWith('#/') ? url.hash.slice(1) : url.pathname;
  await page.waitForURL((url) => !routePath(url).includes('/auth/'));
  await page.screenshot({ path: join(work, 'home.png'), fullPage: true });
  results.push({
    page: 'home',
    path: routePath(new URL(page.url())),
    title: await page.title(),
  });
  function find(nodes, component, parent = '') {
    for (const node of nodes) {
      const path = node.path.startsWith('/')
        ? node.path
        : `${parent}/${node.path}`;
      if (node.component === component) return path;
      const found = find(node.children || [], component, path);
      if (found) return found;
    }
  }
  const userPath = find(menus, 'system/user/index');
  assert.ok(userPath, '授权菜单必须包含用户管理');
  const userUrl = new URL(page.url());
  if (userUrl.hash.startsWith('#/')) userUrl.hash = userPath;
  else userUrl.pathname = userPath;
  const [users] = await Promise.all([
    page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname === '/admin-api/system/user/page',
    ),
    page.goto(userUrl.href),
  ]);
  assert.equal((await users.json()).code, 0);
  await page.locator('.vxe-table').first().waitFor({ state: 'visible' });
  await page.screenshot({ path: join(work, 'users.png'), fullPage: true });
  results.push({ page: 'users', path: userPath, tableVisible: true });
  assert.deepEqual(errors, []);
  await writeFile(
    join(work, 'result.json'),
    JSON.stringify({ results, errors }, null, 2),
  );
  process.stdout.write(JSON.stringify({ results, output: work }) + '\n');
} catch (error) {
  await writeFile(
    join(work, 'failure.json'),
    JSON.stringify(
      { message: redact(error.message), errors, results },
      null,
      2,
    ),
  );
  await writeFile(
    join(work, 'page.txt'),
    redact(await context.pages()[0].locator('body').innerText()),
  );
  await context
    .pages()[0]
    .screenshot({ path: join(work, 'failure.png'), fullPage: true });
  throw new Error(redact(error.message));
} finally {
  await context.close();
}
