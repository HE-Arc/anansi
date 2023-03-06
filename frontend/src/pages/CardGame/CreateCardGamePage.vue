<template>
  <q-page class="row justify-center">
    <div class="col-12">
      <!-- Back button -->
      <q-btn
        class="q-ma-xs q-pa-xs"
        flat
        color="primary"
        :to="{ name: 'mycardgames' }"
        no-caps
        icon="arrow_back"
      ></q-btn>

      <div class="col-12 col-md-6 col-lg-4 q-mx-xl">
        <h1 class="q-mt-xs">New card game</h1>

        <!-- Error banner -->
        <ErrorBanner :errors="errors" />

        <!-- Form -->
        <form @submit.prevent="createCardGame">
          <!-- Name -->
          <q-input
            v-model="name"
            label="Name"
            type="text"
            :rules="[(val) => !!val || 'Name is required']"
          />

          <!-- Privacy -->
          <q-select
            v-model="privacy"
            label="Privacy"
            :options="options"
            :rules="[(val) => !!val || 'Privacy is required']"
          />
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

<script>
import { defineComponent, ref } from "vue";
import { useQuasar } from "quasar";
import ErrorBanner from "src/components/ErrorBanner.vue";

export default defineComponent({
  name: "CreateCardGamePage",
  components: {
    ErrorBanner,
  },
  data() {
    return {
      errors: ref([]),
    };
  },
  setup() {
    const name = ref("");
    const privacy = ref("");
    const $q = useQuasar();

    return {
      options: [
        { label: "Private", value: "private" },
        { label: "Public", value: "public" },
      ],
      $q,
      name,
      privacy,
    };
  },
  methods: {
    async createCardGame() {
      try {
        const response = await this.$api.post("cardgames/", {
          name: this.name,
          privacy: this.privacy.value,
        });

        this.$q.notify({
          message: "Card game created",
          color: "positive",
        });

        this.$router.push({ name: "mycardgames" });
      } catch (error) {
        this.errors = [];
        for (var key in error.response.data) {
          for (var key2 in error.response.data[key]) {
            this.errors.push(key + " : " + error.response.data[key][key2]);
          }
        }
      }
    },
  },
});
</script>
