<script setup>
import { ref, getCurrentInstance } from "vue";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/General/ErrorBanner.vue";
import { useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const router = useRouter();

const options = [
  { label: "Private", value: "private" },
  { label: "Public", value: "public" },
];

const name = ref("");
const privacy = ref(options[0]);
const errors = ref([]);

const createCardGame = async () => {
  try {
    await api.post("mydecks/", {
      name: name.value,
      privacy: privacy.value.value,
    });

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
    <div class="col-lg-5 col-md-8 col-sm-12 col-12 q-mx-lg-xl q-px-xl q-mt-md">
      <!-- Back button -->
      <q-btn
        class="q-ma-none q-pa-none"
        flat
        color="primary"
        no-caps
        icon="arrow_back"
        @click="router.go(-1)"
      ></q-btn>

      <div class="row justify-center">
        <div class="col-12">
          <h1 class="q-mt-none">New deck</h1>

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
    </div>
  </q-page>
</template>
