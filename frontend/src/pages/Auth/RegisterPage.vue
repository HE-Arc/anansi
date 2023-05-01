<script setup>
import { defineComponent, ref, onMounted, getCurrentInstance } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/ErrorBanner.vue";
import { useRoute, useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const username = ref("");
const email = ref("");
const password = ref("");
const password2 = ref("");
const errors = ref([]);

const register = async () => {
  try {
    await api.post("register/", {
      username: username,
      email: email,
      password: password,
      password2: password2,
    });

    await api.post("login/", {
      username: username,
      password: password,
    });

    authStore.login();

    $q.notify({
      message: "You have successfully registered and logged in!",
      color: "positive",
    });

    router.push({ name: "home" });
  } catch (error) {
    errors.value = [];
    for (var key in error.response.data) {
      for (var key2 in error.response.data[key]) {
        errors.value.push(key + " : " + error.response.data[key][key2]);
      }
    }
  }
};
</script>
<template>
  <q-page class="row q-mx-xl">
    <div class="col-12 col-md-6 col-lg-4">
      <h1>Register</h1>
      <ErrorBanner :errors="errors" />
      <!-- Formulaire d'inscription -->
      <form @submit.prevent="register">
        <!-- Nom d'utilisateur -->
        <q-input
          v-model="username"
          label="Username"
          type="text"
          :rules="[(val) => !!val || 'Username is required']"
        />
        <!-- Email -->
        <q-input
          v-model="email"
          label="Email"
          type="email"
          :rules="[(val) => !!val || 'Email is required']"
        />
        <!-- Mot de passe -->
        <q-input
          v-model="password"
          label="Password"
          type="password"
          :rules="[(val) => !!val || 'Password is required']"
        />
        <!-- Confirmation du mot de passe -->
        <q-input
          v-model="password2"
          label="Confirm Password"
          type="password"
          :rules="[(val) => !!val || 'Password is required']"
        />
        <!-- Bouton d'inscription -->
        <q-btn
          type="submit"
          color="primary"
          label="Register"
          no-caps
          class="full-width q-my-md"
        />
      </form>
      <!-- Lien vers la page de connexion -->
      <p class="text-blue-grey-4 q-pa-md">
        Have an account ?
        <q-btn
          class="q-ma-xs q-pa-xs"
          flat
          color="primary"
          :to="{ name: 'login' }"
          no-caps
          >Log in</q-btn
        >
      </p>
    </div>
  </q-page>
</template>
