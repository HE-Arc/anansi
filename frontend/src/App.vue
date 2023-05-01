<script setup>
import { onMounted, getCurrentInstance } from "vue";
import NavBar from "./components/NavBar.vue";
import { useAuthStore } from "./stores/auth";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const authStore = useAuthStore();

const getSession = async () => {
  const response = await api.get(`session`);
  console.log(response.data);
  response.data.isAuthenticated ? authStore.login() : authStore.logout();
  //console.log(authStore.isLoggedIn);
};

onMounted(() => {
  getSession();
});
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <nav-bar />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
