<template>
  <div class="flex w-full justify-center p-6 gap-4 duration-500">
    <div class="fixed w-64 left-6">
      <SidebarMain />
    </div>
    <div
      class="duration-500 min-h-[93vh] justify-start ml-72 items-center w-full bg-frameBackground rounded-xl outline-dashed outline-[1px] outline-outlineColor"
    >
      <div class="flex justify-center mb-4 pt-10">
        <p
          class="text-center text-4xl font-black font-mono text-activeText duration-500"
        >
          Распознавание окружения
        </p>
      </div>
      <div class="items-center px-14">
        <YamnetOutput />
      </div>
      <div class="flex items-center justify-center gap-4 px-14 pt-4">
        <div
          class="flex flex-col border-[1px] border-activeText w-1/2 h-[35vh] rounded-xl"
        >
          <canvas ref="chartCanvas" class="h-[35vh] rounded-xl p-1"> </canvas>
        </div>
        <div
          class="flex flex-col border-[1px] border-activeText w-1/2 h-[35vh] rounded-xl"
        >
          <img src="../img/123123.jpg" class="h-[35vh] rounded-xl p-1" />
        </div>
      </div>
      <div class="px-14 text-activeText pt-4 flex items-center">
        <p>Послушать онлайн:</p>
        <BaseIcon
          @click="takeRealTimeAudio"
          name="play"
          class="w-6 h-6 mt-2 ml-2"
        />
      </div>
      <div
        class="flex w-full justify-center px-14 py-4 gap-4 duration-500 min-h-[80vh]"
      >
        <div
          class="w-full border-[1px] border-activeText bg-frameBackground rounded-xl duration-500"
        >
          <p
            class="text-activeText duration-500 text-center pt-4 font-bold text-2xl"
          >
            Журнал событий
          </p>
          <div class="overflow-y-scroll custom-scrollbar"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";
import TextOutput from "./TextOutput.vue";
import TranslaterLoader from "./TranslaterLoader.vue";
import SidebarMain from "./SidebarMain.vue";
import YamnetOutput from "./YamnetOutput.vue";
import Alert from "./Alert.vue";
import BaseIcon from "./BaseIcon.vue";
export default {
  components: {
    TextOutput,
    TranslaterLoader,
    SidebarMain,
    YamnetOutput,
    Alert,
    BaseIcon,
  },
  data() {
    return {
      isPhoto: false,
      uploadFile: "",
      files: [],
      url: "",
      isError: false,
      text_language: "",
      text_massage: "",
      isLoading: false,
      isReady: false,
      origin_languages: ["русский", "английский"],
    };
  },
  computed: {
    classes() {
      return this.isPhoto ? "w-10/12" : ["w-10/12", "h-[500px]", "pt-8"];
    },
    isDarkMode() {
      return this.$store.state.darkMode;
    },
  },
  methods: {
    handleFilesUpload() {
      this.uploadFile = this.$refs.files.files[0];
      const typeFile = this.uploadFile.type;
      this.url = URL.createObjectURL(this.uploadFile);
      console.log(typeFile);
      this.files.push(this.uploadFile.name);
      console.log(this.files);
      if (
        this.uploadFile.type.startsWith("image") ||
        this.uploadFile.type.startsWith("application")
      ) {
        this.isPhoto = true;
      } else {
        this.isPhoto = false;
      }
    },
    scrollToBottom() {
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth",
      });
      this.submitFiles();
    },
    takeRealTimeAudio() {},
    async submitFiles() {
      this.isLoading = true;
      const formData = new FormData();
      formData.append("file", this.uploadFile);
      const language = this.language;
      console.log(language);
      console.log(formData);
      axios
        .post(
          `http://${process.env.VUE_APP_OCR_SERVICE_IP}/ocr_pdf_image`,
          formData,
          {
            params: {
              language,
            },
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((response) => {
          this.text_massage = response.data.text;
          this.text_language = response.data.language;
          this.isLoading = false;
          this.isReady = true;
          console.log(this.text_massage);
          console.log(this.text_language);
        })
        .catch(
          function (error) {
            console.log("Ошибка в обработке:", error);
            this.isLoading = false;
            this.isError = true;
          }.bind(this)
        );
    },
  },
  mounted() {
    this.ctx = this.$refs.chartCanvas.getContext("2d");
    this.chart = new Chart(this.ctx, {
      type: "line",
      data: {
        labels: [], // Массив для меток времени
        datasets: [
          {
            label: "Частота звука",
            data: [], // Массив для данных частоты звука
            borderColor: "blue",
            backgroundColor: "transparent",
          },
        ],
      },
      options: {
        animation: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  },
};
</script>
