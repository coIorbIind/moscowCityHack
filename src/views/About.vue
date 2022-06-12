<template>
  <div class="about">
    <!-- navbar -->
    <v-app-bar
      elevation="4"
      border="top"
      class="navbar"
      color="black lighten-2"
      dark
    >
      <div class="navbar__brand">
        <img class="navbar__img" src="../assets/images/Logo.png" alt="" />
      </div>
    </v-app-bar>
    <!-- Body part -->

    <resultServe />
  </div>
</template>

<script>
import resultServe from "../components/resultServe.vue";
// import mainServe from '../components/mainServe.vue'
export default {
  components: {
    // mainServe,
    resultServe,
  },
};
</script>

<style></style>
