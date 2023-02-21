<template>
  <q-page class="row items-center justify-evenly">
    <login-form></login-form>
  </q-page>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import LoginForm from 'components/LoginForm.vue';

  export default defineComponent({
    name: 'LoginPage',
    components: {
      LoginForm
    }
  });
</script>
