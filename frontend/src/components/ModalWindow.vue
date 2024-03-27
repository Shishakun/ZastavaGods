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
      <div class="w-full pt-12">
        <form action="" class="flex flex-col gap-2 px-16 justify-center">
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Фамилия:</p>
            <input
              v-model="surname"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Иванов"
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Имя:</p>
            <input
              v-model="name"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Дмитрий"
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Отчество:</p>
            <input
              v-model="patronymic"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Артемьевич"
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Отдел:</p>
            <select
              v-model="otdel"
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
              v-model="secret"
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
              class="rounded-md w-9/12 h-8 placeholder:text-sm file:rounded-xl file:w-[10vw] file:border-2 file:border-neutral-500 file:shadow-md file:mr-4"
              type="file"
              accept="image/png, image/jpeg"
            />
          </div>
          <div class="flex items-center justify-end w-full gap-2">
            <button
              class="bg-green-600 shadow-md hover:bg-green-700 duration-300 hover:shadow-xl rounded-md px-4 py-2 text-neutral-200"
            >
              Сохранить
            </button>
          </div>
        </form>
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
  // data() {
  //   return {
  //     secret: "1",
  //     surname: surname,
  //     name: name,
  //     patronymic: patronymic,
  //     otdel: otdel,
  //     secret: secret,
  //   };
  // },
};
</script>
