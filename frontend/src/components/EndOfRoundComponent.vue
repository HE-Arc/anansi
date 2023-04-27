<script setup>
import { ref, onMounted, defineProps } from "vue";
import RoundResponseCard from "./RoundResponseCard.vue";

const props = defineProps({
  round: {
    default: null,
  },
  cards: {
    default: [],
  },
  username: {
    default: "",
  },
});

const round = ref(null);
const responseCards = ref([]);
const username = ref("");
const is_master = ref(false);

onMounted(() => {
  console.log("Round : ");
  console.log(props.round);
  round.value = props.round;
  responseCards.value = props.cards;
  username.value = props.username;
  is_master.value = props.round.master_object == props.username;
  round.value = props.round;
});
</script>

<template>
  <!-- Display the round's master -->
  <q-banner dense class="bg-primary text-white">
    <div class="row justify-center">
      <div class="text-h6 text-bold">Round Master:</div>
      <div class="text-h6 text-bold text-italic">{{ round.master_object.username }}</div>
    </div>
  </q-banner>

  <q-card v-for="card in responseCards" :key="card" class="col-4">
    <RoundResponseCard :card="card" :is_master="is_master" />
  </q-card>
</template>
