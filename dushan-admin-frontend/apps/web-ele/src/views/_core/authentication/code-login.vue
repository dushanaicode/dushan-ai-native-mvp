<script lang="ts" setup>
import type { VbenFormSchema } from '@vben/common-ui';
import type { Recordable } from '@vben/types';

import { computed, ref } from 'vue';

import { AuthenticationCodeLogin, z } from '@vben/common-ui';
import { $t } from '@vben/locales';

import { ElMessage } from 'element-plus';

import { sendLoginSmsApi } from '#/api/core/auth';
import { UnifiedCaptcha as UnifiedCaptchaComponent } from '#/components';
import { createCaptchaPorts } from '#/services/captcha/ports';
import { useAuthStore } from '#/store';

defineOptions({ name: 'CodeLogin' });

const authStore = useAuthStore();
const loginRef = ref<InstanceType<typeof AuthenticationCodeLogin>>();
const captchaRef = ref<InstanceType<typeof UnifiedCaptchaComponent>>();
const captchaPorts = createCaptchaPorts();
const sending = ref(false);
const codeLength = ref(4);

async function sendCode() {
  const login = loginRef.value;
  const captcha = captchaRef.value;
  if (!login || !captcha) throw new Error($t('smsLogin.checkFields'));
  const form = login.getFormApi();
  const fields = ['mobile'];
  for (const field of fields) {
    await form.validateField(field);
    if (!(await form.isFieldValid(field)))
      throw new Error($t('smsLogin.checkFields'));
  }
  const values = await form.getValues();
  const data = {
    mobile: values.mobile,
  };
  sending.value = true;
  try {
    const verification = await captcha.verify();
    codeLength.value = await sendLoginSmsApi({
      ...data,
      verification: verification?.verification,
    });
    form.setFieldValue('code', '');
    ElMessage.success($t('smsLogin.ready'));
  } finally {
    sending.value = false;
  }
}

const formSchema = computed((): VbenFormSchema[] => [
  {
    component: 'VbenInput',
    componentProps: {
      placeholder: $t('authentication.mobile'),
      autocomplete: 'tel',
    },
    fieldName: 'mobile',
    label: $t('authentication.mobile'),
    rules: z
      .string()
      .regex(/^1[3-9]\d{9}$/, { message: $t('authentication.mobileErrortip') }),
  },
  {
    component: 'VbenPinInput',
    componentProps: {
      codeLength: codeLength.value,
      disabled: authStore.loginLoading,
      loading: sending.value,
      createText: (countdown: number) =>
        countdown > 0
          ? $t('authentication.sendText', [countdown])
          : $t('authentication.sendCode'),
      handleSendCode: sendCode,
    },
    fieldName: 'code',
    label: $t('authentication.code'),
    rules: z.string().length(codeLength.value, {
      message: $t('authentication.codeTip', [codeLength.value]),
    }),
  },
]);

async function handleLogin(values: Recordable<any>) {
  if (sending.value) return;
  await authStore.authSmsLogin({
    mobile: values.mobile,
    code: values.code,
  });
}
</script>

<template>
  <div>
    <AuthenticationCodeLogin
      ref="loginRef"
      :form-schema="formSchema"
      :loading="authStore.loginLoading"
      @submit="handleLogin"
    />
    <UnifiedCaptchaComponent
      ref="captchaRef"
      :ports="captchaPorts"
      purpose="login"
      mode="dialog"
    />
  </div>
</template>
