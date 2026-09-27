<script lang="ts" setup>
import type { VbenFormSchema } from '@vben/common-ui';
import type { Recordable } from '@vben/types';

import { computed, onActivated, ref } from 'vue';

import { AuthenticationLogin, z } from '@vben/common-ui';
import { $t } from '@vben/locales';

import { isRegistrationEnabled } from '#/api/core/auth';
import { isQrLoginEnabled } from '#/api/core/qr-login';
import { UnifiedCaptcha as UnifiedCaptchaComponent } from '#/components';
import { createCaptchaPorts } from '#/services/captcha/ports';
import { isMobileWeb } from '#/services/qr-login';
import { useAuthStore } from '#/store';

import SocialLoginOptions from './social-login-options.vue';

defineOptions({ name: 'Login' });

const authStore = useAuthStore();
const captchaRef = ref<InstanceType<typeof UnifiedCaptchaComponent>>();
const captchaPorts = createCaptchaPorts();
const showRegister = ref(false);
const showQrLogin = ref(false);

onActivated(async () => {
  showRegister.value = false;
  showRegister.value = await isRegistrationEnabled();
  showQrLogin.value = false;
  if (!isMobileWeb()) {
    // 配置请求失败时入口保持关闭，请求层已呈现错误。
    showQrLogin.value = await isQrLoginEnabled().catch(() => false);
  }
});

const formSchema = computed((): VbenFormSchema[] => {
  return [
    {
      component: 'VbenInput',
      componentProps: {
        placeholder: $t('authentication.usernameTip'),
      },
      fieldName: 'username',
      label: $t('authentication.username'),
      rules: z.string().min(1, { message: $t('authentication.usernameTip') }),
    },
    {
      component: 'VbenInputPassword',
      componentProps: {
        placeholder: $t('authentication.password'),
      },
      fieldName: 'password',
      label: $t('authentication.password'),
      rules: z.string().min(1, { message: $t('authentication.passwordTip') }),
    },
  ];
});

/**
 * 提交前先完成人机验证：后端验证码关闭时 acquire 立即返回 null，
 * 开启时弹出对话框，通过后将 verification 凭证随登录参数提交。
 */
async function handleSubmit(values: Recordable<any>) {
  const credentials = { username: values.username, password: values.password };
  let verification;
  try {
    verification = await captchaRef.value?.verify();
  } catch {
    // 验证码弹窗统一呈现失败；取消验证时中止登录。
    return;
  }
  await authStore.authLogin({
    ...credentials,
    verification: verification?.verification,
  });
}
</script>

<template>
  <div>
    <AuthenticationLogin
      :form-schema="formSchema"
      :loading="authStore.loginLoading"
      :show-register="showRegister"
      :show-qrcode-login="showQrLogin"
      @submit="handleSubmit"
    >
      <template #third-party-login>
        <SocialLoginOptions :disabled="authStore.loginLoading" />
      </template>
    </AuthenticationLogin>
    <UnifiedCaptchaComponent
      ref="captchaRef"
      :ports="captchaPorts"
      purpose="login"
      mode="dialog"
    />
  </div>
</template>
