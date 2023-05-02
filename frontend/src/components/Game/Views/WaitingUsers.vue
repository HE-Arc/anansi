<script setup>
import { ref, computed, onMounted, defineProps } from "vue";

const props = defineProps({
  roundCounter: {
    default: 0,
  },
  playerCount: {
    default: 0,
  },
  cardSentCounter: {
    default: 0,
  },
});
</script>

<template>
  <q-card>
    <!-- Display round -->
    <h1>Round {{ roundCounter }} / 6</h1>
    <!-- Display message -->
    <p>Waiting users to choose cards...</p>

    <!-- Display card received -->
    <p>{{ cardSentCounter }} / {{ playerCount }} cards received</p>
  </q-card>
</template>
