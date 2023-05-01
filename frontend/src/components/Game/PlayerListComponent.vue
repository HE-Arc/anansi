<script setup>
import { ref, onMounted, defineProps, watch } from "vue";
import { GameplayerStore } from "src/stores/gameplayerStore";

const props = defineProps({
  players: {
    default: [],
  },
  gameOwnerId: {
    default: 0,
  },
});

const players = ref([]);
const store = GameplayerStore();

onMounted(() => {
  players.value = props.players;
  sortByScore();
  console.log(players.value);
});

const sortByScore = () => {
  players.value = players.value.sort((a, b) => {
    return b.score - a.score;
  });
};

// observe the players prop and update the local players ref
// whenever the prop changes
watch(
  () => props.players,
  (newPlayers) => {
    players.value = newPlayers;
    sortByScore();
  }
);
</script>

<template>
  <div class="col-12">
    <div class="text-h6" v-if="props.players.length > 0">👤 Players</div>
    <!--<h4 v-if="players.length > 0">Players in the game</h4>-->
    <q-list v-if="players.length > 0" class="q-ma-none q-pa-none">
      <div v-for="player in players" :key="player">
        <q-item clickable class="q-px-xs">
          <q-item-section>
            <q-item-label
              :class="store.gameplayer_id == player.id ? 'text-primary text-bold' : ''"
              >{{ player.username }} {{ props.gameOwnerId == player.id ? "👑" : "" }}
            </q-item-label>
            <q-item-label caption>{{ player.score }} points</q-item-label>

            <!--{{ player.username }} (score : {{ player.score }})-->
          </q-item-section>
        </q-item>
        <q-separator spaced />
      </div>
    </q-list>
  </div>
</template>
