// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss'
  ],
  
  ui: {
    global: true,
    icons: ['heroicons', 'simple-icons']
  },
  
  app: {
    head: {
      title: 'DarkSec-AI',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'A comprehensive web vulnerability analysis suite that leverages the power of Generative AI' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },
  
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
    }
  },
  
  typescript: {
    strict: true
  },
  
  nitro: {
    routeRules: {
      "/django_api/**": {
        proxy: `${process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api'}/**`,
        isr: true,
        swr: true,
        cache: { maxAge: 300, staleMaxAge: 900 },
        cors: true,
        headers: {
          'X-Forwarded-Proto': 'http',
          'Access-Control-Allow-Credentials': 'true',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,HEAD,PUT,PATCH,POST,DELETE',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Auth-Override',
        }
      },
    }
  }
})