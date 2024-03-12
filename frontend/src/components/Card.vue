<template>
  <router-link :to="`${url}`">
    <div
      class="duration-500 dark:bg-hoverBackground rounded-[10px] bg-gray-900/55 dark:hover:shadow-xl dark:hover:shadow-red-900 hover:shadow-xl hover:shadow-blue-700"
    >
      <div
        class="w-full h-[358px] rounded-[10px] duration-300 cursor-pointer backdrop-brightness-[0.55]"
      >
        <div class="flex flex-col justify-center px-10 pt-[133px]">
          <p
            class="text-contrast w-full duration-500 dark:text-activeText font-bold text-center text-2xl font-monster border-t-2 border-b-2 h-full py-2.5"
          >
            {{ title }}
          </p>
          <p
            class="text-contrast w-full duration-500 dark:text-activeText text-center pt-1 text-lg"
          >
            {{ subtitle }}
          </p>
        </div>
      </div>
    </div>
  </router-link>
</template>
<script>
export default {
  props: {
    title: String,
    subtitle: String,
    url: String,
  },
};
</script>
