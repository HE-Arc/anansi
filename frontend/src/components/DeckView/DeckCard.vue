<script setup>
import { ref, onMounted, getCurrentInstance, defineEmits } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuasar } from "quasar";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();

const router = useRouter();
const route = useRoute();

const emit = defineEmits(["delete-card"]);

const props = defineProps({
  isDeckMine: {
    default: false,
  },
  card: {
    default: null,
  },
  cardType: {
    default: "cloze",
  },
});

const deleteCard = async (id) => {
  emit("delete-card", id, props.cardType);
};

const editCard = async (id, cardId) => {
  router.push(`/mydecks/${id}/cards/${props.cardType}/${cardId}/edit`);
};

const addToDeck = async (id) => {
  //await fetch(`http://localhost:3000/clozecards/${id}`, {
  //  method: "PUT",
  //});
  //fetchClozeCards();
};

const clozeCardText = (text, index) => {
  const words = text.split(" ");
  return words.slice(0, index).join(" ") + " __________ " + words.slice(index).join(" ");
};
</script>

<template>
  <q-card
    style="
      width: 100%;
      height: 100%;
      justify-content: space-between;
      display: flex;
      flex-direction: column;
    "
    class="text-white text-bold"
    :class="cardType == 'cloze' ? 'bg-blue-5' : 'bg-red-5'"
  >
    <div class="col-12">
      <q-card-section>
        <div v-if="props.cardType == 'cloze'">
          {{ clozeCardText(card.text, card.gap_index) }}
        </div>
        <div v-else>
          {{ card.text }}
        </div>
      </q-card-section>
    </div>
    <div class="col-12">
      <q-separator dark />
      <q-card-actions align="right" class="bg-white q-pa-xs">
        <div v-if="isDeckMine">
          <!-- delete button -->
          <q-btn
            class="q-px-xs"
            color="primary"
            @click="deleteCard(card.id)"
            icon="delete"
            flat
          />
          <!-- edit button -->
          <q-btn
            class="q-px-xs"
            color="primary"
            @click="editCard(card.deck, card.id)"
            icon="edit"
            flat
          />
        </div>
        <div v-else>
          <!-- add to deck button -->
          <q-btn
            class="q-px-xs"
            color="primary"
            @click="addToDeck(card.id)"
            icon="add"
            flat
          />
        </div>
      </q-card-actions>
    </div>
  </q-card>
</template>
