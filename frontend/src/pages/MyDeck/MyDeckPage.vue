<script setup>
import DeckView from "src/components/DeckView/DeckView.vue";
import { ref, onMounted, getCurrentInstance } from "vue";
import { useRoute } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const route = useRoute();

const deck = ref({});

const fetchDeck = async () => {
  try {
    const response = await api.get(`mydecks/${route.params.id}`);
    deck.value = response.data;
  } catch (error) {
    console.log(error);
  }
};

onMounted(() => {
  fetchDeck();
});
</script>

<template>
  <q-page class="row justify-center">
    <div class="col-xs-11">
      <div class="row justify-between q-px-none q-py-none q-my-none">
        <h1 class="q-my-none q-py-none">{{ deck.name }}</h1>
        <!-- Create card -->
        <q-btn
          class="q-mt-sm"
          color="primary"
          icon="add"
          flat
          :to="{ name: 'cards.create' }"
          size="lg"
        />
      </div>
      <DeckView :id="route.params.id" :isDeckMine="true"></DeckView>
    </div>
  </q-page>
</template>
