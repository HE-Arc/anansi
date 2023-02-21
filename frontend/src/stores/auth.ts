import { defineStore } from 'pinia';

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    isLoggedIn: false,
  }),
  getters: {
    get: (state) => state.isLoggedIn,
  },
  actions: {
    login() {
      this.isLoggedIn = true;
    },
    logout() {
      this.isLoggedIn = false;
    },
  },
});
