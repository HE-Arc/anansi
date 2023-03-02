<template>
  <q-page class="row justify-evenly content-start">
    <div class="col-11 col-md-6 col-lg-4">
      <div class="row justify-evenly align-center">
        <h1 class="q-my-sm">My card games</h1>
        <q-btn
          class="q-mt-sm"
          color="primary"
          @click="() => $router.push({ name: 'cardgames.create' })"
          icon="add"
          flat
        />
      </div>
    </div>
    <div class="col-10 col-md-6 col-lg-4">
      <!-- If no card games, display message -->
      <div v-if="cardGames.length == 0">
        <h2>There is no card game</h2>
      </div>
      <div v-else>
        <!-- Display card games -->
        <q-list separator>
          <q-item clickable v-for="cardGame in this.cardGames" :key="cardGame.id">
            <q-item-section>
              {{ cardGame.name }}
            </q-item-section>
            <!-- Privacy -->
            <q-item-section side>
              <q-btn
                class="q-px-xs"
                :color="cardGame.privacy == 'private' ? 'primary' : 'grey-8'"
                @click="() => editCardGamePrivacy(cardGame.id, cardGame.privacy)"
                icon="lock"
                flat
              />
            </q-item-section>
            <q-item-section side>
              <q-btn
                class="q-px-xs"
                color="primary"
                @click="() => editCardGameName(cardGame.id)"
                icon="edit"
                flat
              />
            </q-item-section>
            <q-item-section side>
              <q-btn
                class="q-px-xs"
                color="primary"
                @click="() => deleteCardGame(cardGame.id)"
                icon="delete"
                flat
              />
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted, defineComponent } from "vue";
import { isProxy, toRaw } from "vue";

export default defineComponent({
  name: "CardGamePage",
  data() {
    return {
      cardGames: ref([]),
      cardGamesArray: [],
    };
  },
  methods: {
    async fetchCardGames() {
      try {
        await this.$api.get("cardgames").then((response) => {
          this.cardGames = [];
          response.data.forEach((cardGame) => {
            this.cardGames.push({
              id: cardGame.id,
              name: cardGame.name,
              privacy: cardGame.privacy,
              user: cardGame.user,
              user_object: cardGame.user_object,
            });
          });
        });
      } catch (error) {
        console.log(error);
      }
    },
    async editCardGamePrivacy(id, lastPrivacy) {
      const response = await this.$api.patch(`cardgames/${id}/`, {
        privacy: lastPrivacy == "private" ? "public" : "private",
      });
      console.log(response);
      this.fetchCardGames();
    },
    async putchCardGame() {
      console.log("putch");
    },
    async deleteCardGame(id) {
      const response = await this.$api.delete(`cardgames/${id}/`);
      console.log(response);
      this.fetchCardGames();
    },
  },
  async mounted() {
    this.fetchCardGames();
  },
});
</script>
