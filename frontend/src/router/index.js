import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/face_recognition",
    name: "AudioRecognitionService",

    component: () => import("../views/FaceRecognitionService.vue"),
  },
  {
    path: "/sound_recognition",
    name: "Yamnet",

    component: () => import("../views/YamnetService.vue"),
  },
  {
    path: "/face_database",
    name: "FaceRecognition",

    component: () => import("../views/FaceRecognitionDatabase.vue"),
  },
  {
    path: "/",
    name: "ObjectDetection",

    component: () => import("../views/ObjectDetectionService.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
