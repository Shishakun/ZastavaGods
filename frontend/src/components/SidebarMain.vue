<template>
  <div class="flex flex-col gap-2 min-h-screen relative duration-500">
    <router-link to="/">
      <div class="flex flex-col justify-center">
        <p
          class="text-activeText text-7xl text-center z-20 font-stengazeta -mb-5 duration-500"
        >
          ЗАСТАВА
        </p>
        <p
          class="text-base z-30 font-stengazeta text-center text-activeText duration-500"
        >
          Автоматизировання система охраны
        </p>
      </div>
    </router-link>
    <div class="flex flex-col justify-between h-full w-full pt-1 duration-500">
      <div class="w-full flex flex-col gap-2">
        <AssistantCategoryServiceSection>
          <router-link
            v-for="service in services"
            :key="service.name"
            :to="service.route"
          >
            <AssistantCategoryService
              :category="service.category"
              :name="service.name"
              :classed="service.classed"
              :isActive="service.isActive"
            />
          </router-link>
        </AssistantCategoryServiceSection>
      </div>
      <div class="flex justify-center w-full absolute bottom-8">
        <Switcher />
      </div>
    </div>
  </div>
</template>
<script>
import AssistantCategoryService from "./AssistantCategoryService.vue";
import AssistantCategoryServiceSection from "./AssistantCategoryServiceSection.vue";
import BaseIcon from "./BaseIcon.vue";
import Switcher from "./Switcher.vue";
export default {
  components: {
    AssistantCategoryService,
    AssistantCategoryServiceSection,
    BaseIcon,
    Switcher,
  },

  computed: {
    services() {
      return [
        {
          category: "Обнаружение объектов",
          name: "flag",
          classed: "w-8 h-8 text-blue-400",
          route: "/",
          isActive: this.$route.path === "/",
        },
        {
          category: "Распознавание лиц",
          name: "user",
          classed: "w-8 h-8 text-yellow-400",
          route: "/face_recognition",
          isActive: this.$route.path === "/face_recognition",
        },
        {
          category: "Распознавание звуков",
          name: "microphone",
          classed: "w-8 h-8 text-purple-400",
          route: "/sound_recognition",
          isActive: this.$route.path === "/sound_recognition",
        },
        {
          category: "База данных лиц",
          name: "catalog",
          classed: "w-8 h-8 text-green-400",
          route: "/face_database",
          isActive: this.$route.path === "/face_database",
        },
      ];
    },
    isDarkMode() {
      return this.$store.state.darkMode;
    },
  },
};
</script>
<style>
.rainbows {
  position: relative;
}
@keyframes rainbow {
  0% {
    color: white;
  }
  33% {
    color: blue;
  }
  66% {
    color: red;
  }
  100% {
    color: white;
  }
}
.owl {
  position: absolute;
  width: 40px;
  height: 40px;
  background-image: url("https://freesvg.org/img/1531730612.png");
  background-size: cover;
  animation: fly-around 12s ease-in-out infinite;
}

@keyframes fly-around {
  0% {
    left: 10%;
    top: -3%;
  }
  25% {
    left: 23%;
    top: 2%;
  }
  50% {
    left: 60%;
    top: 1%;
  }
  75% {
    left: 75%;
    top: -3%;
  }
  100% {
    left: 10%;
    top: -3%;
  }
}
</style>
