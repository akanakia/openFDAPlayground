import Vue from 'vue';
import VueRouter from 'vue-router';
import OpenFdaQA from '../views/OpenFdaQA.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'OpenFdaQA',
    component: OpenFdaQA,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
