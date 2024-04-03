<template>
  <div class="flex w-full justify-center p-6 gap-4 duration-500">
    <ModalWindow v-if="isModalOpen" @close="isModalOpen = false" />
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
      <div class="w-11/12">
        <div class="flex">
          <div class="flex flex-wrap items-stretch w-full mb-4">
            <input
              type="search"
              class="form-control relative flex-auto block px-3 py-1.5 text-base font-normal dark:text-neutral-100 text-neutral-700 bg-transparent border-[1px] shadow-md border-neutral-200 rounded transition ease-in-out m-0 focus:outline-none"
              placeholder="Поиск"
              v-model="searchQuery"
            />
          </div>
        </div>
      </div>
      <div class="w-11/12 flex justify-start items-center gap-4">
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
        class="flex justify-between items-center text-neutral-400 pt-12 w-11/12"
      >
        <div>Всего л/c: {{ filteredPeople.length }}</div>
        <div
          @click="isModalOpen = true"
          class="text-neutral-100 dark:hover:bg-green-800 shadow-md items-center flex gap-2 dark:bg-green-700 bg-green-500 border-[1px] border-outputBorder font-roboto cursor-pointer font-medium px-4 py-2 rounded-md duration-300 hover:bg-green-400"
        >
          Загрузить персонал
        </div>
      </div>
      <div class="w-11/12 mb-10 grid grid-cols-2 gap-4">
        <div
          class="flex justify-center pt-8"
          v-for="person in filteredPeople"
          :key="person.id"
        >
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
                  <img
                    :src="getImage(person.image_path)"
                    class="h-40 w-32 rounded-xl"
                  />
                  <div class="flex flex-col justify-between px-4">
                    <div>
                      <p
                        class="text-activeText text-lg hover:underline duration-500 cursor-pointer flex"
                      >
                        ФИО: {{ person.surname }} {{ person.name }}
                        {{ person.patronymic }}
                      </p>
                      <p
                        class="text-activeText text-lg hover:underline duration-500 cursor-pointer flex"
                      >
                        Отдел: {{ person.otdel }}
                      </p>
                    </div>
                    <p
                      class="text-activeText text-lg hover:underline duration-500 cursor-pointer flex"
                    >
                      Уровень допуска: {{ person.secret }}
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
import ModalWindow from "./ModalWindow.vue";
import axios from "axios";
export default {
  components: {
    TextOutput,
    SmallLoader,
    BaseIcon,
    ModalWindow,
    SidebarMain,
  },
  emits: ["close"],
  data() {
    return {
      filters: [
        {
          id: 1,
          name: "По фамилии А → Я",
          sortingFunction: (a, b) => a.surname.localeCompare(b.surname),
        },
        {
          id: 2,
          name: "По фамилии Я → A",
          sortingFunction: (a, b) => b.surname.localeCompare(a.surname),
        },
      ],
      filterIsOpen: false,
      selectedFilter: null,
      people: [],
      isLoading: false,
      isReady: false,
      isModalOpen: false,
      searchQuery: "",
    };
  },
  methods: {
    async fetchPeople() {
      try {
        const response = await fetch("http://localhost:8000/getperson");
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        this.people = data.people;
        this.totalCount = data.total_count;
        console.log(this.people);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    getImage(image_path) {
      return `http://localhost:8000/inputs/people/${image_path}`;
    },
  },
  mounted() {
    this.fetchPeople();
  },
  computed: {
    filteredPeople() {
      let filtered = this.people;
      if (this.searchQuery.trim()) {
        filtered = filtered.filter((person) =>
          person.surname
            .toLowerCase()
            .includes(this.searchQuery.trim().toLowerCase())
        );
      }
      if (this.selectedFilter !== null) {
        const filter = this.filters.find(
          (item) => item.id === this.selectedFilter
        );
        filtered = filtered.slice().sort(filter.sortingFunction);
      }
      return filtered;
    },
  },
};
</script>
