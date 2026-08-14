// Typed REST wrappers around the FastAPI endpoints in
// apps/backend/src/live_bench_server/rest.py.
//
// Every response is parsed through the corresponding Zod schema before being
// handed to the caller. A validation failure throws — the caller is expected
// to surface that as a user-visible "we don't understand the server" error
// rather than corrupting the store.

import {
  BenchmarksListResponseSchema,
  BenchmarkDetailResponseSchema,
  ResetResponseSchema,
  type BenchmarksListResponse,
  type BenchmarkDetailResponse,
  type ResetResponse,
} from '../schemas'

async function jsonOrThrow(res: Response): Promise<unknown> {
  if (!res.ok) {
    let detail = ''
    try {
      detail = await res.text()
    } catch {
      /* swallow */
    }
    throw new Error(`HTTP ${res.status} ${res.statusText}: ${detail}`)
  }
  return res.json()
}

export async function listBenchmarks(): Promise<BenchmarksListResponse> {
  const res = await fetch('/benchmarks', { headers: { Accept: 'application/json' } })
  const raw = await jsonOrThrow(res)
  return BenchmarksListResponseSchema.parse(raw)
}

export async function getBenchmark(sessionId: string): Promise<BenchmarkDetailResponse> {
  const res = await fetch(`/benchmarks/${encodeURIComponent(sessionId)}`, {
    headers: { Accept: 'application/json' },
  })
  const raw = await jsonOrThrow(res)
  return BenchmarkDetailResponseSchema.parse(raw)
}

export async function resetBenchmark(sessionId: string): Promise<ResetResponse> {
  const res = await fetch(`/benchmarks/${encodeURIComponent(sessionId)}/reset`, {
    method: 'POST',
    headers: { Accept: 'application/json' },
  })
  const raw = await jsonOrThrow(res)
  return ResetResponseSchema.parse(raw)
}
