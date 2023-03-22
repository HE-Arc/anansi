<script lang="ts" setup>
import { defineComponent, ref, onMounted } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRoute } from "vue-router";

const authStore = useAuthStore();
const username = authStore.getUsername;
const players = ref([]);
const gameSocket = ref(null);
const route = useRoute();

const connectToGameSocket = () => {
  // Get room_id from url
  const room_id = route.params.room_id;

  console.log(route.params);

  console.log("room_id : " + room_id);
  const url = "ws://127.0.0.1:8000/game/" + room_id + "/";

  gameSocket.value = new WebSocket(url);

  // var vm = this;

  gameSocket.value.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("message : " + data.username);
    players.value.push(data.username);
    console.log("players : ");
    console.log(data.players);
    // vm.players.push(data.username);
  };

  gameSocket.value.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  gameSocket.value.onopen = function () {
    const msg = {
      username: username,
    };
    console.log("open " + username);
    gameSocket.value.send(JSON.stringify(msg));
  };
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
