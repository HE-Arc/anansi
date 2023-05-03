<script setup>
import { defineEmits, defineProps, ref, computed, watch } from "vue";
import { copyToClipboard } from "quasar";

const props = defineProps({
  gameOwner: {
    type: Object,
    required: true,
  },
  isCreator: {
    type: Boolean,
    required: true,
  },
  disabled: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["start-game"]);

const text = ref("Game name");

const inputText = computed(() => {
  return props.gameOwner.game_object !== undefined
    ? props.gameOwner.game_object.name
    : "Game name";
});

function onStartGame() {
  emit("start-game");
}

watch(
  () => props.gameOwner.game_object,
  (newValue) => {
    text.value = newValue.name;
    console.log("game_name new value : ", newValue.name, "text value : ", text.value);
  }
);

const copy = () => {
  console.log("text : ", text.value);
  copyToClipboard(text.value);
};
</script>

<template>
  <q-card>
    <q-card-section class="text-center row justify-center items-center">
      <h6 class="q-my-lg col-12">Waiting for players to join...</h6>
      <p class="col-12">Copy and send code to invite your friends !</p>
      <!-- link with copy button "-->
      <q-input
        :label="text"
        id="game-link"
        class="q-ma-lg col-8 col-lg-4 col-md-6"
        outlined
        readonly
        dense
        label-class="text-black"
        label-color="text-black"
      >
        <template v-slot:append>
          <q-btn
            color="primary"
            icon="content_copy"
            @click="copy"
            class="q-mr-sm"
            flat
            size="sm"
          />
        </template>
      </q-input>

      <!-- Button create room -->
      <q-btn
        v-if="isCreator"
        class="q-ma-lg col-8"
        color="primary"
        @click="onStartGame"
        label="Start game"
        :disable="disabled"
      />
    </q-card-section>
  </q-card>
</template>
