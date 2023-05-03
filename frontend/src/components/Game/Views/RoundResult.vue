<script setup>
import { ref, onMounted, defineProps, defineEmits } from "vue";
import ClozeCard from "../Components/Cards/ClozeCard.vue";
import EmptyCard from "../Components/Cards/EmptyCard.vue";
import ResponseCard from "../Components/Cards/ResponseCard.vue";
import CardComponent from "../CardComponent.vue";

const emit = defineEmits(["nextRound"]);

const props = defineProps({
  roundCounter: {
    default: 0,
  },
  clozeCard: {
    default: null,
  },
  winningCard: {
    default: null,
  },
  isCreator: {
    default: false,
  },
});

const winner = ref(props.winningCard.player_object.username);
</script>

<template>
  <q-card>
    <!-- Display round -->
    <q-card-section
      class="text-center row justify-center items-center q-pb-none q-mb-none"
    >
      <!-- Display round number -->
      <text class="text-h6">Round {{ roundCounter }} / 6</text>
    </q-card-section>

    <!-- Display winning message -->
    <q-card-section
      class="text-center row justify-center items-center q-pb-none q-mb-none"
    >
      <!-- Display message -->
      <p>
        🎉 Round winner is <text class="text-primary text-bold">{{ winner }}</text>
      </p>
    </q-card-section>

    <!-- Display cloze card and response card -->
    <q-card-section class="q-my-none q-py-xs">
      <div class="row justify-center items-center">
        <!-- Display cloze card -->
        <ClozeCard
          :card="clozeCard"
          class="text-bold col-5"
          style="width: 150px; height: 200px"
        />
        <ResponseCard
          :card="winningCard"
          :masterSelection="true"
          style="width: 150px; height: 200px"
          class="text-bold col-5 q-ma-md"
        />
      </div>
    </q-card-section>

    <!-- Display next round button -->
    <q-card-actions align="center">
      <q-btn
        v-if="isCreator"
        class="q-my-lg col-5"
        color="primary"
        @click="
          () => {
            emit('nextRound');
          }
        "
        label="Next round"
      />
    </q-card-actions>
  </q-card>
</template>
