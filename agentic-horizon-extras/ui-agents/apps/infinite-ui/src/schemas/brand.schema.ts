import { z } from 'zod'

const hexColor = /^#[0-9a-fA-F]{6}$/
const cssColor = /^(#[0-9a-fA-F]{6}|rgba?\(.+\))$/
const cssLength = /^\d+(\.\d+)?(px|rem|em|%)$/

const TypographyScale = z.object({
  size: z.string(),
  weight: z.number(),
  tracking: z.string().optional(),
  'line-height': z.number().optional(),
})

const MediaAsset = z.object({
  path: z.string(),
  description: z.string(),
})

const IdentitySchema = z.object({
  mission: z.string().optional(),
  description: z.string().optional(),
  keywords: z.array(z.string()).optional(),
  voice: z.string().optional(),
  avoid: z.array(z.string()).optional(),
}).optional()

export const BrandSchema = z.object({
  name: z.string().min(1),
  tagline: z.string(),
  tone: z.string(),
  audience: z.string(),
  identity: IdentitySchema,
  palette: z.object({
    primary: z.string().regex(hexColor),
    secondary: z.string().regex(hexColor),
    accent: z.string().regex(hexColor),
    background: z.string().regex(hexColor),
    'bg-secondary': z.string().regex(hexColor),
    surface: z.string().regex(hexColor),
    text: z.string().regex(hexColor),
    muted: z.string().regex(hexColor),
    border: z.string().regex(hexColor),
    overlay: z.string().regex(cssColor),
    error: z.string().regex(hexColor),
    warning: z.string().regex(hexColor),
    success: z.string().regex(hexColor),
  }),
  typography: z.object({
    heading: z.string(),
    body: z.string(),
    mono: z.string(),
    scale: z.record(z.string(), TypographyScale),
  }),
  spacing: z.object({
    unit: z.string().regex(cssLength),
    'radius-sm': z.string().regex(cssLength),
    'radius-md': z.string().regex(cssLength),
    'radius-lg': z.string().regex(cssLength),
    'container-max': z.string().regex(cssLength),
  }),
  breakpoints: z.object({
    sm: z.string().regex(cssLength),
    md: z.string().regex(cssLength),
    lg: z.string().regex(cssLength),
    xl: z.string().regex(cssLength),
  }),
  shadows: z.object({
    sm: z.string(),
    md: z.string(),
    lg: z.string(),
  }),
  motion: z.object({
    'duration-fast': z.string(),
    'duration-normal': z.string(),
    'duration-slow': z.string(),
    easing: z.string(),
  }),
  assets: z.object({
    logo: z.string(),
    favicon: z.string(),
    media: z.array(MediaAsset).optional(),
  }),
})

export type BrandConfig = z.infer<typeof BrandSchema>
