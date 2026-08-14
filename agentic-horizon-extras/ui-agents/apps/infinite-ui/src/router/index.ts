import { createRouter, createWebHistory } from 'vue-router'
import WorkspaceView from '../workspace/WorkspaceView.vue'
import BrandView from '../workspace/BrandView.vue'
import CanvasView from '../canvas/CanvasView.vue'
import GalleryHome from '../gallery/GalleryHome.vue'
import TreeView from '../gallery/TreeView.vue'
import BranchPreview from '../gallery/BranchPreview.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'workspace', component: WorkspaceView },
    { path: '/:brand', name: 'brand', component: BrandView, props: true },
    { path: '/:brand/:product', name: 'canvas', component: CanvasView, props: true },
    { path: '/:brand/:product/gallery', name: 'gallery', component: GalleryHome, props: true },
    { path: '/:brand/:product/gallery/:tree', name: 'tree', component: TreeView, props: true },
    { path: '/:brand/:product/gallery/:tree/:branch', name: 'branch', component: BranchPreview, props: true },
  ],
})
