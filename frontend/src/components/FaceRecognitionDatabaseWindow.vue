<template>
  <div class="flex w-full justify-center p-6 gap-4 duration-500">
    <div class="fixed w-64 left-6">
      <SidebarMain />
    </div>
    <div
      class="flex flex-col duration-500 justify-center ml-72 items-center w-full bg-frameBackground rounded-xl outline-dashed outline-[1px] outline-outlineColor"
    >
      <div class="flex mb-4 pt-10">
        <p
          class="text-center text-4xl font-black font-mono text-activeText duration-500"
        >
          Список персонала
        </p>
      </div>
      <div class="w-5/6">
        <div class="flex">
          <div
            class="relative mb-4 flex w-full duration-500 flex-wrap items-stretch gap-2 justify-center text-activeText"
          >
            <input
              type="search"
              class="relative shadow-md m-0 block min-w-0 flex-auto rounded border border-solid border-inputBorder bg-transparent bg-clip-padding px-3 py-[0.25rem] text-base font-normal leading-[1.6] text-activeText outline-none transition duration-500 ease-in-out focus:z-[3] focus:border-primary focus:text-activeText focus:shadow-[inset_0_0_0_1px_rgb(59,113,202)] focus:outline-none placeholder:text-activeText focus:border-primary"
              placeholder="Поиск"
              aria-label="Search"
              aria-describedby="button-addon2"
            />
          </div>
        </div>
      </div>
      <div class="w-5/6 flex justify-start items-center gap-4">
        <p class="text-xl text-activeText duration-500">Сортировка по:</p>
        <div class="flex justify-center gap-2">
          <div v-for="(item, index) in filters" :key="index">
            <button
              :class="{
                'bg-buttonHover text-activeText duration-500':
                  selectedFilter === item.id,
              }"
              class="text-activeText shadow-md font-roboto font-medium border-2 px-4 py-2 rounded-xl duration-500 hover:bg-buttonHover"
              @click="
                selectedFilter = selectedFilter === item.id ? null : item.id
              "
            >
              {{ item.name }}
            </button>
          </div>
        </div>
      </div>
      <div
        class="flex justify-between items-center text-neutral-400 pt-12 w-5/6"
      >
        <div>Всего л/c: 5432</div>
        <div
          class="text-activeText hover:bg-buttonHover shadow-md items-center flex gap-2 dark:bg-green-700 border-[1px] border-outputBorder font-roboto cursor-pointer font-medium px-4 py-2 rounded-md duration-500 dark:hover:bg-green-800"
        >
          Загрузить персонал
        </div>
      </div>
      <div class="w-5/6 mb-10">
        <div class="flex justify-center pt-3" v-for="i in 10" :key="i">
          <transition
            enter-active-class="transition ease-in-out duration-500 transform"
            enter-from-class="-translate-y-[50px]"
            enter-to-class="translate-y-0"
            leave-active-class="transition ease-in-out duration-500 transform"
            leave-from-class="translate-y-0"
            leave-to-class="translate-y-[50px]"
          >
            <div
              class="border-2 shadow-md border-neutral-200 w-full rounded-xl p-2.5"
            >
              <div class="flex justify-between">
                <div class="flex">
                  <img src="../img/translator.jpg" class="h-40 rounded-xl" />
                  <div class="flex flex-col justify-between px-4">
                    <div>
                      <p
                        class="text-activeText text-lg hover:underline duration-500 cursor-pointer flex"
                      >
                        ФИО:
                      </p>
                      <p
                        class="text-activeText text-lg hover:underline duration-500 cursor-pointer flex"
                      >
                        Отдел:
                      </p>
                    </div>
                    <p
                      class="text-activeText text-lg hover:underline duration-500 cursor-pointer flex"
                    >
                      Уровень допуска:
                    </p>
                  </div>
                </div>
                <BaseIcon
                  @click="deleteDocs(i)"
                  name="x"
                  class="w-5 h-5 text-activeText cursor-pointer hover:text-red-600 duration-500"
                />
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TextOutput from "./TextOutput.vue";
import SmallLoader from "./SmallLoader.vue";
import BaseIcon from "./BaseIcon.vue";
import SidebarMain from "./SidebarMain.vue";
import axios from "axios";
export default {
  components: {
    TextOutput,
    SmallLoader,
    BaseIcon,
    SidebarMain,
  },
  computed: {
    file_list() {
      return this.files;
    },
  },
  data() {
    return {
      filters: [
        {
          id: 1,
          name: "По дате загрузки",
        },
        {
          id: 2,
          name: "По названию А → Я",
        },
        {
          id: 3,
          name: "По названию Я → A",
        },
      ],
      filterIsOpen: false,
      selectedFilter: null,
      files: [],
      isLoading: false,
      isReady: false,
    };
  },
  methods: {
    submitFiles() {
      let formData = new FormData();
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append("files[" + i + "]", file);
      }
      axios
        .post("/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(function () {
          console.log("SUCCESS!!");
        })
        .catch(function () {
          console.log("FAILURE!!");
        });
    },
    handleFilesUpload() {
      let uploadedFiles = this.$refs.uploadFile.files;
      console.log(uploadedFiles);
      for (var i = 0; i < uploadedFiles.length; i++) {
        this.files.push(uploadedFiles[i]);
      }
    },
    deleteDocs(id) {
      axios.delete();
    },
  },
};
</script>
