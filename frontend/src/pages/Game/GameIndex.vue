<script setup>
import { ref } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRouter } from "vue-router";

const room_id = ref("");
const username = ref("");
const dialog = ref(false);
const router = useRouter();

const generateGameId = () => {
  room_id.value =
    Math.random().toString(36).substring(2, 15) +
    Math.random().toString(36).substring(2, 15);
};

const goToGameWaitingRoom = () => {
  if (room_id.value == "" || username.value == "") {
    return;
  }

  useAuthStore().username = username.value;

  router.push({
    name: "game.id",
    params: { id: room_id.value, username: username.value },
    props: { username: username.value },
  });
};
</script>

<template>
  <q-page class="row justify-evenly content-start">
    <div class="col-12">
      <div class="row justify-center align-center">
        <q-card class="q-mt-md col-11 col-md-6 col-lg-4 q-pa-md q-mt-md-xl q-pb-lg">
          <q-card-section>
            <!-- Title -->
            <div class="text-h6">🎮 Join or create a room</div>
          </q-card-section>
          <q-card-section>
            <!-- Pseudo -->
            <q-input
              v-model="username"
              label="Pseudo"
              filled
              class="q-my-sm"
              required
              :rules="[(val) => !!val || 'Pseudo is required']"
            />

            <div class="row justify-between q-mt-lg">
              <!-- Join room button -->
              <q-btn
                class="col-5 q-pa-sm"
                color="primary"
                label="Join room"
                @click="dialog = true"
              />

              <!-- Create room button -->
              <q-btn
                class="col-5 q-pa-sm"
                color="primary"
                @click="
                  () => {
                    generateGameId();
                    goToGameWaitingRoom();
                  }
                "
                label="Create room"
              />
            </div>
          </q-card-section>
        </q-card>
        <!-- Popup to enter room id -->
        <q-dialog v-model="dialog" persistent>
          <q-card>
            <q-card-section class="row items-center">
              <div class="text-h6">Enter room id</div>
            </q-card-section>
            <q-card-section>
              <q-input v-model="room_id" filled />
            </q-card-section>
            <q-card-actions align="right">
              <q-btn flat label="Cancel" color="primary" v-close-popup />
              <q-btn
                flat
                label="Join"
                color="primary"
                v-close-popup
                @click="goToGameWaitingRoom"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>
    </div>
  </q-page>
</template>
