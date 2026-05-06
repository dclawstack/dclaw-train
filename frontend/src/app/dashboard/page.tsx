"use client";

import { useState } from "react";
import { api, Training, LearnerProgress } from "@/lib/api";

export default function DashboardPage() {
  const [name, setName] = useState("");
  const [format, setFormat] = useState<"Video" | "Quiz" | "Workshop">("Video");
  const [training, setTraining] = useState<Training | null>(null);
  const [progress, setProgress] = useState<LearnerProgress[] | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleCreate() {
    if (!name.trim()) return;
    setLoading(true);
    try {
      const t = await api<Training>("/trainings", {
        method: "POST",
        body: JSON.stringify({ name, format }),
      });
      setTraining(t);
      const p = await api<LearnerProgress[]>(`/trainings/${t.id}/progress`);
      setProgress(p);
    } catch (e) {
      alert("Failed to create training");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="mb-6 text-3xl font-bold text-brand">DClaw Train</h1>
      <div className="rounded-lg border bg-white p-6 shadow-sm">
        <div className="mb-4">
          <label className="mb-1 block text-sm font-medium">Training name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Training name"
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand focus:outline-none"
          />
        </div>
        <div className="mb-4">
          <label className="mb-1 block text-sm font-medium">Format</label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value as any)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand focus:outline-none"
          >
            <option>Video</option>
            <option>Quiz</option>
            <option>Workshop</option>
          </select>
        </div>
        <button
          onClick={handleCreate}
          disabled={loading || !name.trim()}
          className="rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600 disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create Training"}
        </button>
      </div>

      {training && (
        <div className="mt-6 rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">Training Details</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <p className="text-xs text-gray-500">Enrollment link</p>
              <p className="text-sm font-medium text-brand">{training.enrollment_link}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Completion rate</p>
              <p className="text-sm font-medium">{training.completion_rate}%</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Average score</p>
              <p className="text-sm font-medium">{training.average_score}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Certification expiry</p>
              <p className="text-sm font-medium">{training.certification_expiry}</p>
            </div>
          </div>
        </div>
      )}

      {progress && progress.length > 0 && (
        <div className="mt-6 rounded-lg border bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-semibold">Learner Progress</h2>
          <div className="space-y-3">
            {progress.map((p, i) => (
              <div key={i} className="flex items-center justify-between rounded-md bg-gray-50 px-4 py-3">
                <div>
                  <p className="text-sm font-medium">{p.learner_name}</p>
                  <p className="text-xs text-gray-500">Status: {p.status}</p>
                </div>
                <p className="text-sm font-semibold">{p.score}%</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
