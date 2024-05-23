<template>
  <div>
    <button @click="toggleYamnet" class="text-activeText text-center w-full">
      {{ startYamnet ? "Отключить распознавание" : "Включить распознавание" }}
    </button>
    <div
      class="font-roboto items-center text-center text-xl font-bold mt-2 border-activeText text-activeText border-[1px] p-2 h-12 rounded-xl"
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
      socket: null,
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
      eventLog: [], // Журнал событий
    };
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

      if (this.isRedBackground()) {
        this.logEvent(this.yamnetResult);
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
    logEvent(formattedResult) {
      const timestamp = new Date().toLocaleString();
      this.eventLog.push(`${timestamp} - ${formattedResult}`);
      this.$emit("update-event-log", this.eventLog);
    },
  },
};
</script>
