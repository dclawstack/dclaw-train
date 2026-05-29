"use client";

/**
 * Demo seed/clear controls for the landing page (REMOVABLE feature).
 *
 * To remove the demo feature entirely:
 *   1. Delete this file.
 *   2. Remove the <DemoControls /> block in app/page.tsx (between the markers).
 *   3. Delete the backend demo router + service + include line (see demo.py header).
 */
import { useEffect, useState } from "react";

const BASE = process.env.NEXT_PUBLIC_API_URL || "";

type DemoStatus = {
  enabled: boolean;
  seeded: boolean;
  counts: Record<string, number>;
  credentials: null;
};

type Phase = "loading" | "ready" | "unavailable";

async function call<T>(path: string, method: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { method });
  if (!res.ok) throw new Error(await res.text());
  return (await res.json()) as T;
}

export default function DemoControls() {
  const [status, setStatus] = useState<DemoStatus | null>(null);
  const [phase, setPhase] = useState<Phase>("loading");
  const [busy, setBusy] = useState<"seed" | "reset" | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      const s = await call<DemoStatus>("/api/v1/demo/status", "GET");
      setStatus(s);
      setPhase(s.enabled ? "ready" : "unavailable");
    } catch {
      setStatus(null);
      setPhase("unavailable");
    }
  }

  useEffect(() => {
    void refresh();
  }, []);

  async function onSeed() {
    setBusy("seed");
    setError(null);
    try {
      setStatus(await call<DemoStatus>("/api/v1/demo/seed", "POST"));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Seed failed");
    } finally {
      setBusy(null);
    }
  }

  async function onReset() {
    if (!confirm("Delete all DEMO courses, lessons, enrollments, and forum data?")) return;
    setBusy("reset");
    setError(null);
    try {
      setStatus(await call<DemoStatus>("/api/v1/demo/reset", "DELETE"));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Reset failed");
    } finally {
      setBusy(null);
    }
  }

  return (
    <section data-demo-controls className="border-y border-brand-200 bg-brand-50/50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div className="flex-1">
            <div className="mb-2 inline-flex items-center gap-2 rounded-full bg-brand-100 px-3 py-1 text-[10px] font-bold uppercase tracking-wide text-brand-800">
              Demo
            </div>
            <h2 className="text-2xl font-bold text-gray-900">
              Try DClaw Train with sample data
            </h2>
            <p className="mt-2 max-w-2xl text-sm text-gray-600">
              Seed loads published courses with lessons, a quiz, learners in mixed
              enrollment states with progress, an upcoming live session, and a
              discussion thread. Everything is prefixed{" "}
              <code className="rounded bg-white px-1.5 py-0.5 font-mono text-xs text-brand-700">DEMO</code>{" "}
              so Clear removes only what was seeded.
            </p>

            {phase === "ready" && status?.seeded && (
              <p className="mt-3 text-sm text-gray-700">
                <strong>Seeded:</strong>{" "}
                {Object.entries(status.counts).map(([k, v]) => `${v} ${k}`).join(" · ")}
              </p>
            )}

            {phase === "unavailable" && (
              <div className="mt-4 rounded-xl border border-gray-200 bg-white p-4 text-sm text-gray-600">
                The demo backend isn&rsquo;t connected to this deploy (or demo mode is
                off). Run the full stack with{" "}
                <code className="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-xs">ENABLE_DEMO_MODE=true</code>{" "}
                to activate seeding. Production deploys leave it off — the endpoints return 403.
              </div>
            )}

            {error && (
              <div className="mt-3 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
                {error}
              </div>
            )}
          </div>

          <div className="flex flex-col gap-2 sm:flex-row md:flex-col">
            {phase === "loading" && (
              <div className="text-xs text-gray-400">Checking demo backend…</div>
            )}

            {phase === "ready" && !status?.seeded && (
              <button
                type="button"
                onClick={onSeed}
                disabled={busy !== null}
                className="inline-flex items-center justify-center rounded-lg bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow hover:bg-brand-700 disabled:opacity-50"
              >
                {busy === "seed" ? "Seeding…" : "Seed demo data"}
              </button>
            )}

            {phase === "ready" && status?.seeded && (
              <>
                <a
                  href="/dashboard"
                  className="inline-flex items-center justify-center rounded-lg bg-brand-600 px-5 py-3 text-sm font-semibold text-white shadow hover:bg-brand-700"
                >
                  Open the dashboard →
                </a>
                <button
                  type="button"
                  onClick={onSeed}
                  disabled={busy !== null}
                  className="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-5 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                >
                  {busy === "seed" ? "Re-seeding…" : "Re-seed"}
                </button>
                <button
                  type="button"
                  onClick={onReset}
                  disabled={busy !== null}
                  className="inline-flex items-center justify-center rounded-lg border border-red-200 bg-white px-5 py-3 text-sm font-semibold text-red-700 hover:bg-red-50 disabled:opacity-50"
                >
                  {busy === "reset" ? "Clearing…" : "Clear demo data"}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
