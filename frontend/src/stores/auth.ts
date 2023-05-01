import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false);
  const username = ref("");

  function login() {
    isLoggedIn.value = true;
  }

  function logout() {
    isLoggedIn.value = false;
  }

  return { isLoggedIn, username, login, logout };

  /*id: "auth",
  state: () => ({
    isLoggedIn: false,
    username: "",
  }),
  getters: {
    get: (state) => state.isLoggedIn,
    getUsername: (state) => state.username,
  },
  actions: {
    login() {
      this.isLoggedIn = true;
    },
    logout() {
      this.isLoggedIn = false;
    },
    setUsername(username: string) {
      this.username = username;
    }
  },*/
});
