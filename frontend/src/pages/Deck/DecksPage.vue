<script setup>
import { ref, onMounted, getCurrentInstance } from "vue";
import { useQuasar } from "quasar";
import { useAuthStore } from "src/stores/auth";
import { useRoute, useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();

const searchText = ref("");
const cardGames = ref([]);
const displayedCardGames = ref([]);
const favourites = ref([]);

const fetchDecks = async () => {
  try {
    const response = await api.get("decks");
    cardGames.value = response.data;
    search();
  } catch (error) {
    console.log(error);
  }
};

const fetchFavourites = async () => {
  if (!authStore.isLoggedIn) {
    return;
  }

  try {
    const response = await api.get("favourites");
    favourites.value = response.data;
    //console.log("favourites : ", favourites.value);
  } catch (error) {
    console.log(error);
  }
};

const isInFavorites = (cardGame) => {
  return favourites.value.some((favourite) => favourite.cardgame == cardGame.url);
};

const addToFavourites = async (cardgame) => {
  //console.log(cardgame);
  if (isInFavorites(cardgame)) {
    try {
      const response = await api.delete(`favourites/${cardgame.id}/`);

      $q.notify({
        message: "Card game removed from favourites",
        color: "positive",
      });
    } catch (error) {
      console.log(error);

      $q.notify({
        message: "Error removing card game from favourites",
        color: "negative",
      });
    }
  } else {
    //console.log("addToFavourites", cardgame.id);
    try {
      const response = await api.post(`favourites/`, {
        cardgame: cardgame.url,
      });

      $q.notify({
        message: "Card game added to favourites",
        color: "positive",
      });
    } catch (error) {
      console.log(error);

      $q.notify({
        message: "Error adding card game to favourites",
        color: "negative",
      });
    }
  }
  fetchDecks();
  fetchFavourites();

  //const response = await this.$api.post(`cardgames/${id}/favourites/`);
  //fetchCardGames();
};

const search = async () => {
  displayedCardGames.value = cardGames.value.filter((cardGame) =>
    cardGame.name.toLowerCase().includes(searchText.value.toLowerCase())
  );
};

const openDeck = async (id) => {
  router.push({ name: "decks.id", params: { id: id } });
  //this.$router.push({ name: "decks.id", params: { id: id } });
};

onMounted(() => {
  fetchDecks();
  fetchFavourites();
});
</script>

<template>
  <q-page class="row justify-center">
    <div class="col-12">
      <q-input
        rounded
        outlined
        v-model="searchText"
        label="search"
        @keyup.enter="search"
        class="q-ma-sm q-mt-md"
      >
        <template v-slot:prepend>
          <q-icon name="search" />
        </template>
      </q-input>

      <div>
        <q-list>
          <div v-for="(cardGame, index) in displayedCardGames" :key="index">
            <q-item clickable @click="openDeck(cardGame.id)">
              <q-item-section>
                <!-- Cardgame name with add to favourites button-->
                <q-item-label>{{ cardGame.name }}</q-item-label>
                <q-item-label caption lines="2">{{
                  cardGame.user_object.username
                }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn
                  class="q-mt-sm"
                  :color="isInFavorites(cardGame) ? 'primary' : 'black'"
                  @click="addToFavourites(cardGame)"
                  :icon="isInFavorites(cardGame) ? 'favorite' : 'favorite_border'"
                  flat
                />
              </q-item-section>
            </q-item>
            <q-separator spaced inset />
          </div>
        </q-list>
      </div>
    </div>
  </q-page>
</template>
