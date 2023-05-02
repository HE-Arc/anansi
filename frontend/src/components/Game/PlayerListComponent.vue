<script setup>
import { ref, onMounted, defineProps, watch, computed } from "vue";
import { GameplayerStore } from "src/stores/gameplayerStore";

const props = defineProps({
  players: {
    default: [],
  },
  gameOwnerId: {
    default: null,
  },
  masterId: {
    default: null,
  },
  displayMobile: {
    default: false,
  },
});

const players = ref([]);
const store = GameplayerStore();

const colSize = computed(() => {
  return 12 / players.value.length;
});

onMounted(() => {
  players.value = props.players;
  sortByScore();
  console.log("PlayerList : ", props.masterId, props.gameOwnerId);
  //console.log(players.value);
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
  <div class="col-12" v-if="!displayMobile">
    <div class="text-h6" v-if="props.players.length > 0">👤 Players</div>
    <q-list v-if="players.length > 0" class="q-ma-none q-pa-none">
      <div v-for="player in players" :key="player">
        <q-item clickable class="q-px-xs">
          <q-item-section>
            <q-item-label
              :class="store.gameplayer_id == player.id ? 'text-primary text-bold' : ''"
              >{{ player.username }} {{ props.gameOwnerId == player.id ? "👑" : "" }}
              {{ props.masterId == player.id ? "👔" : "" }}
            </q-item-label>
            <q-item-label caption>{{ player.score }} points</q-item-label>
          </q-item-section>
        </q-item>
        <q-separator spaced />
      </div>
    </q-list>
  </div>
  <div v-else class="row">
    <div v-for="player in players" :key="player">
      <div :class="'col-' + colSize + ' q-pa-sm'">
        <q-item-section>
          <q-item-label
            :class="store.gameplayer_id == player.id ? 'text-primary text-bold' : ''"
            >{{ player.username }} {{ props.gameOwnerId == player.id ? "👑" : "" }}
            {{ props.masterId == player.id ? "👔" : "" }}
          </q-item-label>
          <q-item-label caption>{{ player.score }} points</q-item-label>
        </q-item-section>
      </div>
    </div>
  </div>
</template>
