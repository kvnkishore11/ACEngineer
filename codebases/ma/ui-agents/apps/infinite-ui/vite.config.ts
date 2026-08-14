import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'node:fs'
import path from 'node:path'

function brandSyncPlugin(brandsDir: string): Plugin {
  return {
    name: 'brand-sync',
    configureServer(server) {
      // GET /api/workspace/brands — list brand dirs excluding _template
      server.middlewares.use((req, res, next) => {
        const url = req.url ?? ''

        // GET /api/workspace/brands
        if (url === '/api/workspace/brands' && req.method === 'GET') {
          try {
            const dirs = fs.readdirSync(brandsDir, { withFileTypes: true })
              .filter(d => d.isDirectory() && !d.name.startsWith('_'))
              .map(d => d.name)
            res.setHeader('Content-Type', 'application/json')
            res.end(JSON.stringify(dirs))
          } catch {
            res.statusCode = 500
            res.end('[]')
          }
          return
        }

        // GET /api/workspace/products/:brand
        const productsMatch = url.match(/^\/api\/workspace\/products\/([^/]+)\/?$/)
        if (productsMatch && req.method === 'GET') {
          const brand = productsMatch[1]
          const productsDir = path.join(brandsDir, brand, 'products')
          try {
            const dirs = fs.readdirSync(productsDir, { withFileTypes: true })
              .filter(d => d.isDirectory() && !d.name.startsWith('_'))
              .map(d => d.name)
            res.setHeader('Content-Type', 'application/json')
            res.end(JSON.stringify(dirs))
          } catch {
            res.setHeader('Content-Type', 'application/json')
            res.end('[]')
          }
          return
        }

        // GET/POST /api/trees/:brand/:product
        const treesMatch = url.match(/^\/api\/trees\/([^/]+)\/([^/]+)\/?$/)
        if (treesMatch) {
          const brand = treesMatch[1]
          const product = treesMatch[2]
          const treesPath = path.join(brandsDir, brand, 'products', product, 'trees.yaml')

          if (req.method === 'GET') {
            try {
              const content = fs.readFileSync(treesPath, 'utf-8')
              res.setHeader('Content-Type', 'text/plain')
              res.end(content)
            } catch {
              res.statusCode = 404
              res.end('')
            }
            return
          }

          if (req.method === 'POST') {
            let body = ''
            req.on('data', (c: Buffer) => body += c.toString())
            req.on('end', () => {
              fs.mkdirSync(path.dirname(treesPath), { recursive: true })
              fs.writeFileSync(treesPath, body)
              res.end('ok')
            })
            return
          }
        }

        // GET/POST /api/brand/:brand/:product — product-level brand.yaml
        const brandProductMatch = url.match(/^\/api\/brand\/([^/]+)\/([^/]+)\/?$/)
        if (brandProductMatch) {
          const brand = brandProductMatch[1]
          const product = brandProductMatch[2]
          const brandPath = path.join(brandsDir, brand, 'products', product, 'brand.yaml')

          if (req.method === 'GET') {
            if (fs.existsSync(brandPath)) {
              res.setHeader('Content-Type', 'text/plain')
              res.end(fs.readFileSync(brandPath, 'utf-8'))
            } else {
              res.statusCode = 404
              res.end('')
            }
            return
          }

          if (req.method === 'POST') {
            let body = ''
            req.on('data', (c: Buffer) => body += c.toString())
            req.on('end', () => {
              fs.mkdirSync(path.dirname(brandPath), { recursive: true })
              fs.writeFileSync(brandPath, body)
              res.end('ok')
            })
            return
          }
        }

        // GET /api/brand/:brand — brand-level brand.yaml
        const brandMatch = url.match(/^\/api\/brand\/([^/]+)\/?$/)
        if (brandMatch && req.method === 'GET') {
          const brand = brandMatch[1]
          const brandPath = path.join(brandsDir, brand, 'brand.yaml')
          try {
            const content = fs.readFileSync(brandPath, 'utf-8')
            res.setHeader('Content-Type', 'text/plain')
            res.end(content)
          } catch {
            res.statusCode = 404
            res.end('')
          }
          return
        }

        // GET /api/activity/:brand/:product
        const activityMatch = url.match(/^\/api\/activity\/([^/]+)\/([^/]+)\/?$/)
        if (activityMatch && req.method === 'GET') {
          const brand = activityMatch[1]
          const product = activityMatch[2]
          const activityPath = path.join(brandsDir, brand, 'products', product, 'activity.yaml')
          if (fs.existsSync(activityPath)) {
            res.setHeader('Content-Type', 'text/plain')
            res.end(fs.readFileSync(activityPath, 'utf-8'))
          } else {
            res.statusCode = 404
            res.end('')
          }
          return
        }

        next()
      })
    },
  }
}

export default defineConfig({
  plugins: [
    vue(),
    brandSyncPlugin(path.resolve(__dirname, 'src/brands')),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
