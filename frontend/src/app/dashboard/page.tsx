"use client";

import { useState, useEffect, useCallback } from "react";
import {
  coursesApi, analyticsApi, liveSessionApi, learningPathApi, badgeApi,
  Course, AnalyticsOverview, LiveSession, LearningPath, Badge,
} from "@/lib/api";
import TutorBot from "@/components/tutor-bot";

type Tab = "courses" | "analytics" | "paths" | "sessions" | "badges";

export default function DashboardPage() {
  const [tab, setTab] = useState<Tab>("courses");
  const [courses, setCourses] = useState<Course[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsOverview | null>(null);
  const [sessions, setSessions] = useState<LiveSession[]>([]);
  const [path, setPath] = useState<LearningPath | null>(null);
  const [badges, setBadges] = useState<Badge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [title, setTitle] = useState("");
  const [format, setFormat] = useState("Video");
  const [description, setDescription] = useState("");
  const [creating, setCreating] = useState(false);
  const LEARNER_ID = "demo-learner";

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      switch (tab) {
        case "courses": {
          const res = await coursesApi.list({ page_size: 50 });
          setCourses(res.items);
          break;
        }
        case "analytics": {
          const a = await analyticsApi.overview();
          setAnalytics(a);
          break;
        }
        case "paths": {
          const p = await learningPathApi.get(LEARNER_ID).catch(() => null);
          if (!p) {
            const g = await learningPathApi.generate(LEARNER_ID, "Software Engineer", ["Master AI/ML"]);
            setPath(g);
          } else {
            setPath(p);
          }
          break;
        }
        case "sessions": {
          const s = await liveSessionApi.upcoming(10);
          setSessions(s);
          break;
        }
        case "badges": {
          const b = await badgeApi.list(LEARNER_ID);
          setBadges(b);
          break;
        }
      }
    } catch (e: any) {
      setError(e.message || "Failed to load data");
    } finally {
      setLoading(false);
    }
  }, [tab]);

  useEffect(() => { loadData(); }, [loadData]);

  async function handleCreate() {
    if (!title.trim()) return;
    setCreating(true);
    try {
      await coursesApi.create({ title, format, description, is_published: true });
      setTitle("");
      setDescription("");
      await loadData();
    } catch (e: any) {
      alert("Failed: " + e.message);
    } finally {
      setCreating(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete this course?")) return;
    try {
      await coursesApi.delete(id);
      setCourses(courses.filter((c) => c.id !== id));
    } catch (e: any) {
      alert("Failed: " + e.message);
    }
  }

  async function handleAwardBadge() {
    try {
      await badgeApi.award(LEARNER_ID, "streak", "7-Day Streak", "7 consecutive days");
      await loadData();
    } catch (e: any) {
      alert("Failed: " + e.message);
    }
  }

  const tabs: { key: Tab; label: string }[] = [
    { key: "courses", label: "📚 Courses" },
    { key: "analytics", label: "📊 Analytics" },
    { key: "paths", label: "🧭 Learning Paths" },
    { key: "sessions", label: "🔴 Live Sessions" },
    { key: "badges", label: "🏅 Badges" },
  ];

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-brand-600">DClaw Train Dashboard</h1>
        <p className="mt-1 text-gray-500">AI-powered LMS · Manage courses, track learners, and analyze progress.</p>
      </div>

      <div className="mb-6 flex flex-wrap gap-2 border-b pb-2">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`rounded-t-md px-4 py-2 text-sm font-medium transition-colors ${
              tab === t.key ? "border-b-2 border-brand-600 bg-orange-50 text-brand-600" : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error} <button onClick={loadData} className="ml-3 underline">Retry</button>
        </div>
      )}

      {loading && <div className="py-12 text-center text-gray-400">Loading...</div>}

      {/* Courses tab */}
      {!loading && tab === "courses" && (
        <div>
          <div className="mb-6 rounded-lg border bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-lg font-semibold">Create New Course</h2>
            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="mb-1 block text-xs font-medium text-gray-600">Title</label>
                <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Course title" className="w-full rounded-md border px-3 py-2 text-sm focus:border-brand-600 focus:outline-none" />
              </div>
              <div>
                <label className="mb-1 block text-xs font-medium text-gray-600">Format</label>
                <select value={format} onChange={(e) => setFormat(e.target.value)} className="w-full rounded-md border px-3 py-2 text-sm focus:border-brand-600 focus:outline-none">
                  <option>Video</option><option>Quiz</option><option>Workshop</option><option>Document</option><option>Assignment</option>
                </select>
              </div>
              <div>
                <label className="mb-1 block text-xs font-medium text-gray-600">Description</label>
                <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Brief description" className="w-full rounded-md border px-3 py-2 text-sm focus:border-brand-600 focus:outline-none" />
              </div>
            </div>
            <button onClick={handleCreate} disabled={creating || !title.trim()} className="mt-4 rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50">
              {creating ? "Creating..." : "Create Course"}
            </button>
          </div>

          {courses.length === 0 ? (
            <div className="py-12 text-center text-gray-400">No courses yet. Create one above.</div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {courses.map((c) => (
                <div key={c.id} className="rounded-lg border bg-white p-5 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between">
                    <h3 className="font-semibold text-gray-900">{c.title}</h3>
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${c.is_published ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"}`}>
                      {c.is_published ? "Published" : "Draft"}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">{c.format} · {c.category || "Uncategorized"}</p>
                  {c.description && <p className="mt-2 text-sm text-gray-600 line-clamp-2">{c.description}</p>}
                  <div className="mt-3 flex items-center gap-3 text-xs text-gray-400">
                    <span>{c.lesson_count || 0} lessons</span>
                    <span>{c.enrollment_count || 0} enrolled</span>
                  </div>
                  <button onClick={() => handleDelete(c.id)} className="mt-3 text-xs text-red-500 hover:text-red-700">Delete</button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Analytics tab */}
      {!loading && tab === "analytics" && analytics && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StatCard label="Total Courses" value={analytics.total_courses} color="blue" />
          <StatCard label="Total Enrollments" value={analytics.total_enrollments} color="green" />
          <StatCard label="Total Completions" value={analytics.total_completions} color="purple" />
          <StatCard label="Avg Completion Rate" value={`${analytics.average_completion_rate}%`} color="orange" />
          <StatCard label="Average Score" value={`${analytics.average_score}%`} color="teal" />
          <StatCard label="At-Risk Learners" value={analytics.at_risk_learners} color={analytics.at_risk_learners > 0 ? "red" : "green"} />
        </div>
      )}

      {/* Paths tab */}
      {!loading && tab === "paths" && path && (
        <div>
          <div className="mb-6 rounded-lg border bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">Your Personalized Learning Path</h2>
            <p className="mt-1 text-sm text-gray-500">{path.reasoning || "Based on your role and career goals"}</p>
          </div>
          <div className="space-y-3">
            {(path.recommended_courses || []).map((course, i) => (
              <div key={i} className="flex items-center gap-4 rounded-lg border bg-white p-4 shadow-sm">
                <div className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold text-white ${course.priority === 1 ? "bg-red-500" : "bg-blue-500"}`}>{i + 1}</div>
                <div className="flex-1">
                  <h3 className="font-medium">{course.title}</h3>
                  <p className="text-xs text-gray-500">{course.reason}</p>
                </div>
                <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${course.priority === 1 ? "bg-red-100 text-red-700" : "bg-blue-100 text-blue-700"}`}>
                  {course.priority === 1 ? "High Priority" : "Recommended"}
                </span>
              </div>
            ))}
          </div>
          {path.skills_gap && Object.keys(path.skills_gap).length > 0 && (
            <div className="mt-6 rounded-lg border bg-white p-6 shadow-sm">
              <h2 className="mb-3 text-lg font-semibold">Skills Gaps</h2>
              <div className="space-y-2">
                {Object.entries(path.skills_gap).map(([skill, gap]) => (
                  <div key={skill} className="flex items-center gap-3">
                    <span className="w-24 text-sm font-medium capitalize">{skill}</span>
                    <div className="flex-1 rounded-full bg-gray-100">
                      <div className="h-2 rounded-full bg-red-400" style={{ width: `${Math.min(gap as number, 100)}%` }} />
                    </div>
                    <span className="text-xs text-gray-500">Gap: {gap}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Sessions tab */}
      {!loading && tab === "sessions" && (
        <div>
          {sessions.length === 0 ? (
            <div className="py-12 text-center text-gray-400">No upcoming sessions.</div>
          ) : (
            <div className="space-y-3">
              {sessions.map((s) => (
                <div key={s.id} className="flex items-center gap-4 rounded-lg border bg-white p-4 shadow-sm">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-100 text-red-600 text-lg">🔴</div>
                  <div className="flex-1">
                    <h3 className="font-medium">{s.title}</h3>
                    <p className="text-sm text-gray-500">{new Date(s.scheduled_at).toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })} · {s.duration_minutes} min</p>
                  </div>
                  {s.session_url && <a href={s.session_url} target="_blank" rel="noreferrer" className="rounded-md bg-brand-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-brand-700">Join</a>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Badges tab */}
      {!loading && tab === "badges" && (
        <div>
          <button onClick={handleAwardBadge} className="mb-4 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">🏅 Award Streak Badge</button>
          {badges.length === 0 ? (
            <div className="py-12 text-center text-gray-400">No badges yet.</div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {badges.map((b) => (
                <div key={b.id} className="rounded-lg border bg-white p-4 text-center shadow-sm">
                  <div className="mb-2 text-3xl">{b.badge_type === "completion" ? "🎓" : b.badge_type === "excellence" ? "⭐" : b.badge_type === "speed" ? "⚡" : b.badge_type === "streak" ? "🔥" : "🏅"}</div>
                  <h3 className="text-sm font-medium">{b.title}</h3>
                  {b.description && <p className="mt-1 text-xs text-gray-500">{b.description}</p>}
                  <p className="mt-2 text-xs text-gray-400">{new Date(b.earned_at).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <TutorBot learnerId="demo-learner" />
    </main>
  );
}

function StatCard({ label, value, color }: { label: string; value: string | number; color: string }) {
  const cm: Record<string, string> = { blue: "border-l-blue-500 bg-blue-50", green: "border-l-green-500 bg-green-50", purple: "border-l-purple-500 bg-purple-50", orange: "border-l-orange-500 bg-orange-50", teal: "border-l-teal-500 bg-teal-50", red: "border-l-red-500 bg-red-50" };
  return (
    <div className={`rounded-lg border-l-4 p-4 ${cm[color] || cm.blue}`}>
      <p className="text-xs font-medium text-gray-500 uppercase">{label}</p>
      <p className="mt-1 text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );
}
