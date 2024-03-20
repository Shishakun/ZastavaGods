<template>
  <div class="flex w-full justify-center p-6 gap-4 duration-500">
    <div class="fixed w-64 left-6">
      <SidebarMain />
    </div>
    <div
      class="duration-500 min-h-[90vh] justify-center ml-72 items-center w-full bg-frameBackground rounded-xl outline-dashed outline-[1px] outline-outlineColor"
    >
      <div class="flex justify-between px-16 pt-6">
        <div class="flex flex-col items-center">
          <div
            class="flex flex-col border-[1px] border-activeText w-[30vw] h-[67vh] rounded-xl"
          ></div>
          <div
            class="w-24 h-24 border-[1px] border-activeText rounded-full mt-4"
          ></div>
        </div>
        <div
          class="flex flex-col border-[1px] justify-between border-activeText w-[35vw] h-[83vh] rounded-xl"
        >
          <img src="../img/translator.jpg" class="rounded-t-xl h-[68vh]" />
          <div class="text-activeText px-4 py-6 text-xl">
            <p>ФИО: Шишкарев Захар Андреевич</p>
            <p>Отдел: 2 ЦС КГГ</p>
            <p>Уровень допуска: 2</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TextOutput from "./TextOutput.vue";
import TranslaterLoader from "./TranslaterLoader.vue";
import SidebarMain from "./SidebarMain.vue";
import Alert from "./Alert.vue";
export default {
  components: {
    TextOutput,
    SidebarMain,
    TranslaterLoader,
    Alert,
  },
  data() {
    return {
      isVideo: false,
      isAudio: false,
      uploadFile: "",
      files: [],
      url: "",
      text_language: "",
      text_massage: "",
      isLoading: false,
      isReady: false,
      isError: false,
    };
  },
  computed: {
    classes() {
      return this.isVideo ? "w-8/12" : ["w-8/12", "h-[570px]", "pt-8"];
    },
    audioClasses() {
      return this.isAudio
        ? ["flex", "flex-col", "mb-[600px]", "pt-8"]
        : ["flex", "flex-col", "pt-8"];
    },
  },
  methods: {
    handleFilesUpload() {
      this.uploadFile = this.$refs.files.files[0];
      this.url = URL.createObjectURL(this.uploadFile);
      this.files.push(this.uploadFile.name);
      console.log(this.files);
      if (this.uploadFile.type.startsWith("video")) {
        this.isVideo = true;
        this.isAudio = false;
      } else if (this.uploadFile.type.startsWith("audio")) {
        this.isAudio = true;
        this.isVideo = false;
      }
    },
    async submitFiles() {
      this.isLoading = true;
      const formData = new FormData();
      formData.append("file", this.uploadFile);
      console.log(formData);
      axios
        .post(
          `http://${process.env.VUE_APP_AUDIOREC_SERVICE_IP}/audio_sample`,
          formData,
          {
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
};
</script>

<style></style>
