<template>
  <q-page class="row justify-evenly content-start">
    <div class="col-11 col-md-6 col-lg-4">
      <div class="row justify-evenly align-center">
        <h1 class="q-my-sm">Name of the deck</h1>
        <q-btn class="q-mt-sm" color="primary" icon="add" flat />
        <div class="q-pa-md">
          <div class="q-gutter-y-md" style="max-width: 400px">
            <q-tabs v-model="tab" narrow-indicator dense align="justify">
              <q-tab class="text-purple" name="cloze" icon="help" label="Cloze cards" />
              <q-tab
                class="text-orange"
                name="respond"
                icon="priority_high"
                label="Respond cards"
              />
            </q-tabs>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    return {
      tab: ref("mails"),
    };
  },
};
</script>
