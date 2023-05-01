<script setup>
import { ref, onMounted, defineEmits } from "vue";

const emits = defineEmits(["onSelect"]);

const props = defineProps({
  card: {
    default: null,
  },
  can_select: {
    default: false,
  },
  width: {
    default: 200,
  },
  height: {
    default: 200,
  },
});

const card_text = ref("");
const card_type = ref("");
const card_selected = ref(false);

const emitCardSelected = () => {
  console.log("Card selected");
  card_selected.value = true;
  emits("onSelect", props.card);
};

onMounted(() => {
  card_text.value = props.card.text;
  card_type.value = props.card.type;
});
</script>

<template>
  <q-card
    class="my-card col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2"
    :style="{ width: width + 'px', height: height + 'px', background: card_selected ? 'green' : 'red' }"
  >
    <!-- Display card text, and change color based on the type -->
    <q-card-section class="text-h6 text-white" :class="card_type">
      {{ card_text }}

      <q-btn
        v-if="can_select"
        style="background: blue; color: white"
        label="Choose"
        @click="emitCardSelected"
      />
    </q-card-section>
  </q-card>
</template>

<style></style>
