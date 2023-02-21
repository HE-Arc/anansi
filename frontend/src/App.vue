<template>
  <q-layout>
    <nav-bar />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import NavBar from './components/NavBar.vue';

export default defineComponent({
  name: 'App',
  components: {
    NavBar
  },
  data() {
    return {
      state: {
        csrf: '',
        isAuthenticated: false,
      }
    };
  },
  methods: {
    getSession() {
      fetch('/api/session')
        .then((response) => response.json())
        .then((data) => {
          this.state.isAuthenticated = data.isAuthenticated;
        });
    }
  },
  onMounted: function() {
    this.getSession();
  }
});
</script>
