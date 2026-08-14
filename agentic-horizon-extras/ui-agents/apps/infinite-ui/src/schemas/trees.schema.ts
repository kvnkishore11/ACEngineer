import { z } from 'zod'

const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/

const BranchStatus = z.enum(['draft', 'generating', 'validating', 'validated', 'failed'])

const BranchSchema = z.object({
  slug: z.string().regex(slugPattern, 'Branch slug must be lowercase kebab-case'),
  name: z.string().min(1),
  description: z.string(),
  created: z.string().date(),
  status: BranchStatus,
  screenshot: z.string().nullable(),
  forkedFrom: z.string().regex(slugPattern).nullable().optional(),
})

const TreeSchema = z.object({
  slug: z.string().regex(slugPattern, 'Tree slug must be lowercase kebab-case'),
  name: z.string().min(1),
  description: z.string(),
  icon: z.string(),
  branches: z.array(BranchSchema),
})

export const TreesManifestSchema = z.object({
  version: z.literal(1),
  brand: z.string(),
  product: z.string(),
  trees: z.array(TreeSchema),
})

export type TreesManifest = z.infer<typeof TreesManifestSchema>
export type Tree = z.infer<typeof TreeSchema>
export type Branch = z.infer<typeof BranchSchema>
export type BranchStatusType = z.infer<typeof BranchStatus>
