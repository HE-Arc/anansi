<template>
  <q-layout view="lHh Lpr lFf">
    <nav-bar />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import NavBar from './components/NavBar.vue';
import { useAuthStore } from './stores/auth';

export default defineComponent({
  name: 'App',
  components: {
    NavBar
  },
  setup() {
    const authStore = useAuthStore();
    return {
      authStore
    };
  },
  methods: {
    getSession() {
      fetch('/api/session')
        .then((response) => response.json())
        .then((data) => {
          data.isAuthenticated ? this.authStore.login() : this.authStore.logout();
        });
    }
  },
  onMounted: function() {
    this.getSession();
  }
});
</script>
