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

const favourites = ref([]);

const fetchFavourites = async () => {
  if (!authStore.isLoggedIn) {
    return;
  }

  try {
    const response = await api.get("favourites");
    favourites.value = response.data;
    console.log("favourites : ", favourites.value);
  } catch (error) {
    console.log(error);
  }
};

const openDeck = async (id) => {
  router.push({ name: "decks.id", params: { id: id } });
  //this.$router.push({ name: "decks.id", params: { id: id } });
};

const removeFromFavourites = async (cardgame) => {
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
  fetchFavourites();
};

onMounted(() => {
  fetchFavourites();
});
</script>
<template>
  <q-page class="row justify-center">
    <div class="col-12">
      <div>
        <p v-if="favourites.length == 0">You have no favourite card games yet.</p>
        <q-list>
          <div v-for="(favourite, index) in favourites" :key="index">
            <q-item clickable>
              <q-item-section clickable @click="openDeck(favourite.deck)">
                <q-item-label>{{ favourite.deck_object.name }}</q-item-label>
                <q-item-label caption lines="2">{{
                  favourite.deck_object.user_object.username
                }}</q-item-label>
              </q-item-section>
              <!-- Bouton favoris -->
              <q-item-section side>
                <q-btn
                  class="q-mt-sm"
                  color="primary"
                  @click="removeFromFavourites(favourite.deck_object)"
                  icon="favorite"
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
