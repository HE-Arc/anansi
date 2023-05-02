<script setup>
import { ref, onMounted, defineProps, watch, defineEmits } from "vue";

const emit = defineEmits(["onSelect"]);

const props = defineProps({
  card: {
    default: {},
  },
  action: {
    default: false,
  },
  masterSelection: {
    default: false,
  },
});

const onSelect = () => {
  emit("onSelect", props.card);
};
</script>

<template>
  <q-card :clickable="action" @click="onSelect" class="q-ma-md" bordered>
    <q-card-section class="bg-red-6 text-white">
      <!-- Display card text -->
      {{ props.masterSelection ? props.card.response_card_object.text : props.card.text }}
    </q-card-section>
  </q-card>
</template>
