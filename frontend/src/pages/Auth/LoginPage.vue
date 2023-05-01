<script setup>
import { onMounted, getCurrentInstance, ref } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";
import ErrorBanner from "src/components/ErrorBanner.vue";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const username = ref("");
const password = ref("");
const errors = ref([]);

const login = async () => {
  try {
    const response = await api.post("login/", {
      username: username.value,
      password: password.value,
    });

    authStore.isLoggedIn = true;

    $q.notify({
      message: "Login successful",
      color: "positive",
    });

    router.push({ name: "home" });
  } catch (error) {
    console.log(error);
    errors.value = ["Check your credentials"];
  }
};
</script>

<template>
  <q-page class="row q-mx-xl">
    <div class="col-12 col-md-6 col-lg-4">
      <h1>Login</h1>
      <ErrorBanner :errors="errors" />
      <form @submit.prevent="login">
        <q-input
          v-model="username"
          label="Username"
          type="text"
          :rules="[(val) => !!val || 'Username is required']"
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          :rules="[(val) => !!val || 'Password is required']"
        />
        <q-btn
          type="submit"
          color="primary"
          label="Login"
          no-caps
          class="full-width q-my-md"
        />
      </form>
      <p class="text-blue-grey-4 q-pa-md">
        Doesn't have an account ?
        <q-btn
          class="q-ma-xs q-pa-xs"
          flat
          color="primary"
          :to="{ name: 'register' }"
          no-caps
          >Register</q-btn
        >
      </p>
    </div>
  </q-page>
</template>
