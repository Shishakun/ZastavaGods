<template>
  <div class="flex w-full justify-center p-6 gap-4 duration-500 min-h-[90vh]">
    <div class="fixed w-64 left-6">
      <SidebarMain />
    </div>
    <div
      class="ml-72 w-4/6 outline-dashed bg-frameBackground rounded-xl outline-[1px] outline-outlineColor duration-500"
    >
      <div class="h-full">
        <video
          class="h-full w-full rounded-xl p-1"
          ref="video"
          autoplay
        ></video>
      </div>
    </div>
    <div
      class="w-1/6 outline-dashed bg-frameBackground rounded-xl outline-[1px] outline-outlineColor duration-500"
    >
      <div class="min-h-full p-3">
        <p
          class="text-activeText pt-2 text-center rounded-xl mb-2 text-xl font-medium duration-500"
        >
          Все камеры
        </p>
        <div
          class="w-full px-2 overflow-y-scroll h-[80vh] custom-scrollbar duration-500"
        >
          <div
            class="text-activeText pt-2 w-full duration-500 flex flex-col gap-2"
          >
            <button
              class="border-2 flex gap-3 w-full rounded-xl px-3 py-2 items-center duration-300"
              v-for="i in 30"
              :key="i"
              :class="[
                'bg-[#272727] text-[#d5d5d5] items-center justify-center font-semibold rounded-xl px-2.5 py-1.5 duration-100 flex hover:bg-[#424242]',
                {
                  'bg-[#e7e7e7] text-[#272727] hover:bg-[#ebebeb]':
                    activeButton === i,
                },
              ]"
              @click="handleButtonClick(i)"
            >
              <BaseIcon name="camera" class="w-5 h-5" />
              Камера № {{ i }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    class="flex w-full justify-center px-6 py-4 gap-4 duration-500 min-h-[80vh]"
  >
    <div class="fixed hidden w-64 left-6">
      <SidebarMain />
    </div>
    <div
      class="ml-72 w-5/6 outline-dashed bg-frameBackground rounded-xl outline-[1px] outline-outlineColor duration-500"
    >
      <p
        class="text-activeText duration-500 text-center pt-4 font-bold text-2xl"
      >
        Журнал событий
      </p>
      <div class="overflow-y-scroll custom-scrollbar"></div>
    </div>
  </div>
</template>
<script>
import BaseIcon from "./BaseIcon.vue";
import SidebarMain from "./SidebarMain.vue";
export default {
  components: {
    BaseIcon,
    SidebarMain,
  },
  data() {
    return {
      activeButton: null,
    };
  },
  methods: {
    handleButtonClick(cameraNumber) {
      if (this.activeButton === cameraNumber) {
        this.activeButton = null;
      } else {
        this.activeButton = cameraNumber;
      }
    },
  },
  computed: {
    isDarkMode() {
      return this.$store.state.darkMode;
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
<style>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #535353 #272727;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #27272700;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #535353;
  border-radius: 12px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #323232;
}
</style>
