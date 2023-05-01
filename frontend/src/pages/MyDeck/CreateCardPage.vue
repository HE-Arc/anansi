<script setup>
import { ref, onMounted, getCurrentInstance } from "vue";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/ErrorBanner.vue";
import { useRoute, useRouter } from "vue-router";
import { useToolsStore } from "src/stores/tools";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();

const router = useRouter();
const route = useRoute();

// radio buttons for card type
const cardType = ref("response");
const errors = ref([]);

const textResponse = ref("");
const text1 = ref("");
const text2 = ref("");

const card = ref({
  deck: route.params.id,
  type: cardType.value,
  text: "",
  gap_index: 0,
});

const createCard = async () => {
  const url = cardType.value === "response" ? "responsecards/" : "clozecards/";
  if (cardType.value === "response") {
    card.value.text = textResponse.value;
    card.value.gap_index = null;
  } else {
    if (text1.value.length !== 0) {
      /*text1.value = text1.value.split(" ");
      text1.value.forEach((word, index) => {
        if (word === "") {
          text1.value.splice(index, 1);
        }
      });
      card.value.gap_index = text1.value.length;
      text1.value = text1.value.join(" ");*/
      card.value.gap_index = useToolsStore().rmExcessSpaces(text1.value);
    }

    if (text2.value.length !== 0) {
      /*text2.value = text2.value.split(" ");
      text2.value.forEach((word, index) => {
        if (word === "") {
          text2.value.splice(index, 1);
        }
      });
      text2.value = text2.value.join(" ");*/
      useToolsStore().rmExcessSpaces(text2.value);
    }
    card.value.text = text1.value + " " + text2.value;
  }

  try {
    const response = await api.post(url, card.value);
    console.log(response.data);
    router.push({
      name: "mydecks.id",
      params: { id: route.params.id },
    });
  } catch (error) {
    console.log(error);
    errors.value = [];
    for (var key in error.response.data) {
      for (var key2 in error.response.data[key]) {
        errors.value.push(key + " : " + error.response.data[key][key2]);
      }
    }
  }
};
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
        <h1 class="q-mt-xs">New card</h1>
        <!-- Error banner -->
        <ErrorBanner :errors="errors" />
        <form @submit.prevent="createCard">
          <div>
            <q-option-group
              class="q-mt-sm"
              v-model="cardType"
              :options="[
                { label: 'Response', value: 'response' },
                { label: 'Question', value: 'question' },
              ]"
            />
          </div>
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

          <q-btn class="q-mt-sm" color="primary" type="submit" label="Create" />
        </form>
      </div>
    </div>
  </q-page>
</template>
