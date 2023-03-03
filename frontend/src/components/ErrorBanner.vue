<template>
  <q-banner class="bg-red-1 text-negative" rounded dense v-if="errors.length > 0">
    <template v-slot:avatar>
      <q-icon name="warning" color="negative" />
    </template>
    <ul>
      <li v-for="error in errors" :key="error">
        {{ error }}
      </li>
    </ul>
  </q-banner>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "ErrorBanner",
  setup() {
    return {};
  },
  props: {
    errors: {
      type: Array,
    },
  },
  mounted() {
    console.log("ErrorBanner mounted");
  },
});
</script>
