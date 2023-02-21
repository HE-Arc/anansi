<template>
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
      :width="220"
      >
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
          <img src="../assets/limite-limite-logo.png">
        </q-avatar>
        </q-item>

        <q-item v-for="link in filteredLinksList" :key="link.title" v-bind="link" clickable :to="{ name: link.link }" :class="(link.link == this.$route.name) ? 'bg-pink-1' : ''" @click="link.action">
          <q-item-section avatar>
            <q-icon :name="link.icon" :color="(link.link == this.$route.name) ? 'primary' : 'grey-6'" />
          </q-item-section>
          <q-item-section class="text-black">{{ link.title }}</q-item-section>
          <q-item-section side>
            <q-icon :name="(link.link == this.$route.name) ? 'chevron_left': 'chevron_right'" :color="(link.link == this.$route.name) ? 'primary' : 'grey-6'" />
          </q-item-section>
        </q-item>
      </q-list>

    </q-drawer>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useAuthStore } from 'src/stores/auth';

export default defineComponent({
  name: 'NavBar',
  methods: {
    async logout() {
      const response = await this.$axios.post('http://127.0.0.1:8000/api/logout/', { withCredentials: true });
      this.authStore.logout();
    },
  },
  data(){
    return {
      linksList: [
    {
      title: 'Home',
      link: 'home',
      icon: 'home',
    },
    {
      title: 'Play',
      link: 'play',
      icon: 'sports_esports',
    },
    {
      title: 'My card games',
      link: 'mycardgames',
      icon: 'dashboard',
      authRequired: true
    },
    {
      title: 'About',
      link: 'about',
      icon: 'info',
    },
    {
      title: 'Login',
      link: 'login',
      icon: 'account_circle',
    },
    {
      title: 'Logout',
      link: 'logout',
      icon: 'logout',
      authRequired: true,
      action: this.logout
    },
    {
      title: 'Parameters',
      link: 'parameters',
      icon: 'settings',
    }
  ]
    }
  },
  setup() {
    const authStore = useAuthStore();

    const leftDrawerOpen = ref(false);

    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value;
    };

    return {
      authStore,
      leftDrawerOpen,
      toggleLeftDrawer
    };
  },
  computed: {
    filteredLinksList() {
      if (this.authStore.get) {
        return this.linksList.filter(link => link.link != 'login');
      } else {
        return this.linksList.filter(link => !link.authRequired);
      }
    }
  },
});
</script>
