<script setup>
import { ref, onMounted, defineProps, defineEmits } from "vue";
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
  id: {
    default: null,
  },
});

const emits = defineEmits(["onSelect"]);

const round = ref(null);
const responseCards = ref([]);
const username = ref("");
const is_master = ref(false);
const master_name = ref("");

onMounted(() => {
  console.log("Round : ");
  console.log(props.round);

  round.value = props.round;
  responseCards.value = props.cards;
  username.value = props.username;
  //is_master.value = props.round.master_object.username == props.username;
  console.log("Round master : ", props.round.master_object, props.id);
  is_master.value = props.round.master_object.id == props.id;
  round.value = props.round;

  master_name.value = props.round.master_object.username;

  console.log("Master name : " + master_name.value);
  console.log("Player name : " + username.value);

  console.log("Is master : " + is_master.value);

  console.log("Round master : ");
  console.log(round.value.master_object.username);
});

const onCardSelectedByMaster = (card_id) => {
  console.log("Card selected by master : " + card_id);
  emits("onSelect", card_id);
};
</script>

<template>
  <!-- Display the round's master -->
  <q-banner dense class="bg-primary text-white">
    <div class="row justify-center">
      <div class="text-h6 text-bold">Round Master:</div>
      <div class="text-h6 text-bold text-italic">{{ master_name }}</div>
    </div>
  </q-banner>

  <p v-if="is_master">You are the master of this round, please choose the best card.</p>

  <q-card v-for="card in responseCards" :key="card" class="col-4">
    <RoundResponseCard
      :card="card"
      :is_master="is_master"
      @onSelect="onCardSelectedByMaster"
    />
  </q-card>
</template>
