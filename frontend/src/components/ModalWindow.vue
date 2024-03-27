<template>
  <div
    class="fixed pt-3 z-20 inset-0 focus:outline-none duration-500 bg-neutral-800"
    @click.self="close"
    tabindex="-1"
    @keydown.esc="close"
  >
    <div
      class="bg-neutral-200 z-50 rounded-lg w-[50vw] h-[60vh] mx-auto xl:my-2 flex flex-col shadow-4xl relative"
    >
      <div class="z-50">
        <ModalWindowButtonClose @click="close" class="absolute right-0" />
      </div>
      <div class="flex justify-center pt-8">
        <p class="text-3xl font-bold">Добавить персонал</p>
      </div>
      <div class="w-full pt-8">
        <div class="flex flex-col gap-2 px-16 justify-center">
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Фамилия:</p>
            <input
              v-model="keyword"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Иванов"
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Имя:</p>
            <input
              v-model="keyword"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Дмитрий"
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Отчество:</p>
            <input
              v-model="keyword"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Артемьевич"
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Отдел:</p>
            <select
              v-model="selectedOtdel"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
            >
              <option>1 отдел</option>
              <option>2 отдел</option>
              <option>3 отдел</option>
            </select>
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">
              Уровень допуска:
            </p>
            <select
              v-model="selectedSecret"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
            >
              <option>1</option>
              <option>2</option>
              <option>3</option>
            </select>
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Фото:</p>
            <input
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              type="file"
            />
          </div>
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
