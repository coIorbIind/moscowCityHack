<template>
  <div class="main">
    <form action="#">
      <input
        class="main__url"
        type="text"
        placeholder="Вставьте заголовок новости"
      />
      <v-textarea
        class="main__textarea"
        filled
        auto-grow
        label="Вставьте текст"
        rows="4"
        color="green"
        row-height="55"
      >
      </v-textarea>
      <v-btn @click="valueBar" class="main__button" color="green" block>
        Проверить
      </v-btn>
    </form>
  </div>
</template>

<script>
export default {};
</script>

<style></style>
