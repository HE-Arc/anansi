<template>
  <q-layout view="lHh Lpr lFf">
    <!--Toolbar-->
    <q-header elevated>
      <q-toolbar class="bg-primary text-white">
      <q-btn flat round dense icon="menu" class="q-mr-sm" @click="toggleLeftDrawer" />
      <q-avatar square>
        <img src="../assets/limite-limite-logo-white.png">
      </q-avatar>

        <q-space />

        <q-btn flat round dense icon="account_circle" />
      </q-toolbar>
    </q-header>

    <!--Drawer-->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      >
      <q-list>

      </q-list>

    </q-drawer>

    <!--Page Container-->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'AppLayout',
  setup() {
    const leftDrawerOpen = ref(false);

    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value;
    };

    return {
      leftDrawerOpen,
      toggleLeftDrawer
    };
  }
});
</script>
