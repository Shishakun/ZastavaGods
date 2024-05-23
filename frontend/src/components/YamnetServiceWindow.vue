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
        <div>
          <button
            @click="toggleYamnet"
            class="text-activeText text-center w-full"
          >
            {{
              startYamnet ? "Отключить распознавание" : "Включить распознавание"
            }}
          </button>
          <div
            :class="[
              'font-roboto items-center text-center text-xl font-bold mt-2 border-[1px] p-2 h-12 rounded-xl',
              isDangerousEvent
                ? 'bg-red-600 border-red-600 text-white'
                : 'border-activeText text-activeText',
            ]"
          >
            {{ yamnetResult }}
          </div>
        </div>
      </div>
      <div
        class="flex w-full justify-center px-14 py-4 gap-4 duration-500 min-h-[80vh]"
      >
        <div
          class="w-full border-[1px] border-activeText bg-frameBackground rounded-xl duration-500 h-[70vh]"
        >
          <p
            class="text-activeText duration-500 text-center pt-4 font-bold text-2xl"
          >
            Журнал событий
          </p>
          <div
            class="text-xl text-neutral-50 px-24 h-[59vh] overflow-y-auto custom-scrollbar pt-4"
          >
            <p
              v-for="(log, index) in eventLog"
              :key="index"
              class="text-activeText"
            >
              {{ log }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SidebarMain from "./SidebarMain.vue";

export default {
  components: {
    SidebarMain,
  },
  data() {
    return {
      yamnetResult: null,
      startYamnet: false,
      socket: null,
      classesWithRedBackground: [
        "Дыхание",
        "Шаги",
        "Болтовня",
        "Шум, болтовня, болтовня",
        "Галдёж",
        "Топот",
        "Шелест листьев",
        "Транспортное средство",
        "Лодка, водное транспортное средство",
        "Моторная лодка, катер",
        "Автотранспортное средство (дорога)",
        "Автомобиль",
        "Автосигнализация",
        "Визг шин",
        "Проезжающая машина",
        "Полицейская машина (сирена)",
        "Скорая помощь (сирена)",
        "Пожарная машина (сирена)",
        "Воздушное судно",
        "Двигатель самолета",
        "Реактивный двигатель",
        "Винт, воздушный винт",
        "Вертолет",
        "Самолет",
        "Двигатель",
        "Легкий двигатель (высокая частота)",
        "Средний двигатель (средняя частота)",
        "Тяжелый двигатель (низкая частота)",
        "Стук двигателя",
        "Запуск двигателя",
        "Шум транспорта, шум дороги",
        "Холостой ход",
        "Ускорение, рев двигателя",
        "Сигнал тревоги",
        "Сирена",
        "Гражданская оборонная сирена",
        "Детектор дыма, пожарная сигнализация",
        "Пожарная сигнализация",
        "Туманный сигнал",
        "Инструменты",
        "Молоток",
        "Дрель-молоток",
        "Пила",
        "Напильник",
        "Шлифовка",
        "Электроинструмент",
        "Дрель",
        "Взрыв",
        "Выстрел, стрельба",
        "Пулемет",
        "Залп",
        "Артиллерийский огонь",
        "Взрыв",
        "Грохот",
        "Стекло",
        "Треск",
        "Разбивание",
        "Капание",
        "Шшш, шуршание, шум",
        "Тяжелый удар, тухлый звук",
        "Глухой удар",
        "Громкий удар",
        "Разрушение",
        "Разбивание, краш",
        "Скрежет",
        "Разрыв",
        "Визг",
        "Скрип",
        "Шелест",
        "Стук",
        "Щелчок",
        "Щелчок-щелчок",
        "Грохот",
        "Хруст",
        "Скрежет",
        "Скрежет",

      ],
      eventLog: [],
    };
  },
  computed: {
    isDarkMode() {
      return this.$store.state.darkMode;
    },
    isDangerousEvent() {
      if (!this.yamnetResult) return false;
      return this.classesWithRedBackground.some((dangerClass) =>
        this.yamnetResult.includes(dangerClass)
      );
    },
  },
  methods: {
    toggleYamnet() {
      this.startYamnet = !this.startYamnet;
      if (this.startYamnet) {
        this.startWebSocket();
      } else {
        this.stopWebSocket();
      }
    },
    startWebSocket() {
      this.socket = new WebSocket("ws://localhost:8000/ws/yamnet");
      this.socket.onmessage = this.onMessage;
      this.socket.onopen = () => {
        console.log("WebSocket connection opened");
      };
      this.socket.onclose = () => {
        console.log("WebSocket connection closed");
      };
    },
    stopWebSocket() {
      if (this.socket) {
        this.socket.close();
        this.socket = null;
        setTimeout(() => {
          this.yamnetResult = null;
        }, 10000);
      }
    },
    onMessage(event) {
      const data = event.data;
      this.yamnetResult = this.formatResult(data);
      this.logEvent(data); // Log the event
    },
    formatResult(result) {
      const parts = result.split(";").map((part) => part.trim());
      const formattedParts = parts.map((part) => {
        const [label, value] = part.split(":").map((el) => el.trim());
        return `${label}: ${value}`;
      });
      return `Текущее событие: ${formattedParts.join("; ")}`;
    },
    logEvent(data) {
      const parts = data.split(";").map((part) => part.trim());
      const currentDate = new Date().toLocaleString();

      parts.forEach((part) => {
        const [label] = part.split(":").map((el) => el.trim());
        if (this.classesWithRedBackground.includes(label)) {
          this.eventLog.unshift(`${currentDate} - Опасное событие: ${label}`);
        }
      });
    },
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
