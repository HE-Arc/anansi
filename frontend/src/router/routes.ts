import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  /*{
    path: '/',
    name: 'home',
    alias: ['/home', '/index'],
    component: () => import('pages/IndexPage.vue'),
  },*/
  {
    path: '/login',
    name: 'login',
    component: () => import('src/pages/Auth/LoginPage.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('src/pages/Auth/RegisterPage.vue'),
  },
  {
    path: '/favourites',
    name: 'favourites',
    component: () => import('src/pages/Deck/FavouritePage.vue'),
  },
  {
    path: '/mydecks/:id/cards/create',
    name: 'cards.create',
    props: true,
    component: () => import('src/pages/MyDeck/CreateCardPage.vue')
  },
  {
    path: '/mydecks/:id/cards/:cardType/:cardId/edit',
    name: 'cards.edit',
    props: true,
    component: () => import('src/pages/MyDeck/EditCardPage.vue')
  },
  {
    path: '/mydecks',
    name: 'mydecks',
    component: () => import('src/pages/MyDeck/MyDecksPage.vue')
  },
  {
    path: '/mydecks/create',
    name: 'mydecks.create',
    component: () => import('src/pages/MyDeck/CreateDeckPage.vue')
  },
  {
    path: '/mydecks/:id',
    name: 'mydecks.id',
    props: true,
    component: () => import('src/pages/MyDeck/MyDeckPage.vue')
  },
  {
    path: '/decks',
    name: 'decks',
    component: () => import('src/pages/Deck/DecksPage.vue')
  },
  {
    path: '/decks/:id',
    name: 'decks.id',
    props: true,
    component: () => import('src/pages/Deck/DeckPage.vue')
  },
  {
    path: '/game',
    name: 'game',
    alias: ['/', '/home', '/index'],
    component: () => import('src/pages/Game/GameIndex.vue')
  },
  {
    path: '/game/:id',
    name: 'game.id',
    props: true,
    component: () => import('src/pages/Game/WaitingRoom.vue')

  },
  {
    path: '/game',
    name: 'game',
    component: () => import('src/pages/Game/GameIndex.vue')
  },
  {
    path: '/game/:id',
    name: 'game.id',
    props: true,
    component: () => import('src/pages/Game/WaitingRoom.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
