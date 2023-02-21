<template>
  <q-page class="row q-mx-xl">
    <div class="col-12 col-md-6 col-lg-4">
    <h1>Register</h1>
    <form @submit.prevent="register">
    <q-input
      v-model="username"
      label="Username"
      type="text"
      :rules="[val => !!val || 'Username is required']"
    />
    <q-input
      v-model="email"
      label="Email"
      type="email"
      :rules="[val => !!val || 'Email is required']"
    />
    <q-input
      v-model="password"
      label="Password"
      type="password"
      :rules="[val => !!val || 'Password is required']"
    />
    <q-input
      v-model="password2"
      label="Confirm Password"
      type="password"
      :rules="[val => !!val || 'Password is required']"
    />
    <q-btn type="submit" color="primary" label="Register" no-caps class="full-width q-my-md" />
  </form>
  <p class="text-blue-grey-4 q-pa-md">Have an account ? <q-btn class="q-ma-xs q-pa-xs" flat color="primary" :to="{name:'login'}" no-caps>Log in</q-btn></p>
  </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from 'src/stores/auth';

export default defineComponent({
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      errors: {}
    };
  },
  setup() {
    const authStore = useAuthStore();
    return {
      authStore
    };
  },
  methods: {
    async register() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:8000/api/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2
        });
        console.log(response.data);
        this.authStore.login();
      } catch (error) {
        console.log(error);
      }
    }
  }
});
</script>
