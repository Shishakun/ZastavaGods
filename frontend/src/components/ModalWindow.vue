<template>
  <div
    class="fixed xl:pt-3 inset-0 z-10 bg-black bg-opacity-75 focus:outline-none duration-500"
    @click.self="close"
    tabindex="-1"
    @keydown.esc="close"
  >
    <div class="bg-gray-200 max-w-xl mx-auto xl:my-2">
      <div class="absolute 2xl:right-[41.5rem] p-2">
        <ModalWindowButtonClose @click="close" />
      </div>
      <div class="bg-[#d3d3d3]">
        <div class="h-28">
          <input type="file" multiple />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import ModalWindowButtonClose from "./ModalWindowButtonClose.vue";

export default {
  components: {
    ModalWindowButtonClose,
  },
  methods: {
    close() {
      this.$emit("close");
    },
  },
  mounted() {
    this.$el.focus();
  },
  emits: ["close"],
  props: {
    uav_img: String,
    uav_name: String,
    uav_country: String,
    uav_company: String,
    uav_endurance: Number,
    uav_range: Number,
    uav_payload: Number,
    uav_max_speed: Number,
    uav_platform: String,
    uav_altitude: String,
    uav_mass: Number,
    uav_width: Number,
    uav_length: Number,
  },
};
</script>
