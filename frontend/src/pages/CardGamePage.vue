<template>
  <q-page class="row items-center justify-evenly">
    <div class="row">
      <h1>My cards game</h1>
      <!--Bouton ajout nouveau jeu de <carte-->
      <q-btn
        color="primary"
        @click="() => $router.push('/mycardsgame/create')"
        icon="add"
      />
    </div>
    <div>
      <!-- Si il n'y a pas de jeu de carte, afficher un message -->
      <div v-if="cardGames.length === 0">
        <h2>There is no card game</h2>
      </div>
      <div v-else>
      <!--Liste de tous les jeux de cartes. à droite de chaque ligne, un bouton modifier et supprimer-->
      <q-card v-for="cardGame in cardGames" :key="cardGame.id">
        <q-card-section>
          <div class="text-h6">{{ gameCard.name }}</div>
        </q-card-section>
        <q-card-section>
          <q-btn
            color="primary"
            @click="() => console.log('edit')"
            icon="edit"
          />
          <q-btn
            color="primary"
            @click="() => console.log('delete')"
            icon="delete"
          />
        </q-card-section>
      </q-card>
    </div>
    </div>
  </q-page>
</template>

<script>

import { ref, onMounted } from 'vue';

const cardGames = ref([]);

export default {
  name: 'CardGamePage',
  data() {
    return {
      cardGames,
    };
  },
  methods: {
    async fetchCardGames() {
      const response = await this.$axios.get('http://127.0.0.1:8000/api/cardgames', {
        withCredentials: true,
        /*headers: {
          'X-CSRFToken': this.$axios.get('http://127.0.0.1:8000/api/csrf'),
        },*/
      });
      console.log(response.data);
      // eslint-disable-next-line vue/no-mutating-props
      this.cardGames = response.data;
    },
  },
  mounted() {
    this.fetchCardGames();
  },
};
</script>
