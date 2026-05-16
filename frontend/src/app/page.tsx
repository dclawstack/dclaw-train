"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-white">
      {/* ─── NAVBAR ─── */}
      <nav
        className={`fixed top-0 z-50 w-full transition-all duration-300 ${
          scrolled
            ? "border-b border-gray-200 bg-white/95 backdrop-blur shadow-sm"
            : "bg-transparent"
        }`}
      >
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🚂</span>
            <span className="text-xl font-bold text-gray-900">DClaw Train</span>
          </div>
          <div className="hidden items-center gap-6 md:flex">
            <a href="#features" className="text-sm font-medium text-gray-600 hover:text-brand-600 transition-colors">Features</a>
            <a href="#ai" className="text-sm font-medium text-gray-600 hover:text-brand-600 transition-colors">AI</a>
            <a href="#pricing" className="text-sm font-medium text-gray-600 hover:text-brand-600 transition-colors">Pricing</a>
            <Link
              href="/dashboard"
              className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-brand-700 transition-all"
            >
              Launch Dashboard
            </Link>
          </div>
        </div>
      </nav>

      {/* ─── HERO ─── */}
      <section className="relative overflow-hidden bg-gradient-to-br from-brand-50 via-orange-50 to-amber-50 pt-32 pb-20">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-[0.03]" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, #c2410c 1px, transparent 0)`,
          backgroundSize: "40px 40px",
        }} />
        <div className="relative mx-auto max-w-7xl px-6">
          <div className="grid items-center gap-12 lg:grid-cols-2">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-4 py-1.5 text-xs font-semibold text-brand-700">
                <span className="h-1.5 w-1.5 rounded-full bg-brand-500 animate-pulse" />
                Now with AI Copilot
              </div>
              <h1 className="text-5xl font-extrabold leading-tight tracking-tight text-gray-900 lg:text-6xl">
                Train your team
                <br />
                <span className="bg-gradient-to-r from-brand-600 to-orange-500 bg-clip-text text-transparent">
                  at lightspeed
                </span>
              </h1>
              <p className="max-w-lg text-lg leading-relaxed text-gray-600">
                DClaw Train is the AI-first LMS that lets you build courses, auto-generate quizzes,
                track learner progress, and issue certifications — all from one platform.
              </p>
              <div className="flex flex-wrap gap-3">
                <Link
                  href="/dashboard"
                  className="rounded-xl bg-brand-600 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-brand-200 hover:bg-brand-700 transition-all hover:shadow-xl"
                >
                  Get Started Free →
                </Link>
                <a
                  href="#features"
                  className="rounded-xl border border-gray-300 bg-white px-6 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-all"
                >
                  See Features
                </a>
              </div>
              <div className="flex items-center gap-6 pt-2 text-sm text-gray-500">
                <div className="flex -space-x-2">
                  {["bg-purple-500", "bg-blue-500", "bg-green-500", "bg-brand-500", "bg-pink-500"].map((c, i) => (
                    <div key={i} className={`h-8 w-8 rounded-full border-2 border-white ${c} flex items-center justify-center text-xs font-bold text-white`}>
                      {String.fromCharCode(65 + i)}
                    </div>
                  ))}
                </div>
                <span>Trusted by <strong className="text-gray-900">500+</strong> teams</span>
              </div>
            </div>

            {/* Hero illustration */}
            <div className="hidden lg:block">
              <div className="relative">
                <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-brand-400 to-orange-300 opacity-30 blur-xl" />
                <div className="relative rounded-2xl border border-gray-200 bg-white p-6 shadow-2xl">
                  {/* Fake dashboard preview */}
                  <div className="mb-4 flex items-center gap-2">
                    <div className="h-3 w-3 rounded-full bg-red-400" />
                    <div className="h-3 w-3 rounded-full bg-yellow-400" />
                    <div className="h-3 w-3 rounded-full bg-green-400" />
                  </div>
                  <div className="space-y-3">
                    <div className="flex gap-2">
                      <div className="h-20 flex-1 rounded-lg bg-gradient-to-br from-brand-100 to-orange-100 p-3">
                        <div className="h-2 w-16 rounded bg-brand-300" />
                        <div className="mt-2 text-lg font-bold text-brand-800">1,247</div>
                        <div className="text-xs text-brand-600">Active Learners</div>
                      </div>
                      <div className="h-20 flex-1 rounded-lg bg-gradient-to-br from-blue-50 to-indigo-100 p-3">
                        <div className="h-2 w-16 rounded bg-blue-300" />
                        <div className="mt-2 text-lg font-bold text-blue-800">89%</div>
                        <div className="text-xs text-blue-600">Completion Rate</div>
                      </div>
                      <div className="h-20 flex-1 rounded-lg bg-gradient-to-br from-green-50 to-emerald-100 p-3">
                        <div className="h-2 w-16 rounded bg-green-300" />
                        <div className="mt-2 text-lg font-bold text-green-800">42</div>
                        <div className="text-xs text-green-600">Courses</div>
                      </div>
                    </div>
                    <div className="rounded-lg bg-gray-50 p-3">
                      <div className="mb-2 flex items-center gap-2">
                        <div className="h-6 w-6 rounded-full bg-brand-500 flex items-center justify-center text-xs text-white">🤖</div>
                        <span className="text-xs font-medium text-gray-700">AI Tutor Active</span>
                      </div>
                      <div className="space-y-1">
                        <div className="rounded bg-white px-2 py-1 text-xs text-gray-600">Can you explain this concept?</div>
                        <div className="rounded bg-brand-50 px-2 py-1 text-xs text-brand-800">Let me guide you through it step by step...</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Wave divider */}
        <div className="absolute bottom-0 w-full">
          <svg viewBox="0 0 1440 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 50C240 100 480 0 720 50C960 100 1200 0 1440 50V100H0V50Z" fill="white" />
          </svg>
        </div>
      </section>

      {/* ─── FEATURES (P0 + v1.0) ─── */}
      <section id="features" className="py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-brand-50 px-4 py-1 text-xs font-semibold text-brand-700">
              ⚡ Core Platform
            </div>
            <h2 className="text-4xl font-extrabold text-gray-900">
              Everything you need to train at scale
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-500">
              From course creation to learner analytics — all powered by AI and built on modern infrastructure.
            </p>
          </div>

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                icon: "📚",
                title: "Course & Library CRUD",
                desc: "Create, organize, and manage training courses with rich media support. Full CRUD with real PostgreSQL persistence.",
                gradient: "from-blue-50 to-blue-100",
                iconBg: "bg-blue-100 text-blue-600",
              },
              {
                icon: "🎬",
                title: "Lesson & Video CMS",
                desc: "Structured lessons with video uploads, rich text content, resource attachments, and drag-and-drop reordering.",
                gradient: "from-purple-50 to-purple-100",
                iconBg: "bg-purple-100 text-purple-600",
              },
              {
                icon: "📝",
                title: "Quiz & Assessment Builder",
                desc: "Manual quiz creation with multiple question types (MCQ, T/F, short answer, essay). Auto-scoring and feedback.",
                gradient: "from-amber-50 to-amber-100",
                iconBg: "bg-amber-100 text-amber-600",
              },
              {
                icon: "📊",
                title: "Learner Progress Tracking",
                desc: "Per-learner progress across courses and lessons. Time tracking, completion stats, and score aggregation.",
                gradient: "from-emerald-50 to-emerald-100",
                iconBg: "bg-emerald-100 text-emerald-600",
              },
            ].map((f, i) => (
              <div
                key={i}
                className={`group relative rounded-2xl border border-gray-100 bg-gradient-to-br ${f.gradient} p-6 shadow-sm transition-all hover:shadow-lg hover:-translate-y-1`}
              >
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl ${f.iconBg} text-2xl`}>
                  {f.icon}
                </div>
                <h3 className="mb-2 text-lg font-bold text-gray-900">{f.title}</h3>
                <p className="text-sm leading-relaxed text-gray-600">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── AI FEATURES (P0) ─── */}
      <section id="ai" className="bg-gray-900 py-24 text-white">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-brand-900/50 px-4 py-1 text-xs font-semibold text-brand-300 border border-brand-800">
              🤖 AI-Powered
            </div>
            <h2 className="text-4xl font-extrabold text-white">
              AI that teaches, not just generates
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-400">
              Our AI doesn't just spit out answers — it guides learners with Socratic questioning, personalized paths, and smart content generation.
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-3">
            {[
              {
                icon: "🧑‍🏫",
                title: "AI Learning Copilot",
                tag: "P0",
                points: [
                  "24/7 tutor with RAG over course content",
                  "Socratic questioning — hints, not answers",
                  "Context-aware per lesson/course",
                  "Conversation memory per learner",
                  "Floating chat widget with suggestions",
                ],
                gradient: "from-brand-500 to-orange-500",
                delay: "0",
              },
              {
                icon: "⚡",
                title: "AI Quiz Generator",
                tag: "P0",
                points: [
                  "Auto-generate from lesson transcript/text",
                  "Multiple choice, T/F, short answer types",
                  "Difficulty levels: easy/medium/hard",
                  "Smart distractor generation",
                  "One-click add to any lesson",
                ],
                gradient: "from-purple-500 to-pink-500",
                delay: "100",
              },
              {
                icon: "🎯",
                title: "AI Learning Paths",
                tag: "P1",
                points: [
                  "Role & skills-gap based recommendations",
                  "Career goal alignment",
                  "Priority-ranked course suggestions",
                  "Skills gap visualization",
                  "Auto-regenerates as you progress",
                ],
                gradient: "from-emerald-500 to-teal-500",
                delay: "200",
              },
            ].map((f, i) => (
              <div
                key={i}
                className="relative rounded-2xl border border-gray-800 bg-gray-800/50 p-6 backdrop-blur transition-all hover:border-gray-700 hover:shadow-2xl"
                style={{ animationDelay: `${f.delay}ms` }}
              >
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${f.gradient} text-2xl shadow-lg`}>
                  {f.icon}
                </div>
                <div className="flex items-center gap-2 mb-3">
                  <h3 className="text-xl font-bold text-white">{f.title}</h3>
                  <span className="rounded-full bg-brand-600 px-2 py-0.5 text-[10px] font-bold text-white">{f.tag}</span>
                </div>
                <ul className="space-y-2">
                  {f.points.map((point, j) => (
                    <li key={j} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-brand-400" />
                      {point}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── MORE FEATURES (P1) ─── */}
      <section className="py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-amber-50 px-4 py-1 text-xs font-semibold text-amber-700">
              🚀 Professional Features
            </div>
            <h2 className="text-4xl font-extrabold text-gray-900">
              Enterprise-ready capabilities
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-500">
              Live sessions, certifications, badges, and skills assessments for the complete learning lifecycle.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { icon: "🔴", title: "Live Sessions & Webinars", desc: "Schedule, record, and transcribe live training with Zoom/Jitsi integration." },
              { icon: "📜", title: "Certifications", desc: "Auto-issue PDF certificates upon completion with expiry tracking." },
              { icon: "🏅", title: "Badges & Achievements", desc: "5 badge types: completion, excellence, speed, streak, and mentor." },
              { icon: "📐", title: "Skills Gap Analysis", desc: "Pre/post assessments with improvement tracking and radar charts." },
              { icon: "🎥", title: "AI Video Summaries", desc: "Auto-generated summaries, chapter markers, and searchable transcripts." },
              { icon: "💬", title: "Discussion Forums", desc: "Course-specific forums with AI moderation and auto-replies." },
              { icon: "📦", title: "SCORM/xAPI Ready", desc: "Import/export SCORM packages. Track via xAPI statements." },
              { icon: "🐳", title: "Docker + Helm Deploy", desc: "Containerized with Kubernetes support. CI/CD with GitHub Actions." },
            ].map((f, i) => (
              <div key={i} className="group rounded-xl border border-gray-100 bg-white p-6 shadow-sm transition-all hover:shadow-md hover:border-brand-200">
                <div className="mb-3 text-2xl">{f.icon}</div>
                <h3 className="mb-1 font-bold text-gray-900 text-sm">{f.title}</h3>
                <p className="text-xs leading-relaxed text-gray-500">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── STATS ─── */}
      <section className="bg-gradient-to-r from-brand-600 to-orange-500 py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid grid-cols-2 gap-8 text-center lg:grid-cols-4">
            {[
              { value: "55+", label: "API Endpoints" },
              { value: "17", label: "Data Models" },
              { value: "99.9%", label: "Uptime SLA" },
              { value: "30+", label: "Test Cases" },
            ].map((s, i) => (
              <div key={i}>
                <div className="text-4xl font-extrabold text-white">{s.value}</div>
                <div className="mt-1 text-sm font-medium text-orange-100">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── TECH STACK ─── */}
      <section className="py-24 bg-gray-50">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mb-16 text-center">
            <h2 className="text-4xl font-extrabold text-gray-900">Built on Modern Stack</h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-500">
              Production-grade architecture designed for scale and reliability.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { name: "FastAPI", role: "Backend", desc: "Python async framework with auto OpenAPI docs", color: "bg-teal-100 text-teal-700" },
              { name: "Next.js 14", role: "Frontend", desc: "App Router + Server Components", color: "bg-gray-900 text-white" },
              { name: "PostgreSQL", role: "Database", desc: "Async SQLAlchemy 2.0 + Alembic migrations", color: "bg-blue-100 text-blue-700" },
              { name: "Docker", role: "Infrastructure", desc: "Containerized with Helm + Kubernetes", color: "bg-sky-100 text-sky-700" },
            ].map((t, i) => (
              <div key={i} className="rounded-xl border border-gray-200 bg-white p-6 text-center shadow-sm">
                <span className={`inline-block rounded-lg px-3 py-1 text-xs font-bold mb-3 ${t.color}`}>{t.role}</span>
                <h3 className="text-lg font-bold text-gray-900">{t.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section id="pricing" className="py-24">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-4xl font-extrabold text-gray-900">
            Ready to transform your training?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg text-gray-500">
            Open source. Self-hosted. AI-powered. Start training your team today.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              href="/dashboard"
              className="rounded-xl bg-brand-600 px-8 py-4 text-base font-bold text-white shadow-lg shadow-brand-200 hover:bg-brand-700 transition-all"
            >
              Launch Dashboard →
            </Link>
            <a
              href="https://github.com/dclawstack/dclaw-train"
              target="_blank"
              rel="noreferrer"
              className="rounded-xl border border-gray-300 bg-white px-8 py-4 text-base font-semibold text-gray-700 hover:bg-gray-50 transition-all"
            >
              View on GitHub
            </a>
          </div>
          <p className="mt-6 text-sm text-gray-400">
            Free and open source. No credit card required.
          </p>
        </div>
      </section>

      {/* ─── FOOTER ─── */}
      <footer className="border-t border-gray-100 bg-gray-50 py-12">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-xl">🚂</span>
                <span className="font-bold text-gray-900">DClaw Train</span>
              </div>
              <p className="text-sm text-gray-500">AI-powered learning management system. Built on the DClaw Stack.</p>
            </div>
            <div>
              <h4 className="mb-3 text-sm font-bold text-gray-900">Product</h4>
              <div className="space-y-1 text-sm text-gray-500">
                <p>AI Tutor</p>
                <p>Course Builder</p>
                <p>Quiz Generator</p>
                <p>Analytics</p>
              </div>
            </div>
            <div>
              <h4 className="mb-3 text-sm font-bold text-gray-900">Resources</h4>
              <div className="space-y-1 text-sm text-gray-500">
                <p>Documentation</p>
                <p>API Reference</p>
                <p>GitHub</p>
                <p>Docker Hub</p>
              </div>
            </div>
            <div>
              <h4 className="mb-3 text-sm font-bold text-gray-900">Contact</h4>
              <div className="space-y-1 text-sm text-gray-500">
                <p>Ramsai Kamavaram</p>
                <p className="text-brand-600">kamavaram.ramsai@gmail.com</p>
                <p>Built on DClaw Stack</p>
              </div>
            </div>
          </div>
          <div className="mt-10 border-t border-gray-200 pt-6 text-center text-xs text-gray-400">
            © {new Date().getFullYear()} DClaw Train. Open source under MIT License.
          </div>
        </div>
      </footer>
    </div>
  );
}
