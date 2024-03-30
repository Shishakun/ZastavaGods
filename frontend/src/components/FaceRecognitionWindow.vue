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
          <Loader v-if="isLoading" />
          <button
            v-else
            @click="takeSnapshot"
            class="w-24 h-24 border-[3px] border-red-600 rounded-full mt-4"
          ></button>
          <p class="text-4xl text-white">{{ serverResponse }}</p>
        </div>
        <div
          class="flex flex-col border-[1px] justify-between border-activeText w-[35vw] h-[83vh] rounded-xl"
        >
          <img :src="getImage" class="rounded-t-xl h-[68vh]" />
          <div class="text-activeText px-4 py-6 text-xl">
            <p>ФИО: {{ surname }} {{ name }} {{ patronymic }}</p>
            <p>Отдел: {{ otdel }}</p>
            <p>Уровень допуска: {{ secret }}</p>
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
import Loader from "./Loader.vue";
export default {
  components: {
    TextOutput,
    SidebarMain,
    TranslaterLoader,
    Alert,
    Loader,
  },
  data() {
    return {
      serverResponse: "",
      isLoading: false,
      isReady: false,
      name: "",
      surname: "",
      patronymic: "",
      otdel: "",
      secret: "",
      photo_path: "",
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
      if (response.ok) {
        const data = await response.json();
        if (data) {
          // Handle the user data
          this.surname = data.message.surname;
          this.name = data.message.name;
          this.patronymic = data.message.patronymic;
          this.otdel = data.message.otdel;
          this.secret = data.message.secret;
          this.photo_path = data.message.image_path;
        } else if (data.message === "No user found.") {
          // Handle the case where the user is not found
          console.log("No user found.");
          this.isReady = false;
        } else if (data.message === "No face detected.") {
          // Handle the case where no face is detected in the image
          console.log("No face detected.");
          this.isReady = false;
        }
      } else {
        const error = await response.json();
        console.log(error.message);
        this.isReady = false;
      }
    },
  },
  async mounted() {
    const constraints = { video: true };
    const stream = await navigator.mediaDevices.getUserMedia(constraints);

    const video = this.$refs.video;
    video.srcObject = stream;
    video.play();
  },
  computed: {
    getImage() {
      return `http://localhost:8000/inputs/people/${this.photo_path}`;
    },
  },
};
</script>

<style></style>
