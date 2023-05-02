<script setup>
import { ref, onMounted, defineProps, watch } from "vue";

const props = defineProps({
  winner: {
    default: {},
  },
});
</script>

<template>
  <q-card>
    <q-card-section class="text-center justify-center items-center q-pb-none q-mb-none">
      <!-- Display winning message -->
      <h1 class="q-pa-none q-ma-none">Game over</h1>

      <h1 class="q-pa-none q-ma-none">🎉</h1>
      <text class="text-bold">
        Winner: <text class="text-primary text-bold">{{ props.winner }}</text>
      </text>
    </q-card-section>
    <!-- Display play again message -->
    <q-card-section class="text-center justify-center items-center">
      <q-btn color="primary" label="Play again" :to="{ name: 'game' }" class="q-ma-md" />
    </q-card-section>
  </q-card>
</template>
