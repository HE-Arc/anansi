import { defineStore } from 'pinia';

export const useAuthStore = defineStore({
  id: "auth",
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
  },
});
