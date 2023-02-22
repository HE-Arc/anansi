<template>
  <q-page class="row items-center justify-evenly">
    <div class="row">
      <h1>My cards game</h1>
      <!--Bouton ajout nouveau jeu de <carte-->
      <q-btn
        color="primary"
        @click="() => $router.push({ name: 'cardgames.create' })"
        icon="add"
      />
    </div>
    <div>
      <!-- Si il n'y a pas de jeu de carte, afficher un message-->
      <div v-if="cardGames == undefined">
        <h2>There is no card game</h2>
      </div>
      <div v-else>
      <q-card v-for="cardGame in this.cardGames" :key="cardGame.id">
        <q-card-section>
          <div class="text-h6">{{ cardGame.name }}</div>
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

import { ref, onMounted, defineComponent } from 'vue';
import { isProxy, toRaw } from 'vue';

export default defineComponent({
  name: 'CardGamePage',
  data(){
    return {
      cardGames: ref([]),
      cardGamesArray: [],
    };
  },
  methods: {
    async fetchCardGames() {
      try{
        await this.$axios.get('http://127.0.0.1:8000/api/cardgames', {
          withCredentials: true,
        }).then(response => {
          this.cardGames = [];
          response.data.forEach(cardGame => {
            this.cardGames.push({
              id: cardGame.id,
              name: cardGame.name,
              privacy: cardGame.privacy,
              user: cardGame.user,
            });
          });
          if(isProxy(this.cardGames)){
            console.log("cardgames : ", this.cardGames);
          }
        });
      } catch (error) {
        console.log(error);
      }
    }
  },
  mounted() {
    this.fetchCardGames();
  }
});
</script>
