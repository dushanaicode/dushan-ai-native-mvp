import { createApp, h, nextTick, reactive } from 'vue';

import { afterEach, beforeEach, expect, it, vi } from 'vitest';

import SocialLoginOptions from '../../dushan-admin-frontend/apps/web-ele/src/views/_core/authentication/social-login-options.vue';

const stubs = vi.hoisted(() => ({ providers: vi.fn(), begin: vi.fn() }));
vi.mock('#/api/core/auth', () => ({ getSocialProvidersApi: stubs.providers }));
vi.mock('vue-router', () => ({
  useRoute: () => ({ query: { redirect: '/workbench' } }),
}));
vi.mock('@vben/locales', () => ({ $t: (key: string) => key }));
vi.mock(
  '../../dushan-admin-frontend/apps/web-ele/src/views/_core/authentication/social-oauth',
  async (original) => ({
    ...(await original<object>()),
    beginSocialOAuth: stubs.begin,
  }),
);
const cleanups: Array<() => void> = [];
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubEnv('VITE_APP_SOCIAL_LOGIN_ENABLE', 'true');
});
afterEach(() => {
  for (const close of cleanups.splice(0)) close();
  vi.unstubAllEnvs();
});
function mount() {
  const props = reactive({
    disabled: false,
  });
  const element = document.createElement('div');
  const app = createApp(() => h(SocialLoginOptions, props));
  app.mount(element);
  cleanups.push(() => app.unmount());
  return { props, element };
}

it('读取渠道并使用本站流程发起授权', async () => {
  stubs.providers.mockResolvedValue([
    {
      type: 20,
      source: 'DINGTALK',
      name: '钉钉',
      mode: 'browser',
      codeParameter: 'code',
    },
    {
      type: 30,
      source: 'WECHAT_ENTERPRISE',
      name: '企业微信',
      mode: 'browser',
      codeParameter: 'code',
    },
  ]);
  const { element } = mount();
  await vi.waitFor(() =>
    expect(element.querySelectorAll('button')).toHaveLength(2),
  );
  expect(element.textContent).toContain('钉钉');
  expect(element.textContent).toContain('企业微信');
  element
    .querySelector<HTMLButtonElement>('button[aria-label="钉钉"]')!
    .click();
  await vi.waitFor(() =>
    expect(stubs.begin).toHaveBeenCalledWith({
      type: 20,
      codeParameter: 'code',

      returnPath: '/workbench',
    }),
  );
});

it('关闭开关不查询、不渲染入口或错误', async () => {
  vi.stubEnv('VITE_APP_SOCIAL_LOGIN_ENABLE', 'false');
  const { props, element } = mount();
  await nextTick();
  await nextTick();
  expect(stubs.providers).not.toHaveBeenCalled();
  expect(element.textContent).toBe('');
});

it('禁用期间忽略旧请求的迟到响应，重新启用后重新查询', async () => {
  const pending = Promise.withResolvers<unknown[]>();
  stubs.providers.mockReturnValueOnce(pending.promise).mockResolvedValue([]);
  const { props, element } = mount();
  await nextTick();
  props.disabled = true;
  await nextTick();
  pending.resolve([
    {
      type: 20,
      name: 'old',
      source: 'DINGTALK',
      mode: 'browser',
      codeParameter: 'code',
    },
  ]);
  await nextTick();
  expect(element.querySelectorAll('button')).toHaveLength(0);
  props.disabled = false;
  await nextTick();
  expect(stubs.providers).toHaveBeenCalledTimes(2);
  expect(stubs.providers).toHaveBeenLastCalledWith();
});
