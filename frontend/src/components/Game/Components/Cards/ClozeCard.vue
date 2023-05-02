<script setup>
import { ref, onMounted, defineProps, watch } from "vue";

const props = defineProps({
  card: {
    default: {},
  },
});

const clozeCardText = (text, index) => {
  const words = text.split(" ");
  return words.slice(0, index).join(" ") + " __________ " + words.slice(index).join(" ");
};
</script>

<template>
  <!-- q-card avec contour noir épais et fond bleu -->
  <q-card class="q-ma-md bg-blue-6 text-white">
    <!-- q-card-section avec fond bleu -->
    <q-card-section>
      {{ clozeCardText(props.card.text, props.card.gap_index) }}
    </q-card-section>
  </q-card>
</template>
