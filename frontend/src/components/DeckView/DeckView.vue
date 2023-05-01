<script setup>
import { useQuasar } from "quasar";
import { ref, onMounted, getCurrentInstance } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useRoute, useRouter } from "vue-router";
import DeckCard from "src/components/DeckView/DeckCard.vue";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const props = defineProps({
  isDeckMine: {
    default: false,
  },
  id: {
    default: null,
  },
});

const deck = ref(null);
const responseCards = ref([]);
const clozeCards = ref([]);

const tab = ref("cloze");

const fetchDeck = async () => {
  const response = await api.get(`decks/${props.id}`);
  deck.value = response.data;
};

const fetchResponseCards = async () => {
  const response = await api.get(`responsecards/get_responsecards`, {
    params: {
      deck: props.id,
    },
  });
  responseCards.value = response.data;
};

const fetchClozeCards = async () => {
  const response = await api.get(`clozecards/get_clozecards`, {
    params: {
      deck: props.id,
    },
  });
  clozeCards.value = response.data;
};

const deleteCardCallback = async (cardId, cardType) => {
  let url = "clozecards/";
  if (cardType === "response") {
    url = "responsecards/";
  }

  try {
    await api.delete(`${url}${cardId}/`);
    $q.notify({
      message: "Card deleted",
      color: "positive",
      icon: "check",
    });

    fetchClozeCards();
    fetchResponseCards();
  } catch (err) {
    console.log(err);
    $q.notify({
      message: "Error deleting card",
      color: "negative",
      icon: "warning",
    });
  }
};

onMounted(() => {
  fetchDeck();
  fetchResponseCards();
  fetchClozeCards();
});
</script>

<template>
  <!-- Template to show a deck with cloze cards and response cards tabs -->

  <div class="col-12 q-pt-none q-mt-none">
    <!-- Tabs : Response cards and Cloze cards -->
    <div class="q-lg-mb-xl q-sm-mb-sm">
      <q-tabs v-model="tab" align="justify" no-caps tab-style="text-align: left;">
        <q-tab name="cloze" label="Cloze cards" />
        <q-tab name="response" label="Response cards" />
      </q-tabs>
    </div>

    <!-- Cloze cards -->
    <div v-if="tab == 'cloze'" class="row justify-start" style="align-items: stretch">
      <!--class="row justify-between">  "-->
      <div v-if="clozeCards.length == 0" class="text-h6 text-center">
        No cloze cards in this deck
      </div>
      <div
        v-for="card in clozeCards"
        :key="card.id"
        class="col-xs-6 q-pa-xs-sm col-sm-4 col-md-3 col-lg-2 q-pa-md-md"
      >
        <DeckCard
          :card="card"
          :isDeckMine="props.isDeckMine"
          cardType="cloze"
          @delete-card="deleteCardCallback"
        ></DeckCard>
      </div>
    </div>

    <!-- Response cards -->
    <div v-if="tab == 'response'" class="row justify-start" style="align-items: stretch">
      <div v-if="responseCards.length == 0" class="text-h6 text-center">
        No response cards in this deck
      </div>
      <div
        v-for="card in responseCards"
        :key="card.id"
        style="align-content: space-between"
        class="col-xs-6 q-pa-xs-sm col-sm-4 col-md-3 col-lg-2 q-pa-md-md"
      >
        <DeckCard
          :card="card"
          :isDeckMine="props.isDeckMine"
          cardType="response"
          @delete-card="deleteCardCallback"
        ></DeckCard>
      </div>
    </div>
  </div>
</template>
