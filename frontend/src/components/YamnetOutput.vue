<template>
  <div>
    <button @click="toggleYamnet" class="text-activeText text-center w-full">
      {{ startYamnet ? "Отключить распознавание" : "Включить распознавание" }}
    </button>
    <div
      class="font-roboto items-center text-center text-xl font-bold mt-2 border-activeText text-activeText border-[1px] p-2 h-12 p rounded-xl"
    >
      {{ yamnetResult }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      yamnetResult: null,
      startYamnet: false,
      classesWithRedBackground: [
        "Gunshot",
        "gunfire",
        "Machine gun",
        "Explosion",
        "Artillery fire",
        "Cap gun",
        "Boom",
        "Fireworks",
        "Firecracker",
        "Police car (siren)",
        "Ambulance (siren)",
        "fire truck (siren)",
        "Engine",
        "Siren",
        "Alarm",
        "Jet engine",
        "Foghorn",
        "Aircraft",
        "Helicopter",
      ],
    };
  },
  methods: {
    async fetchYamnetResult() {
      if (this.startYamnet) {
        try {
          const response = await fetch("http://localhost:8000/yamnet");
          const data = await response.json();

          if (data.result && data.result.length > 0) {
            const result = data.result[0];
            const formattedResult = this.formatResult(result);
            this.yamnetResult = formattedResult;
          } else {
            this.yamnetResult = "No result available";
          }

          console.log(data);
          console.log(this.yamnetResult);
        } catch (error) {
          console.error(error);
        }
      }
    },
    toggleYamnet() {
      this.startYamnet = !this.startYamnet;
      if (!this.startYamnet) {
        setInterval(() => {
          this.yamnetResult = null;
        }, 10000);
        // очищаем результат, чтобы не отображать устаревшие данные
        clearInterval(this.interval); // останавливаем интервал обновления данных
      } else {
        this.fetchYamnetResult(); // если startYamnet стало true, сразу запрашиваем данные
        this.interval = setInterval(this.fetchYamnetResult, 2000); // запускаем интервал обновления данных
      }
    },
    isRedBackground() {
      if (this.yamnetResult) {
        for (const className of this.classesWithRedBackground) {
          if (this.yamnetResult.includes(className)) {
            return true;
          }
        }
      }
      return false;
    },
    formatResult(result) {
      const parts = result.split(";").map((part) => part.trim());
      const formattedParts = parts.map((part) => {
        const [label, value] = part.split(":").map((el) => el.trim());
        return `${label}: ${value}`;
      });
      return `Текущее событие: ${formattedParts.join("; ")}`;
    },
  },
};
</script>
