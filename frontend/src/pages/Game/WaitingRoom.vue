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
<script lang="ts">
import { defineComponent, ref } from "vue";
import { useAuthStore } from "src/stores/auth";

export default defineComponent({
  name: "IndexRoom",
  setup() {
    const authStore = useAuthStore();
    const username = authStore.getUsername;
    const players = ref([]);
    const gameSocket = ref(null);

    function connectToGameSocket(){
      const room_id = this.$route.params.id;
      console.log("room_id : " + room_id);
      const url = "ws://127.0.0.1:8000/game/" + room_id + "/";

      const authStore = useAuthStore();
      const username = authStore.getUsername;

      this.gameSocket = new WebSocket(url);

      console.log("socket : " + this.gameSocket)

      this.gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log("message : " + data.username);
        this.players.push(data.username);
      };

      this.gameSocket.onclose = function (e) {
        console.error("Chat socket closed unexpectedly");
      };

      this.gameSocket.onopen = function () {
        const msg = {
          username: username,
        };
        console.log("open " + username);
        this.gameSocket.send(JSON.stringify(msg));
      };
    }

    return { username, players, gameSocket };
  },
  mounted() {
    this.connectToGameSocket();
  },
});
</script>
