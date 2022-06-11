<template>
    <div class="result">
        <div class="main__progress">

            <div>
                <v-progress-circular :rotate="360" :size="100" :width="15" value="0" color="green">
                    0%
                </v-progress-circular>
                <h4>Вероятность</h4>
            </div>
            <div>
                <v-progress-circular :rotate="360" :size="100" :width="15" value="0" color="yellow">
                    0%
                </v-progress-circular>
                <h4>Позитивность</h4>
            </div>
            <div>
                <v-progress-circular :rotate="360" :size="100" :width="15" value="0" color="white">
                    0%
                </v-progress-circular>
                <h4>Совпадений
                    в <br> белом
                    списке</h4>
            </div>
            
        </div>
        <div class="newsInfo">
            
            <h5>«Мегафон» и «Ростелеком» в середине марта отключили от точки обмена трафиком британской компании LINX. В
                отношении других российских клиентов, которые могут быть аффилированы с вышеназванными компаниями, LINX
                продолжила свою работу.
            </h5>
            <p>https://news.mail.ru/politics/51655415/?frommail=1</p>

        </div>
        <div class="newsInfo">
            <h5>«Мегафон» и «Ростелеком» в середине марта отключили от точки обмена трафиком британской компании LINX. В
                отношении других российских клиентов, которые могут быть аффилированы с вышеназванными компаниями, LINX
                продолжила свою работу.
            </h5>
            <p>https://news.mail.ru/politics/51655415/?frommail=1</p>

        </div>

    </div>
</template>

<script>
export default {

}
</script>

<style>

</style>