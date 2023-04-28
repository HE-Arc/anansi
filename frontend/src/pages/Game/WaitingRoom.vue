<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRoute } from "vue-router";
import { Dictionary } from "express-serve-static-core";
import { useQuasar } from "quasar";

import CardComponent from "src/components/CardComponent.vue";
import RoundResponseCard from "src/components/RoundResponseCard.vue";
import EndOfRoundComponent from "src/components/EndOfRoundComponent.vue";
import PlayerListComponent from "src/components/PlayerListComponent.vue";

const $q = useQuasar();

const authStore = useAuthStore();
const route = useRoute();

const username = authStore.getUsername;
const gameOwner = ref("");
const players = ref([]);
const gameSocket = ref(null);

const isCreator = ref(false);
const players_cards = ref([]); // Cards owned by the player
const round_response_cards = ref([]); // Cards sent by the players for a round
const isGameStarted = ref(false);
const isCardSelectionOver = ref(false); // All the players have choosen their cards, and now the master must choose the best one
const isRoundOver = ref(false); // The master has choosen the best card, and now the players must see the result

const roundWinningCard = ref(null);
const roundWinningPlayerUsername = ref("");

const card_sent_counter = ref(0);
const player_count = ref(0);
const error_message = ref("");
const current_round = ref(null);

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

    // Display the received players_cards
    players_cards.value = data.cards;

    $q.loading.hide();
  },

  update_cards: (data: any) => {
    // TODO
  },

  // This function is called when a player sends a card, and used to update the counter of players_cards sent
  update_players_count: (data: any) => {
    console.log(data);

    player_count.value = data.player_number;
  },

  update_card_sent_counter: (data: any) => {
    console.log(data);

    card_sent_counter.value = data.card_sent_counter;
  },

  // End of the round, display response players_cards
  display_response_cards: (data: any) => {
    console.log(data);

    // Send to counter to 0
    card_sent_counter.value = 0;
    player_count.value = 0;

    // Display the received players_cards
    round_response_cards.value = data.cards;

    current_round.value = data.round;
    console.log("current_round");
    console.log(current_round.value);

    isCardSelectionOver.value = true;

    $q.loading.hide();
  },

  display_round_winner: (data: any) => {
    console.log("display_round_winner");
    console.log(data);

    roundWinningCard.value = data.card;

    roundWinningPlayerUsername.value = data.card.player_object.username;

    isRoundOver.value = true;

    $q.loading.hide();
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

    error_message.value = e.reason;
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

const chooseRoundWinner = (card_id: string) => {
  $q.loading.show();

  console.log("chooseRoundWinner " + card_id);

  const msg = {
    action: "choose_round_winner",
    card_id: card_id,
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

const nextRound = () => {
  $q.loading.show();

  const msg = {
    action: "next_round",
  };
  gameSocket.value.send(JSON.stringify(msg));
};

onMounted(() => {
  connectToGameSocket();
});
</script>

<template>
  <q-page class="row justify-evenly content-start">
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
      <!-- <h1 v-if="username">Welcome {{ username }}</h1> -->
      <h5 v-if="isCreator">Your are the game owner</h5>
      <h5 v-if="!isCreator && username">Game owner: {{ gameOwner }}</h5>
      <!-- Button create room -->
      <q-btn
        v-if="isCreator && !isGameStarted"
        class="q-mt-sm col-12"
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
      <PlayerListComponent
        v-if="players.length > 0 && !isGameStarted"
        :players="players"
      />

      <!-- Display card sent counter and number of players-->
      <h2 v-if="isGameStarted && !isCardSelectionOver">Cards sent</h2>
      <h3 v-if="isGameStarted && !isCardSelectionOver">
        {{ card_sent_counter }} / {{ player_count }}
      </h3>

      <!-- Display players_cards -->
      <h2 v-if="players_cards.length > 0 && !isCardSelectionOver">Your cards</h2>
      <div
        v-if="players_cards.length > 0 && !isCardSelectionOver"
        class="row justify-evenly"
      >
        <q-card v-for="card in players_cards" :key="card" class="col-12">
          <CardComponent
            :card="card"
            @onSelect="
              () => {
                sendCard(card);
              }
            "
          />
        </q-card>
      </div>

      <!-- Display round_response_cards -->
      <EndOfRoundComponent
        class="col-12"
        v-if="isCardSelectionOver && !isRoundOver"
        :cards="round_response_cards"
        :round="current_round"
        :username="username"
        @onSelect="chooseRoundWinner"
      />

      <div class="col-12" v-if="isRoundOver">
        <!-- Next round button is the player is the game owner -->
        <q-btn
          v-if="isCreator"
          class="q-mt-sm col-12"
          color="primary"
          @click="
            () => {
              nextRound();
            }
          "
          flat
          label="Next round"
        />

        <h5>The following card wins the round :</h5>
        <RoundResponseCard
          :card="roundWinningCard"
          v-if="isRoundOver"
          :is_master="false"
        />
      </div>
    </div>
  </q-page>
</template>
