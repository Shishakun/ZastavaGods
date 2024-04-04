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
        <form
          class="flex flex-col gap-2 px-16 justify-center"
          @submit.prevent="submitPersonData"
        >
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Фамилия:</p>
            <input
              v-model="this.surname"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Иванов"
              required
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Имя:</p>
            <input
              v-model="this.name"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Дмитрий"
              required
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Отчество:</p>
            <input
              v-model="this.patronymic"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              placeholder="Например: Артемьевич"
              required
            />
          </div>
          <div class="flex items-center justify-between w-full gap-2">
            <p class="text-neutral-700 w-3/12 font-semibold">Отдел:</p>
            <select
              v-model="this.otdel"
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm border-[1px] border-neutral-300 shadow-sm"
              required
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
              v-model="this.secret"
              required
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
              class="rounded-md w-9/12 h-8 pl-2.5 placeholder:text-sm file:rounded-xl file:w-[10vw] file:border-2 file:border-neutral-500 file:shadow-md file:mr-4"
              type="file"
              accept="image/png, image/jpeg"
              ref="fileInput"
              @change="updateFileInput"
              required
            />
          </div>
          <div class="flex items-center justify-end w-full gap-2">
            <button
              @click.prevent="submitPersonData"
              type="submit"
              class="bg-green-600 shadow-md hover:bg-green-700 duration-300 hover:shadow-xl rounded-md px-4 py-2 text-neutral-200"
            >
              Сохранить
            </button>
          </div>
          <div v-if="successMessage" class="text-green-600">
            {{ successMessage }}
          </div>
          <div v-else-if="errorMessage" class="text-red-600">
            {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import ModalWindowButtonClose from "./ModalWindowButtonClose.vue";
import axios from "axios";
export default {
  components: {
    ModalWindowButtonClose,
  },
  methods: {
    close() {
      this.$emit("close");
    },
    updateFileInput() {
      this.file = this.$refs.fileInput.files[0];
    },
    async submitPersonData() {
      if (!this.validateForm()) {
        return;
      }
      const formData = new FormData();
      formData.append("surname", this.surname);
      formData.append("name", this.name);
      formData.append("patronymic", this.patronymic);
      formData.append("otdel", this.otdel);
      formData.append("secret", this.secret);
      formData.append("file", this.file);

      try {
        const response = await axios.post(
          "http://localhost:8000/uploadPeople",
          formData
        );
        this.successMessage = "Данные успешно отправлены!";
        this.surname = "";
        this.name = "";
        this.patronymic = "";
        this.secret = "";
        this.otdel = "";
        this.file = "";
        setTimeout(() => {
          this.$emit("close");
          this.$emit("update-people-list");
        }, 2000);
        console.log(response.data);
      } catch (error) {
        this.errorMessage = "Ошибка при отправке данных";
        console.error(error);
      }
    },
    validateForm() {
      if (
        !this.surname ||
        !this.name ||
        !this.patronymic ||
        !this.otdel ||
        !this.secret ||
        !this.file
      ) {
        this.errorMessage = "Все поля должны быть заполнены!";
        return false;
      }
      return true;
    },
  },
  mounted() {
    this.$el.focus();
  },

  emits: ["close"],
  data() {
    return {
      surname: "",
      name: "",
      patronymic: "",
      otdel: "",
      secret: "",
      file: "",
      successMessage: "",
      errorMessage: "",
    };
  },
};
</script>
