<template>
  <h1>New card game</h1>
  <form @submit.prevent="createCardGame">
    <q-input
      v-model="name"
      label="Name"
      type="text"
      :rules="[val => !!val || 'Name is required']"
    />
    <!-- Privacy : private or public, with icon -->
    <q-select
      v-model="privacy"
      label="Privacy"
      :options="['private', 'public']"
      :rules="[val => !!val || 'Privacy is required']"
    />
    <q-btn type="submit" color="primary" label="Create" no-caps class="full-width q-my-md" />
  </form>
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'CreateCardGamePage',
  setup() {
    const name = ref('');
    const privacy = ref('');

    return {
      name,
      privacy,
    };
  },
  methods: {
    async createCardGame(){
      try {
        /*const test = await this.$axios.get('http://127.0.0.1:8000/api/session/', {
          withCredentials: true,
        });
        console.log(test);*/

        const userId = await this.$api.get('userid', {
          withCredentials: true,
        });

        console.log(userId.data.userId);

        const response = await this.$api.post('cardgames/', {
          name: this.name,
          privacy: this.privacy,
          user: userId.data.userId,
        });

        console.log(response);
        this.$router.push({ name: 'mycardgames' });
      } catch (error) {
        console.log(error);
      }
    }
  },
});
</script>
