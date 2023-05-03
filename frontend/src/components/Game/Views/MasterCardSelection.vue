<script setup>
import { ref, onMounted, defineProps, watch, defineEmits, computed } from "vue";
import { useQuasar } from "quasar";
import ClozeCard from "../Components/Cards/ClozeCard.vue";
import EmptyCard from "../Components/Cards/EmptyCard.vue";
import ResponseCard from "../Components/Cards/ResponseCard.vue";

const emit = defineEmits(["onSelect", "onSend"]);

const $q = useQuasar();

const props = defineProps({
  roundCounter: {
    default: 0,
  },
  clozeCard: {
    default: null,
  },
  selectedCard: {
    default: null,
  },
  responseCards: {
    default: [],
  },
  hasPlayerSelectedCard: {
    default: false,
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
  <q-card class="column justify-evenly">
    <div>
      <!-- Display round number -->
      <q-card-section
        class="text-center row justify-center items-center q-pb-none q-mb-none"
      >
        <text class="text-h6">Round {{ roundCounter }} / 6</text>
      </q-card-section>

      <!-- Display Cloze card with (empty) response card -->
      <q-card-section class="q-my-none q-py-xs">
        <!-- Display Cloze card with (empty) response card -->
        <div class="row justify-center items-center">
          <ClozeCard :card="clozeCard" class="text-bold col-5" :style="bigCardStyle" />
          <ResponseCard
            v-if="selectedCard !== null"
            :card="selectedCard"
            class="text-bold col-5 q-ma-md"
            :masterSelection="true"
            :style="bigCardStyle"
          />
          <EmptyCard v-else class="text-bold col-5" :style="bigCardStyle" />
        </div>
        <!-- Display message -->
      </q-card-section>
      <q-card-section class="row justify-center text-center">
        <p class="col-12">
          You are the master of this round, please choose the best card
        </p>
      </q-card-section>
    </div>
    <div>
      <!-- Display user response cards -->
      <q-card-section class="col-12 q-my-none q-py-xs">
        <div class="row justify-center items-center" style="align-items: stretch">
          <div
            v-for="card in responseCards"
            :key="card"
            class="q-pa-xs q-pa-lg-sm q-pa-md-sm"
          >
            <ResponseCard
              class="text-weight-regular"
              :card="card"
              :action="true"
              :masterSelection="true"
              :defaultStyle="false"
              :style="smallCardStyle"
              @onSelect="
                () => {
                  emit('onSelect', card);
                }
              "
            />
          </div>
        </div>
      </q-card-section>

      <!-- Display validate button -->
      <q-card-section class="row q-my-none q-py-xs justify-center">
        <q-btn
          class="q-ma-lg col-8"
          color="primary"
          @click="
            () => {
              emit('onSend', selectedCard.id);
            }
          "
          label="Validate card"
          :disable="!hasPlayerSelectedCard"
        />
      </q-card-section>
    </div>
  </q-card>
</template>
