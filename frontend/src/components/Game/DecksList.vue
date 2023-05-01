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

const emit = defineEmits(["onSelectDeck"]);

const fetchDecks = async () => {
  try {
    const response = await api.get("decks");
    decks.value = response.data;
    search();
  } catch (error) {
    console.log(error);
  }
};

const search = async () => {
  displayedDecks.value = decks.value.filter((deck) =>
    deck.name.toLowerCase().includes(searchText.value.toLowerCase())
  );

  // Filter by favorite
  // TODO : find a way to do it in the previous filter
};

const onClick = (deckId) => {
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
      v-model="favoriteOnly"
      label="Favorites"
      color="primary"
      class="q-ma-sm"
    />

    <!-- Liste des decks -->
    <div>
      <q-list>
        <div v-for="(deck, index) in displayedDecks" :key="index">
          <q-item clickable>
            <q-item-section clickable @click="onClick(deck.id)">
              <q-item-label>{{ deck.name }}</q-item-label>
              <q-item-label caption lines="2">{{
                deck.user_object.username
              }}</q-item-label>
            </q-item-section>
            <!-- Bouton add -->
            <q-item-section side>
              <q-btn class="q-mt-sm" color="primary" @click="() => {}" icon="add" flat />
            </q-item-section>
          </q-item>
          <q-separator spaced inset />
        </div>
      </q-list>
    </div>
  </div>
</template>
