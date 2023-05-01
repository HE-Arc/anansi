<template>
  <!--Toolbar-->
  <q-header elevated>
    <q-toolbar class="bg-primary text-white">
      <q-btn flat round dense icon="menu" class="q-mr-sm" @click="toggleLeftDrawer" />
      <q-avatar square>
        <img src="../../assets/limite-limite-logo-white.png" />
      </q-avatar>
      <q-space />
      <q-btn flat round dense icon="account_circle" />
    </q-toolbar>
  </q-header>

  <!--Drawer-->
  <q-drawer v-model="leftDrawerOpen" show-if-above bordered :width="220">
    <q-list size="100px">
      <!-- Close button -->
      <q-item>
        <q-btn
          flat
          round
          dense
          icon="close"
          class="q-mr-sm"
          @click="toggleLeftDrawer"
          color="primary"
        />
      </q-item>

      <!-- Logo -->
      <q-item>
        <q-avatar square size="100px">
          <img src="../../assets/limite-limite-logo.png" />
        </q-avatar>
      </q-item>

      <q-item
        v-for="link in filteredLinksList"
        :key="link.title"
        v-bind="link"
        clickable
        :to="{ name: link.link }"
        :class="link.link == route.name ? 'bg-pink-1' : ''"
        @click="link.action"
      >
        <q-item-section avatar>
          <q-icon
            :name="link.icon"
            :color="link.link == route.name ? 'primary' : 'grey-6'"
          />
        </q-item-section>
        <q-item-section class="text-black">{{ link.title }}</q-item-section>
        <q-item-section side>
          <q-icon
            :name="link.link == route.name ? 'chevron_left' : 'chevron_right'"
            :color="link.link == route.name ? 'primary' : 'grey-6'"
          />
        </q-item-section>
      </q-item>
    </q-list>
  </q-drawer>
</template>

<script setup>
import { defineComponent, ref, onMounted, getCurrentInstance, watch } from "vue";
import { useAuthStore } from "src/stores/auth";
import { useQuasar } from "quasar";
import { useRoute, useRouter } from "vue-router";

const app = getCurrentInstance();
const api = app.appContext.config.globalProperties.$api;
const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const leftDrawerOpen = ref(false);

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value;
};

const logout = async () => {
  const response = await api.post("logout/");
  if (response.data["success"]) {
    $q.notify({
      message: "You have been logged out",
      color: "positive",
    });
    authStore.logout();
  } else {
    $q.notify({
      message: response.data["error"],
      color: "negative",
    });
  }
  authStore.logout();
  router.push({ name: "home" });
};

const filteredLinksList = ref([]);

const linksList = [
  {
    title: "Home",
    link: "home",
    icon: "home",
  },
  {
    title: "Play",
    link: "game",
    icon: "sports_esports",
  },
  {
    title: "Search decks",
    link: "decks",
    icon: "search",
  },
  {
    title: "Favourites",
    link: "favourites",
    icon: "favorite",
    authRequired: true,
  },
  {
    title: "My decks",
    link: "mydecks",
    icon: "dashboard",
    authRequired: true,
  },
  {
    title: "About",
    link: "about",
    icon: "info",
  },
  {
    title: "Login",
    link: "login",
    icon: "account_circle",
  },
  {
    title: "Logout",
    link: "logout",
    icon: "logout",
    authRequired: true,
    action: logout,
  },
];

const filterLinksList = () => {
  if (authStore.isLoggedIn) {
    filteredLinksList.value = linksList.filter((link) => {
      return link.link != "login";
    });
  } else {
    filteredLinksList.value = linksList.filter((link) => {
      return !link.authRequired;
    });
  }
};

onMounted(() => {
  filterLinksList();
});

watch(
  () => authStore.isLoggedIn,
  () => filterLinksList()
);

/*filteredLinksList() {
      if (this.authStore.get) {
        return this.linksList.filter((link) => link.link != "login");
      } else {
        return this.linksList.filter((link) => !link.authRequired);
      }
    },*/
</script>
