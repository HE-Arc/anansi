<template>
    <div>
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
        <q-btn type="submit" color="primary" label="Login" />
      </form>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      username: '',
      password: '',
      csrf: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:8000/api/login/', {
          username: this.username,
          password: this.password,
        },{
          //withCredentials: true,
          /*headers: {
            'X-CSRFToken': this.csrf
          }*/
        });

        console.log(response);

        const isLoggedIn = await this.$axios.get('http://127.0.0.1:8000/api/session', {
          withCredentials: true,
          /*headers: {
            'X-CSRFToken': this.csrf
            }*/
          });
        console.log(isLoggedIn);
      } catch (error) {
        console.log(error);
      }
    }
  },
  async mounted(){
    console.log('onMounted');
    //const response = await this.$axios.get('http://127.0.0.1:8000/api/csrf')
    //console.log(response);
    //this.csrf = response.data.csrfToken;
  }
});
</script>

