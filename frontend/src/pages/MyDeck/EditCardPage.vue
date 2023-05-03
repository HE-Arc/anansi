<script setup>
import { ref, onMounted, getCurrentInstance } from "vue";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/General/ErrorBanner.vue";
import { useRoute, useRouter } from "vue-router";

import { useToolsStore } from "src/stores/tools";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();

const router = useRouter();
const route = useRoute();

const errors = ref([]);

const card = ref({});
const cardType = ref(route.params.cardType);
const url = route.params.cardType === "response" ? "responsecards/" : "clozecards/";

const textResponse = ref("");
const text1 = ref("");
const text2 = ref("");

const fetchCard = async () => {
  const response = await api.get(`${url}${route.params.cardId}`);
  card.value = response.data;

  if (cardType.value === "response") {
    textResponse.value = card.value.text;
  } else {
    useToolsStore().rmExcessSpaces(card.value.text);
    text1.value = card.value.text.split(" ").slice(0, card.value.gap_index).join(" ");
    text2.value = card.value.text.split(" ").slice(card.value.gap_index).join(" ");
  }
};

const patchCard = async () => {
  if (cardType.value === "response") {
    card.value.text = textResponse.value;
    card.value.gap_index = null;
  } else {
    if (text1.value.length !== 0) {
      card.value.gap_index = useToolsStore().rmExcessSpaces(text1.value);
    }

    if (text2.value.length !== 0) {
      useToolsStore().rmExcessSpaces(text2.value);
    }

    card.value.text = text1.value + " " + text2.value;
  }

  try {
    await api.patch(`${url}${route.params.cardId}/`, card.value);

    $q.notify({
      message: "Card updated",
      color: "positive",
      icon: "check",
    });
    router.push(`/mydecks/${route.params.id}`);
  } catch (error) {
    console.log(error);
    errors.value = useToolsStore().validationErrors(error.response.data);
  }
};

onMounted(() => {
  fetchCard();
});
</script>

<template>
  <q-page class="row justify-center">
    <div class="col-12">
      <!-- Back button -->
      <q-btn
        class="q-ma-xs q-pa-xs"
        flat
        color="primary"
        no-caps
        icon="arrow_back"
        @click="router.go(-1)"
      ></q-btn>

      <div class="col-12 col-md-6 col-lg-4 q-mx-xl">
        <h1 class="q-mt-xs">Update card</h1>
        <!-- Error banner -->
        <ErrorBanner :errors="errors" />
        <form @submit.prevent="patchCard">
          <div v-if="cardType === 'response'">
            <q-input
              class="q-mt-sm"
              v-model="textResponse"
              label="Response"
              type="text"
              lazy-rules
              :rules="[(val) => !!val || 'Response is required']"
            />
          </div>
          <div v-else class="row items-end q-mb-md">
            <!-- First part input -->
            <q-input
              class="q-mt-sm"
              v-model="text1"
              label="Question"
              type="text"
              lazy-rules
            />

            <p class="q-pa-none q-my-none q-mx-sm">_________________</p>

            <!-- Second part input -->
            <q-input class="q-mt-sm" v-model="text2" label="" type="text" lazy-rules />
          </div>

          <q-btn class="q-mt-sm" color="primary" type="submit" label="Update" />
          <!-- Cancel button -->
          <q-btn
            class="q-mt-sm"
            flat
            color="primary"
            no-caps
            label="Cancel"
            @click="router.push(`/mydecks/${route.params.id}`)"
          />
        </form>
      </div>
    </div>
  </q-page>
</template>
