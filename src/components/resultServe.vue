<template>
    <v-container class="container">
        <div class="main">
            <form action="#">
                <input v-model="titleValue" class="main__url" type="text" placeholder="Вставьте заголовок новости" />
                <v-textarea class="main__textarea" filled auto-grow label="Вставьте текст" rows="6" color="green"
                    row-height="58">
                </v-textarea>
                <v-btn @click="titleSend" class="main__button" color="green" block>
                    Проверить
                </v-btn>
            </form>
            <br />
            <div class="main__progress">
                <div>
                    <v-avatar color="grey" size="60">0</v-avatar>
                    <h4>Искажения</h4>
                </div>
                <div>
                    <v-avatar color="grey" size="60">0</v-avatar>
                    <h4>Вбросы </h4>
                </div>
                <div>
                    <v-avatar color="grey" size="60">0</v-avatar>
                    <h4>Прямые цитаты</h4>
                </div>
                <div>
                    <v-avatar color="grey" size="60">0</v-avatar>
                    <h4>Источники</h4>
                </div>
            </div>
            <v-alert class="main__pointer" border="left" color="green" elevation="2">
                <div>

                    <v-progress-circular :size="75" :width="15" :value="valueTrue" color="white">
                       {{valueTrue}}
                    </v-progress-circular>
                </div>

                <div>
                    <h4>{{titlePosted}}</h4>
                </div>
            </v-alert>
        </div>

        <!-- Result -->

        <div>
            <v-stepper value="3">
                <v-stepper-header style="price">
                    <v-stepper-step complete editable step="1">
                        Поставьте заголовок новости
                    </v-stepper-step>

                    <v-divider></v-divider>

                    <v-stepper-step complete editable step="2">
                        Поместите текст новости
                    </v-stepper-step>

                    <v-divider></v-divider>

                    <v-stepper-step complete step="3">
                        Проверенный результат
                    </v-stepper-step>
                </v-stepper-header>
            </v-stepper>
            <img class="fake-image" src="../assets/images/fake.jpg" alt="" />
        </div>

    </v-container>
</template>

<script>
export default {
  data() {
        return {
            titleValue: '',
            titlePosted: '',
      valueTrue: "0%",
      valueWhite: "0%",
      valuePositive: "0%",
    };
  },

  methods: {

      titleSend() {
          this.titlePosted = this.titleValue;
          (this.valueTrue = "75%");
    }
  },
};
</script>

<style></style>
