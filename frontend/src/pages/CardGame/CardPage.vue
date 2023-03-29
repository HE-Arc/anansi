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
            <q-tab-panels v-model="tab" animated>
              <!-- Cloze cards -->
              <q-tab-panel name="cloze">
                <q-card class="my-card">
                  <q-card-section class="bg-primary text-white">
                    <div class="text-h6">J'ai adoré ma première vidéo avec _____</div>
                  </q-card-section>
                  <q-separator />
                  <q-card-actions align="right">
                    <q-btn class="q-mt-sm" color="primary" icon="add" flat />
                    <q-btn class="q-mt-sm" color="primary" icon="delete" flat />
                  </q-card-actions>
                </q-card>

                <q-card class="my-card">
                  <q-card-section class="bg-primary text-white">
                    <div class="text-h6">J'aimerais trop enfilé _____</div>
                  </q-card-section>
                  <q-separator />
                  <q-card-actions align="right">
                    <q-btn class="q-mt-sm" color="primary" icon="add" flat />
                    <q-btn class="q-mt-sm" color="primary" icon="delete" flat />
                  </q-card-actions>
                </q-card>
              </q-tab-panel>

              <!-- Response cards -->
              <q-tab-panel name="respond">
                <q-card class="my-card">
                  <q-card-section class="bg-primary text-white">
                    <div class="text-h6">Jacquie et Michel</div>
                  </q-card-section>
                  <q-separator />
                  <q-card-actions align="right">
                    <q-btn class="q-mt-sm" color="primary" icon="add" flat />
                    <q-btn class="q-mt-sm" color="primary" icon="delete" flat />
                  </q-card-actions>
                </q-card>

                <q-card class="my-card">
                  <q-card-section class="bg-primary text-white">
                    <div class="text-h6">Ta mère</div>
                  </q-card-section>
                  <q-separator />
                  <q-card-actions align="right">
                    <q-btn class="q-mt-sm" color="primary" icon="add" flat />
                    <q-btn class="q-mt-sm" color="primary" icon="delete" flat />
                  </q-card-actions>
                </q-card>
              </q-tab-panel>
            </q-tab-panels>
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
