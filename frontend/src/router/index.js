import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/face_recognition",
    name: "AudioRecognitionService",

    component: () => import("../views/AudioRecognitionService.vue"),
  },
  {
    path: "/sound_recognition",
    name: "ScanningDocs",

    component: () => import("../views/DocumentsScan.vue"),
  },
  {
    path: "/face_database",
    name: "SeacrhDocs",

    component: () => import("../views/SearchDocument.vue"),
  },
  {
    path: "/",
    name: "ObjectDetectionService",

    component: () => import("../views/ObjectDetectionService.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
