<script setup>
import { ref, onMounted, defineProps, watch, defineEmits, computed } from "vue";

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
  defaultStyle: {
    default: true,
  },
});

const style = computed(() => {
  return props.defaultStyle
    ? ""
    : "width: 100%;height: 100%;justify-content: space-between;display: flex;flex-direction: column;";
});

const onSelect = () => {
  emit("onSelect", props.card);
};
</script>

<template>
  <q-card
    :clickable="action"
    @click="onSelect"
    class="bg-red-6 text-white"
    :style="style"
  >
    <q-card-section>
      <!-- Display card text -->
      {{ props.masterSelection ? props.card.response_card_object.text : props.card.text }}
    </q-card-section>
  </q-card>
</template>
