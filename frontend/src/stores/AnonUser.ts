import { defineStore } from 'pinia';

export const anonUserStore = defineStore('anonUser', {
  state: () => ({
    anonUsername: '',
  }),

  getters: {
    getAnonUsername(): string {
      return this.anonUsername;
    }
  },

  actions: {
    setAnonUsername(username: string): void {
      this.anonUsername = username;
    },

    // Randomly generate a username
    generateAnonUsername(): void {
      const adjectives = ['Anonymous', 'Brave', 'Clever', 'Determined', 'Energetic', 'Friendly', 'Gentle', 'Happy', 'Kind', 'Lucky', 'Nice', 'Polite', 'Quiet', 'Rich', 'Shy', 'Talented', 'Witty'];

      const nouns = ['Ant', 'Bear', 'Cat', 'Dog', 'Elephant', 'Frog', 'Giraffe', 'Horse', 'Iguana', 'Jaguar', 'Kangaroo', 'Lion', 'Monkey', 'Narwhal', 'Octopus', 'Penguin', 'Quail', 'Rabbit', 'Snake', 'Tiger', 'Unicorn', 'Vulture', 'Whale', 'X-Ray Tetra', 'Yak', 'Zebra'];

      const randomAdjective = adjectives[Math.floor(Math.random() * adjectives.length)];

      const randomNoun = nouns[Math.floor(Math.random() * nouns.length)];

      const randomNum = Math.floor(Math.random() * 1000);

      const username = `${randomAdjective}${randomNoun}${randomNum}`;

      this.setAnonUsername(username);

      console.log(`Generated username: ${username}`);
    }
  }
});
