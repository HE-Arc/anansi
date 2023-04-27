<script setup>
import { ref, onMounted, defineProps, defineEmits } from "vue";

const props = defineProps({
  card: {
    default: null,
  },
  is_master: {
    default: false,
  },
  width: {
    default: 200,
  },
  height: {
    default: 200,
  },
});

const emits = defineEmits(["onSelect"]);

const card_id = ref(0);
const card_text = ref("");
const card_type = ref("");
const card_owner = ref("");
const is_master = ref(false);

onMounted(() => {
  card_id.value = props.card.id;
  card_text.value = props.card.text;
  card_type.value = props.card.type;
  card_owner.value = props.card.player_object.username;
  console.log(props.card);
  is_master.value = props.is_master;

  console.log("Is master : " + is_master.value);
});

const onCardSelectedByMaster = () => {
  emits("onSelect", card_id.value);
};
</script>

<template>
  <q-card
    class="my-card"
    style="width: {{ width }}px; height: {{ height }}px; background-color: red;"
  >
    <!-- Display card text, and change color based on the type -->
    <q-card-section class="text-h6 text-white" :class="card_type">
      {{ card_text }}
      <br />
      This card was selected by
      <span class="text-bold text-italic">{{ card_owner }}</span>
    </q-card-section>

    <!-- Select button if is master -->
    <q-card-actions v-if="is_master">
      <q-btn
        color="secondary"
        class="text-white"
        label="Select"
        @click="onCardSelectedByMaster"
      />
    </q-card-actions>
  </q-card>
</template>
