<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  card: {
    default: null,
  },
  width: {
    default: 200,
  },
  height: {
    default: 200,
  },
});

const card_text = ref("");
const card_type = ref("");

onMounted(() => {
  card_text.value = props.card.text;
  card_type.value = props.card.type;
});
</script>

<template>
  <q-card class="my-card" style="width: {{ width }}px; height: {{ height }}px; background-color: red;">
    <!-- Display card text, and change color based on the type -->
    <q-card-section class="text-h6 text-white" :class="card_type">
      {{ card_text }}
    </q-card-section>
  </q-card>
</template>

<style></style>
