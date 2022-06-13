<template>
    <v-app>
        <v-container class="container">
            <!-- Form for putting title and text -->
            <div class="main">
                <form action="#">
                    <input v-model="titleValue" class="main__url" type="text"
                        placeholder="Вставьте заголовок новости" />
                    <v-textarea v-model="originalText" class="main__textarea" filled auto-grow label="Вставьте текст"
                        rows="6" color="green" row-height="58">
                    </v-textarea>
                    <v-btn @click="goto('res'); titleSend(); textSend();" class="main__button" color="green" block>
                        Проверить
                    </v-btn>
                </form>
                <br />
                <!-- Result conateiner for news convert -->
                <!-- main end -->
            </div>
            <!-- Image side for steps -->
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

        <!-- Result pointers -->

        <div ref="res" id="result">
            <img class="navbar__img" src="../assets/images/Logo.png" alt="" />
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
            <div>
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
        </div>

        <!-- Result text -->
        <div class="result_text">
            <div class="original_text">
                <h4>{{originalTextSend}}</h4>
            </div>
        </div>
    </v-app>

</template>

<script>
export default {
  data() {
        return {
            titleValue: '',
            titlePosted: '',
            originalText: '',
            originalTextSend: '',
      valueTrue: "0%",
      valueWhite: "0%",
      valuePositive: "0%",
    };
  },

  methods: {
      isDisable() {
          return this.titleValue.length > 0;
      },
      textSend() {
          this.originalTextSend = this.originalText;  
},
      titleSend() {
          this.titlePosted = this.titleValue;
          (this.valueTrue = "75%");
      },
      goto(refName) {
          const element = this.$refs[refName];
          const top = element.offsetTop;
          window.scrollTo(0, top);
    }
  },
};
</script>

<style></style>
