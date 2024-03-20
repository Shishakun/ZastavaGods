<template>
  <div class="bg-background w-full min-h-screen duration-500">
    <div class="flex justify-center">
      <YamnetServiceWindow />
    </div>
  </div>
</template>

<script>
import Header2 from '@/components/Header2.vue'
import Footer from '@/components/Footer.vue'
import YamnetServiceWindow from '@/components/YamnetServiceWindow.vue'

export default {
  components: {
    Header2,
    Footer,
    YamnetServiceWindow
  }
}
</script>

<style></style>
