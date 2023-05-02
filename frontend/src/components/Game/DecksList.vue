<script setup>
import { ref, onMounted, getCurrentInstance, defineEmits } from "vue";
import { useQuasar } from "quasar";
import { useAuthStore } from "src/stores/auth";
import { useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();

const searchText = ref("");
const favoriteOnly = ref(false);
const decks = ref([]);
const displayedDecks = ref([]);

const selectedDeckId = ref(null);

const emit = defineEmits(["onSelectDeck"]);

const removeEmptyDeck = async () => {
  let notEmptyDecks = [];

  // Foreach deck, get the response card from the api
  for (let i = 0; i < decks.value.length; i++) {
    const deck_id = decks.value[i].id;

    const response = await api.get(`responsecards/get_responsecards`, {
      params: {
        deck: deck_id,
      },
    });

    console.log("Response cards for deck " + deck_id);
    console.log(response.data);

    if (response.data.length > 0) {
      notEmptyDecks.push(decks.value[i]);
    }
  }

  return notEmptyDecks;
};

const fetchDecks = async () => {
  try {
    if (favoriteOnly.value) {
      if (!authStore.isLoggedIn) {
        return;
      }

      const response = await api.get("favourites");

      // Get the decks from the favourites (deck_object)
      decks.value = response.data.map((favourite) => favourite.deck_object);

      console.log("Decks");
      console.log(response.data);
    } else {
      const response = await api.get("decks");

      console.log("Decks");
      console.log(response.data);
      decks.value = response.data;
    }

    // Remove empty decks
    decks.value = await removeEmptyDeck();

    search();
  } catch (error) {
    console.log(error);
  }
};

const search = async () => {
  if (searchText.value != null && searchText.value != "") {
    displayedDecks.value = decks.value.filter((deck) =>
      deck.name.toLowerCase().includes(searchText.value.toLowerCase())
    );
  } else {
    displayedDecks.value = decks.value;
  }
};

const onClick = (deckId) => {
  selectedDeckId.value = deckId;

  emit("onSelectDeck", deckId);
};

onMounted(() => {
  fetchDecks();
  search();
});
</script>

<template>
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

    <!-- Filtrer par favoris -->
    <q-toggle
      v-if="authStore.isLoggedIn"
      v-model="favoriteOnly"
      @click="fetchDecks"
      label="Favorites"
      color="primary"
      class="q-ma-sm"
    />

    <!-- Liste des decks -->
    <div>
      <q-list>
        <div v-for="(deck, index) in displayedDecks" :key="index">
          <q-item clickable :active="selectedDeckId == deck.id">
            <q-item-section clickable @click="onClick(deck.id)">
              <q-item-label>{{ deck.name }}</q-item-label>
              <q-item-label caption lines="2">{{
                deck.user_object.username
              }}</q-item-label>
            </q-item-section>
            <!-- Bouton add -->
            <!-- <q-item-section side>
              <q-btn class="q-mt-sm" color="primary" @click="() => {}" icon="add" flat />
            </q-item-section> -->
          </q-item>
          <q-separator spaced inset />
        </div>

        <!-- If no decks found, display message -->
        <div v-if="displayedDecks.length == 0">
          <q-item>
            <q-item-section>
              <q-item-label>No decks found</q-item-label>
            </q-item-section>
          </q-item>
        </div>
      </q-list>
    </div>
  </div>
</template>
