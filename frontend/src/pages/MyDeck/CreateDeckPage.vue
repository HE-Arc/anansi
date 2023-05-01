<script setup>
import { ref, onMounted, getCurrentInstance } from "vue";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/ErrorBanner.vue";
import { useRoute, useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();

const router = useRouter();
const route = useRoute();

const name = ref("");
const privacy = ref("private");
const errors = ref([]);

const options = [
  { label: "Private", value: "private" },
  { label: "Public", value: "public" },
];

const createCardGame = async () => {
  try {
    const response = await api.post("mydecks/", {
      name: name.value,
      privacy: privacy.value,
    });

    console.log(response.data);

    $q.notify({
      message: "Card game created",
      color: "positive",
    });

    router.push({ name: "mydecks" });
  } catch (error) {
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
        <h1 class="q-mt-xs">New deck</h1>

        <!-- Error banner -->
        <ErrorBanner :errors="errors" />

        <!-- Formulaire de création de deck -->
        <form @submit.prevent="createCardGame">
          <!-- Nom -->
          <q-input
            v-model="name"
            label="Name"
            type="text"
            :rules="[(val) => !!val || 'Name is required']"
          />
          <!-- Visibilité -->
          <q-select
            v-model="privacy"
            label="Privacy"
            :options="options"
            :rules="[(val) => !!val || 'Privacy is required']"
          />
          <!-- Bouton de création -->
          <q-btn
            type="submit"
            color="primary"
            label="Create"
            no-caps
            class="full-width q-my-md"
          />
        </form>
      </div>
    </div>
  </q-page>
</template>
