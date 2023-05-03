<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRoute } from "vue-router";
import { Dictionary } from "express-serve-static-core";
import { useQuasar } from "quasar";
import { GameplayerStore } from "src/stores/gameplayerStore";

import CardComponent from "src/components/Game/CardComponent.vue";
import RoundResponseCard from "src/components/Game/RoundResponseCard.vue";
import EndOfRoundComponent from "src/components/Game/EndOfRoundComponent.vue";
import PlayerListComponent from "src/components/Game/PlayerListComponent.vue";

import ClozeCard from "src/components/Game/Components/Cards/ClozeCard.vue";
import EmptyCard from "src/components/Game/Components/Cards/EmptyCard.vue";

import WaitingRoom from "src/components/Game/Views/WaitingRoom.vue";
import UserCardSelection from "src/components/Game/Views/UserCardSelection.vue";
import WaitingUsers from "src/components/Game/Views/WaitingUsers.vue";
import MasterCardSelection from "src/components/Game/Views/MasterCardSelection.vue";
import WaitingMaster from "src/components/Game/Views/WaitingMaster.vue";
import RoundResult from "src/components/Game/Views/RoundResult.vue";
import GameResult from "src/components/Game/Views/GameResult.vue";
import DecksList from "src/components/Game/DecksList.vue";

const gameplayerStore = GameplayerStore();
const authStore = useAuthStore();
const $q = useQuasar();
const route = useRoute();

const username = ref(authStore.username);
const gameOwner = ref("");
const gameOwnerId = ref(0);
const players = ref([]);
const gameSocket = ref(null);

const isCreator = ref(false);
const players_cards = ref([]); // Cards owned by the player
const round_response_cards = ref([]); // Cards sent by the players for a round
const isGameStarted = ref(false);
const hasPlayerSelectedCard = ref(false); // The player has selected a card
const hasPlayerSentCard = ref(false); // The player has sent a card
const hasMasterSelectedCard = ref(false); // The master has selected a card
const isCardSelectionOver = ref(false); // All the players have choosen their cards, and now the master must choose the best one
const isRoundOver = ref(false); // The master has choosen the best card, and now the players must see the result
const isGameOver = ref(false); // The game is over
const isMaster = ref(false); // The player is the master for the current round
const masterId = ref(0); // The id of the master for the current round

const selectedDeckId = ref(null); // The deck selected by the creator of the game to play with

const roundCounter = ref(0);

const roundWinningCard = ref(null);
const roundWinningPlayerUsername = ref("");
const gameWinnerName = ref("");

const card_sent_counter = ref(0);
const player_count = ref(0);
const error_message = ref("");
const current_round = ref(null);
const cloze_card = ref("");
const cloze_card_ = ref({});

const selectedCard = ref(null);
const masterSelectedCard = ref(null);
const openDialog = ref(true);

const WAITING_ROOM = computed(() => {
  return !isGameStarted.value;
});

const USER_CARD_SELECTION = computed(() => {
  return (
    isGameStarted.value &&
    !isRoundOver.value &&
    !isCardSelectionOver.value &&
    !isMaster.value &&
    !hasPlayerSentCard.value
  );
});

const MASTER_CARD_SELECTION = computed(() => {
  return isCardSelectionOver.value && !isRoundOver.value && isMaster.value;
});

const WAITING_USER_CARD_SELECTION = computed(() => {
  return (
    isGameStarted.value &&
    !isRoundOver.value &&
    !isCardSelectionOver.value &&
    (hasPlayerSentCard.value || isMaster.value)
  );
});

const WAITING_MASTER_CARD_SELECTION = computed(() => {
  return isCardSelectionOver.value && !isRoundOver.value && !isMaster.value;
});

const ROUND_RESULT = computed(() => {
  return isRoundOver.value && !isGameOver.value;
});

const GAME_RESULT = computed(() => {
  return isGameOver.value;
});

// Dictionary of functions that handle the game
const handlingGameFunctions: Dictionary<(data: any) => void> = {
  game_joined_or_created: (data: any) => {
    console.log("game_joined_or_created");
    console.log(data);

    // Set the game
    gameplayerStore.setGameId(data.game_id);

    // Set the gameplayer id
    console.log("gameplayer_id : " + data.gameplayer_id);
    gameplayerStore.setGameplayerId(data.gameplayer_id);

    $q.loading.hide();
  },

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
    gameOwnerId.value = data.creator.id;

    isCreator.value = data.creator.id == gameplayerStore.gameplayer_id;

    $q.loading.hide();
  },

  start_new_round: (data: any) => {
    console.log("game_starting");
    console.log(data);

    roundCounter.value += 1;

    // Update state variables
    isCardSelectionOver.value = false;
    isRoundOver.value = false;
    isGameStarted.value = true;
    masterId.value = data.master.id;
    isMaster.value = data.master.id == gameplayerStore.gameplayer_id;

    // Display the received players_cards
    players_cards.value = data.cards;

    cloze_card.value = data.cloze_card;
    cloze_card_.value = data.cloze_card_;

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
    //isMaster.value = data.master_object.id == gameplayerStore.gameplayer_id;
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
    hasPlayerSelectedCard.value = false;
    hasPlayerSentCard.value = false;
    selectedCard.value = null;
    hasMasterSelectedCard.value = false;
    masterSelectedCard.value = null;

    $q.loading.hide();
  },

  display_game_winner: (data: any) => {
    console.log("display_game_winner");
    console.log(data);

    gameWinnerName.value = data.winner;

    isGameOver.value = true;

    $q.loading.hide();
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
      // Call the function that handles the action
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
    // If the user is not authentified
    if (username.value == null || username.value == null || username.value == "") {
      username.value = gameplayerStore.generateAnonUsername();
    } else gameplayerStore.setUsername(username.value);

    const msg = {
      action: "create_or_join_game",
      game_name: room_id,
      username: username.value,
    };

    console.log("GamePlayer username : " + username.value);
    gameSocket.value.send(JSON.stringify(msg));
  };
};

