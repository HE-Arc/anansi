<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRoute } from "vue-router";
import { Dictionary } from "express-serve-static-core";
import { useQuasar } from "quasar";

import CardComponent from "src/components/CardComponent.vue";

const $q = useQuasar();

const authStore = useAuthStore();
const username = authStore.getUsername;
const gameOwner = ref("");
const players = ref([]);
const gameSocket = ref(null);
const route = useRoute();
const isCreator = ref(false);
const cards = ref([]);
const isGameStarted = ref(false);
const card_sent_counter = ref(0);
const player_count = ref(0);
const error_message = ref("");

// Dictionary of functions that handle the game
const handlingGameFunctions: Dictionary<(data: any) => void> = {
  error: (data: any) => {
    console.log("error");
    console.log(data);

    error_message.value = data.message;

    $q.loading.hide();
  },
  update_players: (data: any) => {
    console.log("update_players");
    console.log(data);
    players.value = data.players;

    gameOwner.value = data.creator;

    isCreator.value = data.creator == username;

    $q.loading.hide();
  },

  game_starting: (data: any) => {
    console.log("game_starting");
    console.log(data);

    isGameStarted.value = true;

    // Display the received cards
    cards.value = data.cards;

    $q.loading.hide();
  },

  update_cards: (data: any) => {
    // TODO
  },

  // This function is called when a player sends a card, and used to update the counter of cards sent
  update_players_count: (data: any) => {
    console.log(data);

    player_count.value = data.player_number;
  },

  update_card_sent_counter: (data: any) => {
    console.log(data);

    card_sent_counter.value = data.card_sent_counter;
  },

  // End of the round, display response cards
  display_response_cards: (data: any) => {
    console.log(data);

    // Send to counter to 0
    card_sent_counter.value = 0;
    player_count.value = 0;

    // Display the received cards
    cards.value = data.cards;

    $q.loading.hide();
  },

  display_round_winner: (data: any) => {
    // TODO
  },

  display_game_winner: (data: any) => {
    // TODO
  },
};

const connectToGameSocket = () => {
  $q.loading.show();

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
      console.log("Action " + action + " not found");
    }
  };

  gameSocket.value.onclose = function (e) {
    console.log(e);
    if (e.wasClean) {
      console.log("Connection closed cleanly");
    } else {
      console.log("Connection died");
    }
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

const sendCard = (card) => {
  // $q.loading.show();

  const msg = {
    action: "send_card",
    card_id: card.id,
  };
  gameSocket.value.send(JSON.stringify(msg));
};

const chooseRoundWinner = (winner: string) => {
  $q.loading.show();

  const msg = {
    action: "choose_round_winner",
    winner: winner,
  };
  gameSocket.value.send(JSON.stringify(msg));
};

const startGame = () => {
  $q.loading.show();

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
        <!-- Display error message as a banner if not empty -->
        <div v-if="error_message != ''" class="text-white bg-red">
          <q-banner dense class="text-white bg-red">
            {{ error_message }}
          </q-banner>
          <!-- Go back to main menu button -->
          <q-btn
            class="q-mt-sm"
            color="text-white"
            @click="() => $router.push('/')"
            flat
            label="Go back to main menu"
          />
        </div>

        <!-- Pseudo -->
        <h1 v-if="username">Welcome {{ username }}</h1>
        <h5 v-if="isCreator">Your are the game owner</h5>
        <h5 v-if="!isCreator && username">Game owner: {{ gameOwner }}</h5>
        <!-- Button create room -->
        <q-btn
          v-if="isCreator && !isGameStarted"
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

        <!-- print players in a list using quasar component -->
        <h2 v-if="players.length > 0">Players</h2>
        <q-list v-if="players.length > 0">
          <q-item v-for="player in players" :key="player" clickable>
            <q-item-section>{{ player }}</q-item-section>
          </q-item>
        </q-list>

        <!-- Display card sent counter and number of players-->
        <h2 v-if="isGameStarted">Cards sent</h2>
        <h3 v-if="isGameStarted">{{ card_sent_counter }} / {{ player_count }}</h3>

        <!-- Display cards -->
        <h2 v-if="cards.length > 0">Your cards</h2>
        <div v-if="cards.length > 0" class="row justify-evenly">
          <q-card v-for="card in cards" :key="card" class="col-4">
            <CardComponent
              :card="card"
              @onSelect="
                () => {
                  sendCard(card);
                }
              "
            />
            <!-- <q-card-actions align="right">
              <q-btn
                color="primary"
                flat
                label="Send"
                @click="
                  () => {
                    sendCard(card);
                  }
                "
              />
            </q-card-actions> -->
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>
