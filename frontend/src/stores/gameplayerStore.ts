import { defineStore } from 'pinia';

export const GameplayerStore = defineStore('GameplayerStore', {
  state: () => ({
    username: '',
    is_anon: true,
    game_id: 0,
    gameplayer_id: 0,
  }),

  getters: {
    getAnonUsername(): string {
      return this.username;
    },

    getIsAnon(): boolean {
      return this.is_anon;
    },

    getGameId(): number {
      return this.game_id;
    },

    getGameplayerId(): number {
      return this.gameplayer_id;
    }
  },

  actions: {
    setUsername(username: string): void {
      this.username = username;
    },

    setIsAnon(is_anon: boolean): void {
      this.is_anon = is_anon;
    },

    setGameId(game_id: number): void {
      this.game_id = game_id;
    },

    setGameplayerId(gameplayer_id: number): void {
      this.gameplayer_id = gameplayer_id;
    },

    // Randomly generate a username
    generateAnonUsername(): string {
      const adjectives = ['Anonymous', 'Brave', 'Clever', 'Determined', 'Energetic', 'Friendly', 'Gentle', 'Happy', 'Kind', 'Lucky', 'Nice', 'Polite', 'Quiet', 'Rich', 'Shy', 'Talented', 'Witty'];

      const nouns = ['Ant', 'Bear', 'Cat', 'Dog', 'Elephant', 'Frog', 'Giraffe', 'Horse', 'Iguana', 'Jaguar', 'Kangaroo', 'Lion', 'Monkey', 'Narwhal', 'Octopus', 'Penguin', 'Quail', 'Rabbit', 'Snake', 'Tiger', 'Unicorn', 'Vulture', 'Whale', 'X-Ray Tetra', 'Yak', 'Zebra'];

      const randomAdjective = adjectives[Math.floor(Math.random() * adjectives.length)];

      const randomNoun = nouns[Math.floor(Math.random() * nouns.length)];

      const randomNum = Math.floor(Math.random() * 1000);

      const username = `${randomAdjective}${randomNoun}${randomNum}`;

      this.setUsername(username);

      console.log(`Generated username: ${username}`);

      return username;
    }
  }
});