const sendCard = (card) => {
  // $q.loading.show();

  console.log("sendCard " + card.id);

  hasPlayerSelectedCard.value = true;
  hasPlayerSentCard.value = true;

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

const onDeckSelected = (deck_id) => {
  console.log("onDeckSelected");
  console.log(deck_id);

  selectedDeckId.value = deck_id;
};

const startGame = () => {
  const msg = {
    action: "start_game",
  };

  // Add the selected deck if not null
  if (selectedDeckId.value != null) {
    $q.loading.show();

    console.log("startGame : " + selectedDeckId.value);

    msg["deck_id"] = selectedDeckId.value;

    gameSocket.value.send(JSON.stringify(msg));
  } else {
    // Pop up error message
    $q.notify({
      message: "A deck must be selected to start the game",
      color: "red",
    });
  }
};

const nextRound = () => {
  $q.loading.show();

  const msg = {
    action: "next_round",
    deck_id: selectedDeckId.value,
  };

  gameSocket.value.send(JSON.stringify(msg));
};

onMounted(() => {
  connectToGameSocket();
});

const masterCardSelected = (card) => {
  masterSelectedCard.value = card;
  hasMasterSelectedCard.value = true;
  console.log("masterCardSelected");
};

const cardSelected = (card) => {
  selectedCard.value = card;
  hasPlayerSelectedCard.value = true;
};
</script>

<template>
  <q-page class="row justify-evenly content-start" style="height: 100%">
    <!-- Users list -->
    <div class="col-12 col-lg-3 q-pa-md">
      <q-dialog persistent v-model="openDialog" v-if="isCreator">
        <q-card>
          <q-card-section class="q-pb-none q-mb-none row justify-center">
            <div class="text-h6">Select deck</div>
          </q-card-section>
          <q-card-section class="q-pt-none q-mt-none">
            <DecksList @on-select-deck="onDeckSelected" />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn
              flat
              label="Confirm"
              color="primary"
              v-close-popup
              :disabled="selectedDeckId == null"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <!-- print players in a list --><!--&& !isGameStarted-->
      <PlayerListComponent
        v-if="players.length > 0 || isGameOver"
        :players="players"
        :gameOwnerId="gameOwnerId"
        :masterId="masterId"
        :displayMobile="$q.screen.lt.lg"
      />
    </div>
    <div class="col-12 col-lg-9 q-px-sm q-my-md-md">
      <WaitingRoom
        v-if="WAITING_ROOM"
        :gameOwner="gameOwner"
        :isCreator="isCreator"
        @start-game="startGame"
        :disabled="players.length < 3"
      />
      <UserCardSelection
        v-if="USER_CARD_SELECTION"
        :roundCounter="roundCounter"
        :clozeCard="cloze_card_"
        :selectedCard="selectedCard"
        :playersCards="players_cards"
        :hasPlayerSelectedCard="hasPlayerSelectedCard"
        @onSelect="cardSelected"
        @onSend="sendCard"
      />
      <WaitingUsers
        v-if="WAITING_USER_CARD_SELECTION"
        :roundCounter="roundCounter"
        :playerCount="player_count - 1"
        :cardSentCounter="card_sent_counter"
      />
      <MasterCardSelection
        v-if="MASTER_CARD_SELECTION"
        :roundCounter="roundCounter"
        :clozeCard="cloze_card_"
        :selectedCard="masterSelectedCard"
        :responseCards="round_response_cards"
        :hasPlayerSelectedCard="hasMasterSelectedCard"
        @onSelect="masterCardSelected"
        @onSend="chooseRoundWinner"
      />
      <WaitingMaster
        v-if="WAITING_MASTER_CARD_SELECTION"
        :roundCounter="roundCounter"
        :clozeCard="cloze_card_"
        :responseCards="round_response_cards"
      />
      <RoundResult
        v-if="ROUND_RESULT"
        :roundCounter="roundCounter"
        :clozeCard="cloze_card_"
        :winningCard="roundWinningCard"
        :isCreator="isCreator"
        @nextRound="nextRound"
      />
      <GameResult v-if="GAME_RESULT" :winner="gameWinnerName" />
    </div>

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
  </q-page>
</template>
