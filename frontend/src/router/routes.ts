import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    alias: ['/home', '/index'],
    component: () => import('pages/IndexPage.vue'),
  },
  /*{
    path: '/',
    component: () => import('layouts/AppLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/login', component: () => import('pages/LoginPage.vue') },
      { path: '/register', component: () => import('pages/RegisterPage.vue') },
      { path: '/mycardgames', component: () => import('pages/CardGamePage.vue') },
    ]
    //component: () => import('pages/IndexPage.vue'),
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
    path: '/mycardgames',
    name: 'mycardgames',
    component: () => import('src/pages/CardGame/CardGamePage.vue')
  },
  {
    path: '/mycardgames/create',
    name: 'cardgames.create',
    component: () => import('src/pages/CardGame/CreateCardGamePage.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
