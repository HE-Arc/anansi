<script setup>
import { ref, onMounted, defineProps } from "vue";

const props = defineProps({
  players: {
    default: [],
  },
});

const players = ref([]);

onMounted(() => {
  players.value = props.players;
  console.log(players.value);
});
</script>

<template>
  <div class="col-12">
    <h4 v-if="players.length > 0">Players in the game</h4>
    <q-list v-if="players.length > 0">
      <q-item v-for="player in players" :key="player" clickable class="12">
        <q-item-section>
          - {{ player.username }} (score : {{ player.score }})</q-item-section
        >
      </q-item>
    </q-list>
  </div>
</template>
