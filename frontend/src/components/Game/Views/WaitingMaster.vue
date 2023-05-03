<script setup>
import { ref, onMounted, defineProps, watch, computed } from "vue";
import { useQuasar } from "quasar";
import ClozeCard from "../Components/Cards/ClozeCard.vue";
import EmptyCard from "../Components/Cards/EmptyCard.vue";
import ResponseCard from "../Components/Cards/ResponseCard.vue";

const $q = useQuasar();

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

const bigCardStyle = computed(() => {
  return $q.screen.lt.lg ? "width: 130px; height: 173px" : "width: 170px; height: 227px";
});

const smallCardStyle = computed(() => {
  return $q.screen.lt.lg ? "width: 100px; height: 133px" : "width: 120px; height: 160px";
});
</script>

<template>
  <q-card class="column justify-evenly q-pb-lg">
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
        <div class="row justify-center items-center">
          <ClozeCard :card="clozeCard" class="col-5" :style="bigCardStyle" />
        </div>
      </q-card-section>
    </div>
    <div>
      <!-- Display user response cards -->
      <q-card-section class="col-12 q-my-none q-py-xs">
        <div class="row justify-center items-center" style="align-items: stretch">
          <div v-for="card in responseCards" :key="card" class="q-pa-xs">
            <ResponseCard
              class="text-bold"
              :card="card"
              :action="false"
              :masterSelection="true"
              :defaultStyle="false"
              :style="smallCardStyle"
            />
          </div>
        </div>
      </q-card-section>
    </div>
  </q-card>
</template>
