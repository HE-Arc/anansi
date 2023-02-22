<template>
  <q-page class="row q-mx-xl"> <!--class="row items-center justify-evenly">-->
    <div class="col-12 col-md-6 col-lg-4">
      <h1>Login</h1>
    <form @submit.prevent="login">
        <q-input
          v-model="username"
          label="Username"
          type="text"
          :rules="[val => !!val || 'Username is required']"
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          :rules="[val => !!val || 'Password is required']"
        />
        <q-btn type="submit" color="primary" label="Login" no-caps  class="full-width q-my-md" />
      </form>
      <p class="text-blue-grey-4 q-pa-md">Doesn't have an account ? <q-btn class="q-ma-xs q-pa-xs" flat color="primary" :to="{name:'register'}" no-caps>Register</q-btn></p>
    </div>
  </q-page>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { useAuthStore } from 'src/stores/auth';

  export default defineComponent({
    name: 'LoginPage',
    data() {
    return {
      username: '',
      password: '',
      csrf: '',
    };
  },
  setup() {
    const authStore = useAuthStore();
    return {
      authStore
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:8000/api/login/', {
          username: this.username,
          password: this.password,
        },{
          withCredentials: true,
          headers: {
            'X-CSRFToken': this.csrf
          }
        });

        console.log(response);

        const isLoggedIn = await this.$axios.get('http://127.0.0.1:8000/api/session', {
          withCredentials: true,
          /*headers: {
            'X-CSRFToken': this.csrf
            }*/
          });
        console.log(isLoggedIn);
        this.authStore.login();
      } catch (error) {
        console.log(error);
      }
    }
  },
  async mounted(){
    console.log('onMounted');
    const response = await this.$axios.get('http://127.0.0.1:8000/api/csrf')
    console.log(response);
    this.csrf = response.data.csrfToken;
  }
});
</script>
