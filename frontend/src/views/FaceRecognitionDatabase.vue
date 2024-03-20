<template>
  <div class="bg-background w-full custom-scrollbar duration-500 min-h-screen">
    <div class="flex justify-center">
      <FaceRecognitionDatabaseWindow />
    </div>
  </div>
</template>

<script>
import Header2 from "@/components/Header2.vue";
import Footer from "@/components/Footer.vue";
import FaceRecognitionDatabaseWindow from "@/components/FaceRecognitionDatabaseWindow.vue";

export default {
  components: {
    Header2,
    Footer,
    FaceRecognitionDatabaseWindow,
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
