<script setup>
import { ref, onMounted, defineProps, watch } from "vue";
import ClozeCard from "../Components/Cards/ClozeCard.vue";
import EmptyCard from "../Components/Cards/EmptyCard.vue";
import ResponseCard from "../Components/Cards/ResponseCard.vue";

const props = defineProps({
  roundCounter: {
    default: 0,
  },
  clozeCard: {
    default: null,
  },
  responseCards: {
    default: null,
  },
});
</script>

<template>
  <q-card class="column justify-evenly">
    <div>
      <!-- Display round number -->
      <q-card-section
        class="text-center row justify-center items-center q-pb-none q-mb-none"
      >
        <!-- Display round number -->
        <text class="text-h6">Round {{ roundCounter }} / 6</text>
      </q-card-section>

      <!-- Display waiting message -->
      <q-card-section
        class="text-center row justify-center items-center q-pb-none q-mb-none"
      >
        <!-- Display message -->
        <p>Waiting master to choose round winner...</p>
      </q-card-section>

      <!-- Display cloze card -->
      <q-card-section class="q-my-none q-py-xs">
        <div class="row justify-center">
          <ClozeCard :card="clozeCard" class="col-5" />
        </div>
      </q-card-section>
    </div>
    <div>
      <!-- Display user response cards -->
      <q-card-section class="col-12 q-my-none q-py-xs">
        <div class="row justify-center" style="align-items: stretch">
          <div v-for="card in responseCards" :key="card" class="col-4 q-pa-xs">
            <ResponseCard
              :card="card"
              :action="false"
              :masterSelection="true"
              :defaultStyle="false"
            />
          </div>
        </div>
      </q-card-section>
    </div>
  </q-card>
</template>
