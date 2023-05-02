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
    <q-card-section
      class="text-center row justify-center items-center q-pb-none q-mb-none"
    >
      <!-- Display round number -->
      <text class="text-h6">Round {{ roundCounter }} / 6</text>
    </q-card-section>
    <q-card-section
      class="text-center row justify-center items-center q-pb-none q-mb-none"
    >
      <!-- Display message -->
      <p>Waiting users to choose cards...</p>
    </q-card-section>

    <q-card-section
      class="text-center row justify-center items-center q-pb-none q-mb-none"
    >
      <!-- Display card received -->
      <p>{{ cardSentCounter }} / {{ playerCount }} cards received</p>
    </q-card-section>
  </q-card>
</template>
