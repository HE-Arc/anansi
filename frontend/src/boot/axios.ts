import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';
import { useToolsStore} from './../stores/tools';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: 'http://127.0.0.1:8000/api', withCredentials: true});

// ajout d’un intercepteur de requête
api.interceptors.request.use(function (config) {
  console.log('intercepteur de requête');
  config.headers['accept'] = 'application/json';
  config.headers['content-type'] = 'application/json';
  config.withCredentials = true;

  // add headers if method is not safe
  if (config.method !== 'get' && config.method !== 'head' && config.method !== 'options') {
    config.headers['x-csrftoken'] = useToolsStore().readCookie('csrftoken');
  }

  return config;
}, function (error) {
  // faire quelque chose en cas d’erreur
  return Promise.reject(error);
});


export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
