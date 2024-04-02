<template>
  <div class="fixed right-0 bottom-1 py-2 z-50">
    <div
      class="bg-red-200 border-l-4 border-red-500 text-red-700 p-4 w-96"
      role="alert"
    >
      <div class="relative">
        <BaseIcon
          name="x"
          class="w-6 h-6 absolute -right-2 -top-2"
          @click="$emit('close')"
        />
      </div>
      <p class="font-bold text-xl">Ошибка</p>
      <p class="text-lg pt-1 leading-tight">Не найдено лицо или человек отстутсвует в базе персонала</p>
    </div>
  </div>
</template>
<script>
import BaseIcon from "./BaseIcon.vue";

export default {
  components: { BaseIcon },
};
</script>
