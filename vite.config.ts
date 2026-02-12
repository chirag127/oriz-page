import { defineConfig } from "vite";

export default defineConfig({
    base: "/",
    build: {
        outDir: "dist",
        emptyOutDir: true,
        minify: "esbuild",
        sourcemap: false,
        rollupOptions: {
            output: {
                assetFileNames: "assets/[name]-[hash][extname]",
                chunkFileNames: "assets/[name]-[hash].js",
                entryFileNames: "assets/[name]-[hash].js",
            },
        },
    },
    server: {
        port: 3000,
        open: true,
    },
});
