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
            @click="takeSnapshot"
            class="w-24 h-24 border-[3px] border-red-600 rounded-full mt-4 bg-neutral-400"
          ></button>
          <p class="text-4xl text-white">{{ serverResponse }}</p>
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
      serverResponse: "",
    };
  },
  methods: {
    async takeSnapshot() {
      const video = this.$refs.video;
      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d");

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      const image = canvas.toDataURL("image/png");

      const response = await fetch("http://localhost:8000/facerecognition", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
      });

      const data = await response.json();
      const message = data.message;
      const firstDotIndex = message.indexOf(".");
      const result =
        firstDotIndex !== -1 ? message.substring(0, firstDotIndex) : message;

      this.serverResponse = result;
    },
  },
  async mounted() {
    const constraints = { video: true };
    const stream = await navigator.mediaDevices.getUserMedia(constraints);

    const video = this.$refs.video;
    video.srcObject = stream;
    video.play();
  },
};
</script>

<style></style>
