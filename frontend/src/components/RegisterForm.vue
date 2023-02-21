<template>
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
    <q-btn type="submit" color="primary" label="Register" />
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

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
      } catch (error) {
        console.log(error);
      }
    }
  }
});
</script>
