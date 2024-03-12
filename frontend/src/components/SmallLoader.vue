<template>
  <div
    class="lds-dual-ring inline-block w-20 h-20 after:block after:w-[64px] after:h-[64px] after:m-2 after:border-r-[50%] after:border-[6px] dark:after:border-[#ffffff] after:border-[#000000]"
  ></div>
</template>

<script>
export default {};
</script>

<style>
.lds-dual-ring:after {
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
