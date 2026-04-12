<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import { useRoute, useRouter } from "nuxt/app";
import type { FormInstance, FormRules } from "element-plus";
import schoolLogo from "~/assets/image/school-logo-light.jpg";
const { $authService } = useNuxtApp();
const route = useRoute();
const router = useRouter();

const loading = ref(false);
const formRef = ref<FormInstance>();
definePageMeta({ layout: false, middleware: [] });
const form = reactive({
  token: "",
  new_password: "",
  confirm_password: "",
});

const tokenFromUrl = computed(() => String(route.query.token ?? "").trim());

onMounted(() => {
  // Auto-fill token from URL if present
  if (tokenFromUrl.value) form.token = tokenFromUrl.value;
});

const rules: FormRules = {
  token: [{ required: true, message: "Token is required", trigger: "blur" }],
  new_password: [
    { required: true, message: "Please enter new password", trigger: "blur" },
    {
      min: 6,
      message: "Password must be at least 6 characters",
      trigger: "blur",
    },
  ],
  confirm_password: [
    { required: true, message: "Please confirm password", trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value !== form.new_password)
          callback(new Error("Passwords do not match"));
        else callback();
      },
      trigger: "blur",
    },
  ],
};

const submit = async () => {
  if (loading.value) return;

  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  loading.value = true;
  try {
    const ok = await $authService.confirmResetPassword({
      token: form.token,
      new_password: form.new_password,
    });

    // Only redirect on success
    if (ok) {
      await router.push("/auth/login");
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
      <!-- Canvas must be client-only in Nuxt -->

  <Transition name="fade-slide" appear>
    <div class="auth-shell">
      <div class="auth-card">
        <div class="auth-logo-wrap">
          <img :src="schoolLogo" alt="HRM Logo" class="auth-logo" />
        </div>

        <div class="mb-4 text-center">
          <h2 class="auth-title">Reset Password</h2>
          <p class="auth-subtitle">
            Enter the reset token and choose a new password.
          </p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          class="text-left"
          @submit.prevent="submit"
        >
          <!-- Token -->
          <el-form-item label="Reset Token" prop="token" class="mb-8">
            <el-input
              v-model="form.token"
              placeholder="Paste token here"
              autocomplete="off"
              class="auth-input"
            />
          </el-form-item>

          <!-- New password -->
          <el-form-item label="New Password" prop="new_password" class="mb-8">
            <el-input
              v-model="form.new_password"
              type="password"
              placeholder="New password"
              autocomplete="new-password"
              show-password
              class="auth-input"
            />
          </el-form-item>

          <!-- Confirm -->
          <el-form-item
            label="Confirm Password"
            prop="confirm_password"
            class="mb-6"
          >
            <el-input
              v-model="form.confirm_password"
              type="password"
              placeholder="Confirm password"
              autocomplete="new-password"
              show-password
              class="auth-input"
              @keyup.enter="submit"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              native-type="submit"
              :loading="loading"
              :disabled="loading"
              class="auth-primary-btn w-full"
            >
              Update Password
            </el-button>
          </el-form-item>
        </el-form>

        <p class="auth-footer mt-4">
          Remember your password?
          <RouterLink to="/auth/login" class="auth-link"
            >Back to login</RouterLink
          >
        </p>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.page {
  min-height: 100vh;
  position: relative;
  isolation: isolate; /* keeps z-index layering predictable */
}

.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
}

/* “premium glass” card */
.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 28px;
  border-radius: 16px;

  background: color-mix(in srgb, rgba(255, 255, 255, 0.08) 70%, transparent);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);

  border: 1px solid rgba(255, 255, 255, 0.14);
  box-shadow:
    0 18px 55px rgba(0, 0, 0, 0.45),
    0 1px 0 rgba(255, 255, 255, 0.06) inset;

  color: var(--text-color, #e5e7eb);
}

.auth-logo-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.auth-logo {
  display: block;
  width: 175px;
  height: auto;
  border-radius: 14px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.20);
}

.auth-primary-btn {
  border-radius: 10px;
  font-weight: 650;
  background: var(--color-primary, #6366f1);
  color: #fff;
  border: 1px solid color-mix(in srgb, var(--color-primary, #6366f1) 80%, transparent);
  box-shadow: 0 10px 18px color-mix(in srgb, var(--color-primary, #6366f1) 18%, transparent);
  transition: transform 200ms ease, background 200ms ease;
}

.auth-primary-btn:hover {
  transform: translateY(-0.5px);
}

.auth-primary-btn:active {
  transform: translateY(0px);
}

.auth-link {
  color: #a5b4fc;
  font-weight: 600;
  text-decoration: none;
}
.auth-link:hover {
  text-decoration: underline;
}

/* Animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-16px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}
</style>