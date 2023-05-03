<script setup>
import { defineProps } from "vue";
import { useToolsStore } from "src/stores/tools";

const toolsStore = useToolsStore();

const props = defineProps({
  card: {
    default: {},
  },
});
</script>

<template>
  <!-- Display card text -->
  <q-card class="q-ma-md bg-blue-6 text-white column justify-center items-center">
    <q-card-section class="flex" align="center">
      {{ toolsStore.clozeCardText(props.card.text, props.card.gap_index) }}
    </q-card-section>
  </q-card>
</template>
