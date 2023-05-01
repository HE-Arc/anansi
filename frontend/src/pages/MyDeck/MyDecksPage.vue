<script setup>
import { ref, onMounted, defineComponent, getCurrentInstance } from "vue";
import { isProxy, toRaw } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuasar } from "quasar";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const router = useRouter();
const route = useRoute();

const cardGames = ref([]);

const fetchCardGames = async () => {
  try {
    const response = await api.get("mydecks");
    cardGames.value = response.data;

    cardGames.value.forEach((cardGame) => {
      cardGame.readonly = true;
    });
  } catch (error) {
    console.log(error);
  }
};

const putchCardGamePrivacy = async (id, lastPrivacy) => {
  await this.$api.patch(`mydecks/${id}/`, {
    privacy: lastPrivacy == "private" ? "public" : "private",
  });
  fetchCardGames();
};

const cancelEditCardGameName = (cardGame) => {
  cardGame.name = cardGame.lastName;
  cardGame.readonly = true;
};

const putchCardGameName = async (id, name) => {
  await this.$api.patch(`mydecks/${id}/`, {
    name: name,
  });
  fetchCardGames();
};

const deleteCardGame = async (id) => {
  await this.$api.delete(`mydecks/${id}/`);
  this.fetchCardGames();
};

onMounted(() => {
  fetchCardGames();
});
</script>
<template>
  <q-page class="row justify-evenly content-start">
    <div class="col-11 col-md-6 col-lg-4">
      <div class="row justify-evenly align-center">
        <h1 class="q-my-sm">My decks</h1>
        <q-btn
          class="q-mt-sm"
          color="primary"
          @click="() => router.push({ name: 'mydecks.create' })"
          icon="add"
          flat
        />
      </div>
    </div>
    <div class="col-10 col-md-6 col-lg-4">
      <!-- If no card games, display message -->
      <div v-if="cardGames.length == 0">
        <h2>There is no deck</h2>
      </div>
      <div v-else>
        <!-- Display card games -->
        <q-list separator>
          <q-item clickable v-for="cardGame in this.cardGames" :key="cardGame.id">
            <q-input
              v-model="cardGame.name"
              :readonly="cardGame.readonly"
              :class="{ editable: !cardGame.readonly }"
            />
            <!-- Privacy -->
            <q-item-section side>
              <q-btn
                class="q-px-xs"
                :color="cardGame.privacy == 'private' ? 'primary' : 'grey-8'"
                @click="() => putchCardGamePrivacy(cardGame.id, cardGame.privacy)"
                icon="lock"
                flat
              />
            </q-item-section>
            <!-- Edit -->
            <q-item-section side>
              <q-btn
                v-if="cardGame.readonly == true"
                class="q-px-xs"
                color="primary"
                @click="
                  () => {
                    cardGame.readonly = false;
                    cardGame.lastName = cardGame.name;
                  }
                "
                icon="edit"
                flat
              />
              <!-- Save -->
              <q-btn-group v-else>
                <q-btn
                  class="q-px-xs"
                  color="primary"
                  @click="() => putchCardGameName(cardGame.id, cardGame.name)"
                  icon="check"
                  flat
                />
                <!-- Cancel -->
                <q-btn
                  class="q-px-xs"
                  color="primary"
                  @click="() => cancelEditCardGameName(cardGame)"
                  icon="close"
                  flat
                />
              </q-btn-group>
            </q-item-section>
            <!-- Show -->
            <q-item-section side>
              <q-btn
                class="q-mt-sm"
                color="primary"
                @click="() => router.push({ name: 'mydecks.id' })"
                icon="style"
                flat
              />
            </q-item-section>
            <!-- Delete -->
            <q-item-section side>
              <q-btn
                class="q-px-xs"
                color="primary"
                @click="() => deleteCardGame(cardGame.id)"
                icon="delete"
                flat
              />
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </div>
  </q-page>
</template>
