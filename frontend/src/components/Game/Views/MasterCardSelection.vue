<script setup>
import { ref, onMounted, defineProps, watch, defineEmits } from "vue";
import ClozeCard from "../Components/Cards/ClozeCard.vue";
import EmptyCard from "../Components/Cards/EmptyCard.vue";
import ResponseCard from "../Components/Cards/ResponseCard.vue";

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
  responseCards: {
    default: [],
  },
  hasPlayerSelectedCard: {
    default: false,
  },
});
</script>

<template>
  <q-card>
    <!-- Display round number -->
    <q-card-section>
      <h1>Round {{ roundCounter }} / 6</h1>
    </q-card-section>

    <!-- Display Cloze card with (empty) response card -->
    <q-card-section>
      <!-- Display Cloze card with (empty) response card -->
      <ClozeCard :card="clozeCard" class="col-6" />
      <ResponseCard
        v-if="selectedCard !== null"
        :card="selectedCard"
        class="col-6"
        :masterSelection="true"
      />
      <EmptyCard v-else class="col-6" />
    </q-card-section>

    <!-- Display message -->
    <p>You are the master of this round, please choose the best card.</p>

    <!-- Display user response cards -->
    <q-card-section>
      <ResponseCard
        v-for="card in responseCards"
        :key="card"
        :card="card"
        :action="true"
        :masterSelection="true"
        @onSelect="
          () => {
            emit('onSelect', card);
          }
        "
      />
    </q-card-section>

    <!-- Display validate button -->
    <q-card-section>
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
  </q-card>
</template>
