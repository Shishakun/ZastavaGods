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
          <div class="overflow-y-scroll custom-scrollbar p-4">
            <ul>
              <li v-for="(event, index) in eventLog" :key="index">
                {{ event }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TextOutput from "./TextOutput.vue";
import SidebarMain from "./SidebarMain.vue";
import YamnetOutput from "./YamnetOutput.vue";
export default {
  components: {
    TextOutput,
    SidebarMain,
    YamnetOutput,
  },
  data() {
    return {
      eventLog: [], // Журнал событий
    };
  },
  computed: {
    isDarkMode() {
      return this.$store.state.darkMode;
    },
  },
  methods: {
    updateEventLog(newLog) {
      this.eventLog = newLog;
    },
  },
};
</script>
