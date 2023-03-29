import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    alias: ['/home', '/index'],
    component: () => import('pages/IndexPage.vue'),
  },
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
    path: '/mycardgames',
    name: 'mycardgames',
    component: () => import('src/pages/CardGame/CardGamePage.vue')
  },
  {
    path: '/mycardgames/create',
    name: 'cardgames.create',
    component: () => import('src/pages/CardGame/CreateCardGamePage.vue')
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
  {
    path: '/mycardgames/open',
    name: 'cardgames.open',
    component: () => import('src/pages/CardGame/CardPage.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
