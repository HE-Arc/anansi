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
            :options="['private', 'public']"
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

export default defineComponent({
  name: "CreateCardGamePage",
  setup() {
    const name = ref("");
    const privacy = ref("");

    return {
      name,
      privacy,
    };
  },
  methods: {
    async createCardGame() {
      try {
        const response = await this.$api.post("cardgames/", {
          name: this.name,
          privacy: this.privacy,
        });

        console.log(response);
        this.$router.push({ name: "mycardgames" });
      } catch (error) {
        console.log(error);
      }
    },
  },
});
</script>
