<script lang="ts" setup>
import type { QrLoginStatus, QrLoginTicket } from '#/api/core/qr-login';

import {
  computed,
  onActivated,
  onBeforeUnmount,
  onDeactivated,
  onMounted,
  ref,
} from 'vue';
import { useRouter } from 'vue-router';

import { LOGIN_PATH } from '@vben/constants';

import { useQRCode } from '@vueuse/integrations/useQRCode';
import { ElButton } from 'element-plus';

import {
  cancelQrLogin,
  createQrLogin,
  isQrLoginEnabled,
  pollQrLogin,
} from '#/api/core/qr-login';
import { notifyError } from '#/api/error-feedback';
import { $t } from '#/locales';
import { isMobileWeb, qrLoginUrl } from '#/services/qr-login';
import { useAuthStore } from '#/store';

defineOptions({ name: 'QrCodeLogin' });
const router = useRouter();
const auth = useAuthStore();
const ticket = ref<QrLoginTicket>();
const status = ref<'idle' | QrLoginStatus>('idle');
const loading = ref(false);
const enabled = ref(false);
const now = ref(Date.now());
let active = false;
let generation = 0;
let timer: ReturnType<typeof setTimeout> | undefined;
let clock: ReturnType<typeof setInterval> | undefined;
let pollAbort: AbortController | undefined;

const url = computed(() =>
  ticket.value
    ? qrLoginUrl(
        router.resolve({
          name: 'QrLoginScan',
          query: {
            ticket: ticket.value.ticket,
          },
        }).href,
      )
    : '',
);
const mobileAddress = computed(() =>
  url.value ? new URL(url.value) : undefined,
);
const loopback = computed(() =>
  ['127.0.0.1', '[::1]', 'localhost'].includes(
    mobileAddress.value?.hostname ?? '',
  ),
);
const qrcode = useQRCode(url, {
  errorCorrectionLevel: 'M',
  margin: 4,
  width: 280,
});
const remaining = computed(() =>
  ticket.value
    ? Math.max(0, Math.ceil((ticket.value.expiresAt - now.value) / 1000))
    : 0,
);
const showCode = computed(
  () => ticket.value && ['scanned', 'waiting'].includes(status.value),
);

function stop() {
  generation++;
  clearTimeout(timer);
  clearInterval(clock);
  pollAbort?.abort();
}

async function poll(current: QrLoginTicket, version: number) {
  if (!active || generation !== version) return;
  pollAbort = new AbortController();
  try {
    const result = await pollQrLogin(current.ticket, pollAbort.signal);
    if (!active || generation !== version) return;
    status.value = result.status;
    if (result.status === 'approved') {
      stop();
      try {
        await auth.authQrLogin(current.ticket);
      } catch (error) {
        status.value = 'idle';
        notifyError(error);
      }
      return;
    }
    if (['cancelled', 'expired'].includes(result.status)) {
      stop();
      return;
    }
    timer = setTimeout(() => poll(current, version), current.pollInterval);
  } catch (error) {
    if (generation !== version) return;
    stop();
    status.value = 'idle';
    notifyError(error);
  }
}

async function refresh() {
  if (loading.value || !enabled.value) return;
  stop();
  const version = generation;
  loading.value = true;
  status.value = 'idle';
  const previous = ticket.value;
  ticket.value = undefined;
  try {
    if (previous && previous.expiresAt > Date.now())
      await cancelQrLogin(previous.ticket);
    const created = await createQrLogin();
    if (!active || generation !== version) {
      await cancelQrLogin(created.ticket);
      return;
    }
    ticket.value = created;
    status.value = 'waiting';
    now.value = Date.now();
    clock = setInterval(() => {
      now.value = Date.now();
      if (!remaining.value) {
        status.value = 'expired';
        stop();
      }
    }, 1000);
    timer = setTimeout(() => poll(created, version), created.pollInterval);
  } catch (error) {
    notifyError(error);
  } finally {
    loading.value = false;
  }
}

async function activate() {
  if (active) return;
  active = true;
  try {
    if (isMobileWeb() || !(await isQrLoginEnabled())) {
      await router.replace(LOGIN_PATH);
      return;
    }
    enabled.value = true;
    await refresh();
  } catch (error) {
    notifyError(error);
  }
}

function deactivate() {
  active = false;
  stop();
}
onMounted(activate);
onActivated(activate);
onDeactivated(deactivate);
onBeforeUnmount(deactivate);
</script>

<template>
  <section class="mx-auto w-full max-w-sm text-center">
    <h1 class="mb-3 text-3xl font-semibold">{{ $t('qrLogin.title') }}</h1>
    <p class="text-muted-foreground mb-6">{{ $t('qrLogin.subtitle') }}</p>
    <div
      v-loading="loading || auth.loginLoading"
      class="border-border flex min-h-80 flex-col items-center justify-center rounded-xl border p-5"
    >
      <img
        v-if="showCode"
        :src="qrcode"
        :alt="$t('qrLogin.title')"
        class="h-64 w-64 rounded-lg bg-white"
      />
      <p class="mt-4 font-medium" role="status">
        {{ $t(`qrLogin.status.${status}`) }}
      </p>
      <p v-if="showCode" class="text-muted-foreground mt-2 text-sm">
        {{ $t('qrLogin.code') }}
        <strong class="text-foreground font-mono tracking-widest">{{
          ticket?.code
        }}</strong>
        · {{ $t('qrLogin.remaining', { seconds: remaining }) }}
      </p>
    </div>
    <p
      v-if="mobileAddress"
      class="text-muted-foreground mt-3 break-all text-sm"
    >
      {{ $t('qrLogin.mobileAddress', { address: mobileAddress.origin }) }}
    </p>
    <p v-if="loopback" class="mt-3 text-sm text-amber-600 dark:text-amber-400">
      {{ $t('qrLogin.loopback') }}
    </p>
    <ElButton
      class="mt-5 w-full"
      type="primary"
      :loading="loading"
      :disabled="!enabled"
      @click="refresh"
    >
      {{ $t('qrLogin.refresh') }}
    </ElButton>
    <ElButton
      class="!ml-0 mt-3 w-full"
      @click="
        router.push({
          path: LOGIN_PATH,
          query: router.currentRoute.value.query,
        })
      "
    >
      {{ $t('qrLogin.passwordLogin') }}
    </ElButton>
  </section>
</template>
