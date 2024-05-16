<template>
  <div class="flex w-full justify-center p-6 gap-4 duration-500">
    <div class="fixed w-64 left-6">
      <SidebarMain />
    </div>
    <transition
      enter-active-class="transition ease-in-out duration-500 transform"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition ease-in-out duration-500 transform"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <Alert v-if="isError" @close="isError = false" />
    </transition>
    <div
      class="duration-500 min-h-[93vh] justify-center ml-72 items-center w-full bg-frameBackground rounded-xl outline-dashed outline-[1px] outline-outlineColor"
    >
      <div class="flex justify-between px-16 pt-6">
        <div class="flex flex-col items-center">
          <div class="">
            <button
              @click="toggleVideo"
              class="mt-4 w-full h-10 text-white rounded"
            >
              {{ isVideoOn ? "Выключить" : "Включить" }} видео
            </button>
          </div>
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
            :class="[
              isReady ? 'bg-green-600' : 'bg-red-600',
              'w-24 h-24 border-[3px] border-gray-400 rounded-full mt-4',
            ]"
          ></button>
          <p class="text-4xl text-white">{{ serverResponse }}</p>
        </div>
        <div
          class="flex flex-col border-[1px] justify-between border-activeText w-[35vw] min-h-[83vh] rounded-xl"
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
      isError: false,
      isReady: false,
      name: "",
      surname: "",
      patronymic: "",
      otdel: "",
      secret: "",
      photo_path: "",
      isVideoOn: false,
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
      this.isLoading = true;
      const response = await fetch("http://localhost:8000/facerecognition", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
      });

      if (response.ok) {
        const data = await response.json();
        this.isLoading = false;
        this.isReady = true;
        if (data) {
          // Handle the user data
          this.surname = data.message.surname;
          this.name = data.message.name;
          this.patronymic = data.message.patronymic;
          this.otdel = data.message.otdel;
          this.secret = data.message.secret;
          this.isLoading = false;
          this.photo_path = data.message.image_path;
          setTimeout(() => {
            this.surname = "";
            this.name = "";
            this.patronymic = "";
            this.otdel = "";
            this.secret = "";
            this.photo_path = "";
            this.isReady = false;
          }, 5000);
        }
      } else {
        const error = await response.json();
        console.log(error.message);
        this.isLoading = false;
        this.isError = true;
        setTimeout(() => {
          this.isError = false;
        }, 2000);
      }
    },
    toggleVideo() {
      if (!this.isVideoOn) {
        const constraints = { video: true };
        navigator.mediaDevices
          .getUserMedia(constraints)
          .then((stream) => {
            const video = this.$refs.video;
            video.srcObject = stream;
            video.play();
            this.isVideoOn = true;
          })
          .catch((error) => {
            console.error("Error accessing the camera:", error);
            // Handle error, show message to the user, etc.
          });
      } else {
        const video = this.$refs.video;
        const stream = video.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
        video.srcObject = null;
        this.isVideoOn = false;
      }
    },
  },

  computed: {
    getImage() {
      return `http://localhost:8000/inputs/people/${this.photo_path}`;
    },
  },
};
</script>

<style></style>
