<template>
  <q-page class="row items-center justify-evenly">
    <register-form></register-form>
  </q-page>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import RegisterForm from 'components/RegisterForm.vue';

  export default defineComponent({
    name: 'RegisterPage',
    components: {
      RegisterForm
    }
  });
</script>
