<template>
  <q-page class="row q-mx-xl">
    <div class="col-12 col-md-6 col-lg-4">
      <h1>Register</h1>
      <ErrorBanner :errors="errors" />
      <form @submit.prevent="register">
        <q-input
          v-model="username"
          label="Username"
          type="text"
          :rules="[(val) => !!val || 'Username is required']"
        />
        <q-input
          v-model="email"
          label="Email"
          type="email"
          :rules="[(val) => !!val || 'Email is required']"
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          :rules="[(val) => !!val || 'Password is required']"
        />
        <q-input
          v-model="password2"
          label="Confirm Password"
          type="password"
          :rules="[(val) => !!val || 'Password is required']"
        />
        <q-btn
          type="submit"
          color="primary"
          label="Register"
          no-caps
          class="full-width q-my-md"
        />
      </form>
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

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/ErrorBanner.vue";

export default defineComponent({
  name: "RegisterPage",
  components: {
    ErrorBanner,
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      password2: "",
      errors: ref([]),
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
    async register() {
      try {
        const response = await this.$api.post("register/", {
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2,
        });

        this.authStore.login();

        console.log("response " + response);
        $q.notify({
          message: "You have successfully registered and logged in!",
          color: "positive",
        });

        this.$router.push({ name: "home" });
      } catch (error) {
        this.errors = [];
        for (var key in error.response.data) {
          for (var key2 in error.response.data[key]) {
            this.errors.push(key + " : " + error.response.data[key][key2]);
          }
        }
      }
    },
  },
  async mounted() {
    console.log("onMounted");
  },
});
</script>
