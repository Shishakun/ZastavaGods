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
            class="flex flex-col border-[1px] border-activeText w-[30vw] rounded-xl"
          >
            <video
              class="h-full w-full rounded-xl"
              ref="video"
              autoplay
            ></video>
          </div>
          <button
            @click="takeScreenshot"
            class="w-24 h-24 border-[3px] border-red-600 rounded-full mt-4 bg-neutral-400"
          ></button>
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
    takeScreenshot() {
      // Capture screenshot from the video
      const canvas = document.createElement("canvas");
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;
      canvas
        .getContext("2d")
        .drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);
      const image = canvas.toDataURL("image/jpeg");

      // Send the captured image to the server for face recognition
      axios
        .post("http://localhost:8000/facerecognition", {
          image: image,
        })
        .then((response) => {
          console.log("Upload successful:", response.data);
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    },
  },
  mounted() {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        this.$refs.video.srcObject = stream;
      })
      .catch((error) => {
        console.log("Error accessing webcam:", error);
      });
  },
};
</script>

<style></style>
