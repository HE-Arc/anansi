<script setup>
import { ref, onMounted, defineProps, defineEmits } from "vue";
import ClozeCard from "../Components/Cards/ClozeCard.vue";
import EmptyCard from "../Components/Cards/EmptyCard.vue";
import ResponseCard from "../Components/Cards/ResponseCard.vue";
import CardComponent from "../CardComponent.vue";

const emit = defineEmits(["onSelect", "onSend"]);

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
  playersCards: {
    default: [],
  },
  hasPlayerSelectedCard: {
    default: false,
  },
});
</script>

<template>
  <q-card class="column justify-evenly">
    <div>
      <q-card-section
        class="text-center row justify-center items-center q-pb-none q-mb-none"
      >
        <!-- Display round number -->
        <text class="text-h6">Round {{ roundCounter }} / 6</text>
      </q-card-section>

      <q-card-section class="q-my-none q-py-xs">
        <!-- Display Cloze card with (empty) response card -->
        <div class="row">
          <ClozeCard :card="clozeCard" class="col-5" />
          <ResponseCard
            v-if="selectedCard !== null"
            :card="selectedCard"
            class="col-5 q-ma-md"
          />
          <EmptyCard v-else class="col-5" />
        </div>
      </q-card-section>
    </div>
    <div>
      <!-- Display user response cards -->
      <q-card-section class="col-12 q-my-none q-py-xs">
        <div class="row justify-start" style="align-items: stretch">
          <div v-for="card in playersCards" :key="card" class="col-4 q-pa-xs">
            <ResponseCard
              :card="card"
              :action="true"
              :defaultStyle="false"
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
              emit('onSend', selectedCard);
            }
          "
          label="Validate card"
          :disable="!hasPlayerSelectedCard"
        />
      </q-card-section>
    </div>
  </q-card>
</template>
