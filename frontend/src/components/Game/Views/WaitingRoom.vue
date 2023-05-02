<script setup>
import { defineEmits, defineProps, ref, computed } from "vue";

const props = defineProps({
  gameOwner: {
    type: Object,
    required: true,
  },
  isCreator: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["start-game"]);

const inputText = computed(() => {
  return props.gameOwner.game_object !== undefined
    ? props.gameOwner.game_object.name
    : "Game name";
});

function onStartGame() {
  emit("start-game");
}
</script>

<template>
  <q-card>
    <q-card-section class="text-center row justify-center items-center">
      <h6 class="q-my-lg col-12">Waiting for players to join...</h6>
      <p class="col-12">Copy and send code to invite your friends !</p>

      <!-- link with copy button "-->
      <q-input
        :label="inputText"
        id="game-link"
        class="q-ma-lg col-8"
        outlined
        readonly
        dense
      />

      <!-- Button create room -->
      <q-btn
        v-if="isCreator"
        class="q-ma-lg col-8"
        color="primary"
        @click="onStartGame"
        label="Start game"
      />
    </q-card-section>
  </q-card>
</template>
