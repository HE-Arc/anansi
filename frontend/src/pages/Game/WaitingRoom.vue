<script lang="ts" setup>
import { defineComponent, ref, onMounted } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRoute } from "vue-router";
import { Dictionary } from "express-serve-static-core";
import { isDeepStrictEqual } from "util";

const authStore = useAuthStore();
const username = authStore.getUsername;
const players = ref([]);
const gameSocket = ref(null);
const route = useRoute();
const isCreator = ref(false);

// Dictionary of functions that handle the game
const handlingGameFunctions: Dictionary<(data: any) => void> = {
  game_created: (data: any) => {
    console.log("game created");
    isCreator.value = true;
  },

  update_players: (data: any) => {
    console.log("update_players");
    console.log(data);
    players.value = data.players;
  },

  game_starting: (data: any) => {
    console.log("game_starting");
    console.log(data);
    // TODO
  },

  update_cards: (data: any) => {
    // TODO
  },

  display_round_winner: (data: any) => {
    // TODO
  },

  display_game_winner: (data: any) => {
    // TODO
  },
};

const connectToGameSocket = () => {
  // Get room_id from url
  const room_id = route.params.id;

  console.log("room_id : " + room_id);
  const url = "ws://127.0.0.1:8000/game/" + room_id + "/";

  gameSocket.value = new WebSocket(url);

  // Check if the socket has been created
  if (gameSocket.value == null) {
    console.log("Socket is null");
    return;
  }

  gameSocket.value.onmessage = function (e: any) {
    const data = JSON.parse(e.data);

    // Get action of type string
    const action: string = data.action;

    // IF action is in handlingGameFunctions
    if (action in handlingGameFunctions) {
      // Call the function that handles the game
      handlingGameFunctions[action](data);
    } else {
      console.log("Action not found");
    }
  };

  gameSocket.value.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  gameSocket.value.onopen = function () {
    const msg = {
      action: "create_or_join_game",
      game_name: room_id,
      username: username,
    };

    console.log("open " + username);
    gameSocket.value.send(JSON.stringify(msg));
  };
};

const startGame = () => {
  const msg = {
    action: "start_game",
  };
  gameSocket.value.send(JSON.stringify(msg));
};

onMounted(() => {
  connectToGameSocket();
});
</script>

<template>
  <q-page class="row justify-evenly content-start">
    <div class="col-11 col-md-6 col-lg-4">
      <div class="row justify-evenly align-center">
        <!-- Pseudo -->
        <h1>Welcome {{ username }}</h1>
        <h5 v-if="isCreator">Your are the game owner</h5>
        <!-- Button create room -->
        <q-btn
          v-if="isCreator"
          class="q-mt-sm"
          color="primary"
          @click="
            () => {
              startGame();
            }
          "
          flat
          label="Start game"
        />
        <!-- print players in a list -->
        <ul>
          <li v-for="player in players" :key="player">
            {{ player }}
          </li>
        </ul>
      </div>
    </div>
  </q-page>
</template>
