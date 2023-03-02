<template>
  <q-page class="row q-mx-xl">
    <div class="col-12 col-md-6 col-lg-4">
      <h1>Login</h1>
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

<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useQuasar } from "quasar";

export default defineComponent({
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  setup() {
    const authStore = useAuthStore();
    const $q = useQuasar();
    return {
      $q,
      authStore,
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$api.post("login/", {
          username: this.username,
          password: this.password,
        });

        console.log(response);

        const isLoggedIn = await this.$api.get("session", { withCredentials: true });
        console.log(isLoggedIn);
        this.authStore.login();

        this.$q.notify({
          message: "Login successful",
          color: "positive",
        });

        this.$router.push({ name: "home" });
      } catch (error) {
        console.log(error);
      }
    },
  },
  async mounted() {
    console.log("onMounted");
  },
});
</script>
