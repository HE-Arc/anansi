<script setup>
import { ref, onMounted, getCurrentInstance } from "vue";
import { useQuasar } from "quasar";
import { useAuthStore } from "src/stores/auth";
import { useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();

const searchText = ref("");
const decks = ref([]);
const displayedDecks = ref([]);
const favourites = ref([]);

const fetchDecks = async () => {
  try {
    const response = await api.get("decks/get_public_decks");
    decks.value = response.data;
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
  } catch (error) {
    console.log(error);
  }
};

const isInFavorites = (deck) => {
  return favourites.value.some((favourite) => favourite.deck == deck.url);
};

const addToFavourites = async (deck) => {
  if (isInFavorites(deck)) {
    try {
      await api.delete(`favourites/${deck.id}/`);

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
    try {
      await api.post(`favourites/`, {
        deck: deck.url,
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
  fetchFavourites();
  fetchDecks();
};

const search = async () => {
  displayedDecks.value = decks.value.filter((deck) =>
    deck.name.toLowerCase().includes(searchText.value.toLowerCase())
  );
};

const openDeck = async (id) => {
  router.push({ name: "decks.id", params: { id: id } });
};

onMounted(() => {
  fetchFavourites();
  fetchDecks();
});
</script>

<template>
  <q-page class="row justify-center">
    <div class="col-12">
      <!-- Barre de recherche -->
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

      <!-- Liste des decks -->
      <div>
        <q-list>
          <div v-for="(deck, index) in displayedDecks" :key="index">
            <q-item clickable>
              <q-item-section clickable @click="openDeck(deck.id)">
                <q-item-label>{{ deck.name }}</q-item-label>
                <q-item-label caption lines="2">{{
                  deck.user_object.username
                }}</q-item-label>
              </q-item-section>
              <!-- Bouton favoris -->
              <q-item-section side>
                <q-btn
                  class="q-mt-sm"
                  :color="isInFavorites(deck) ? 'primary' : 'black'"
                  @click="addToFavourites(deck)"
                  :icon="isInFavorites(deck) ? 'favorite' : 'favorite_border'"
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
