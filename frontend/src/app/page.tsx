"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handle = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", handle);
    return () => window.removeEventListener("scroll", handle);
  }, []);

  return (
    <div style={{ background: "#05060f", color: "#e2e8f0", fontFamily: "'Inter', sans-serif", overflowX: "hidden" }}>

      {/* ── NAVBAR ── */}
      <nav style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 100,
        padding: "0 2rem",
        height: "64px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        background: scrolled ? "rgba(5,6,15,0.85)" : "transparent",
        backdropFilter: scrolled ? "blur(20px)" : "none",
        borderBottom: scrolled ? "1px solid rgba(255,255,255,0.06)" : "none",
        transition: "all 0.3s ease",
      }}>
        <Link href="/" style={{ display: "flex", alignItems: "center", gap: "10px", textDecoration: "none" }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: "linear-gradient(135deg, #f97316, #fb923c)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 16, boxShadow: "0 0 20px rgba(249,115,22,0.4)",
          }}>🚂</div>
          <span style={{ fontWeight: 700, fontSize: "1rem", color: "#fff", letterSpacing: "-0.02em" }}>
            DClaw <span style={{ color: "#fb923c" }}>Train</span>
          </span>
        </Link>

        <div style={{ display: "flex", gap: "2rem" }}>
          {["Features", "AI", "Enterprise", "Pricing"].map((l) => (
            <a key={l} href={`#${l.toLowerCase()}`} style={{
              color: "#94a3b8", fontSize: "0.875rem", fontWeight: 500,
              textDecoration: "none", transition: "color 0.2s",
            }}
              onMouseEnter={e => (e.currentTarget.style.color = "#f1f5f9")}
              onMouseLeave={e => (e.currentTarget.style.color = "#94a3b8")}
            >{l}</a>
          ))}
        </div>

        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
          <Link href="/dashboard" style={{
            color: "#94a3b8", fontSize: "0.875rem", fontWeight: 500,
            textDecoration: "none", padding: "6px 14px",
          }}>Sign In</Link>
          <Link href="/dashboard" style={{
            background: "linear-gradient(135deg, #ea580c, #f97316)",
            color: "#fff", fontWeight: 600, fontSize: "0.875rem",
            padding: "8px 20px", borderRadius: "8px", textDecoration: "none",
            boxShadow: "0 0 24px rgba(249,115,22,0.35)",
            transition: "box-shadow 0.2s",
          }}>Get Started →</Link>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section style={{
        minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center",
        textAlign: "center", padding: "120px 1.5rem 80px",
        position: "relative", overflow: "hidden",
      }}>
        {/* Dot grid */}
        <div style={{
          position: "absolute", inset: 0, opacity: 0.18,
          backgroundImage: "radial-gradient(circle, #334155 1px, transparent 1px)",
          backgroundSize: "28px 28px",
        }} />
        {/* Orange glow orb top-center */}
        <div style={{
          position: "absolute", top: "-100px", left: "50%", transform: "translateX(-50%)",
          width: "600px", height: "600px", borderRadius: "50%",
          background: "radial-gradient(circle, rgba(249,115,22,0.12) 0%, transparent 70%)",
          pointerEvents: "none",
        }} />

        <div style={{ position: "relative", maxWidth: "820px" }}>
          {/* Badge */}
          <div style={{
            display: "inline-flex", alignItems: "center", gap: "8px",
            border: "1px solid rgba(249,115,22,0.35)",
            background: "rgba(249,115,22,0.08)",
            borderRadius: "999px", padding: "6px 16px",
            fontSize: "0.75rem", fontWeight: 600, color: "#fb923c",
            marginBottom: "28px", backdropFilter: "blur(8px)",
          }}>
            <span style={{
              width: 6, height: 6, borderRadius: "50%",
              background: "#fb923c", display: "inline-block",
              boxShadow: "0 0 8px #fb923c",
            }} />
            AI-Powered Learning Platform · v1.2
          </div>

          {/* Headline */}
          <h1 style={{
            fontSize: "clamp(2.6rem, 6vw, 4.5rem)",
            fontWeight: 800, lineHeight: 1.05,
            letterSpacing: "-0.04em", margin: "0 0 24px",
            color: "#f8fafc",
          }}>
            Train your team at{" "}
            <span style={{
              background: "linear-gradient(90deg, #fb923c, #fbbf24)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            }}>lightspeed</span>
          </h1>

          <p style={{
            fontSize: "1.15rem", color: "#94a3b8", lineHeight: 1.7,
            maxWidth: "580px", margin: "0 auto 40px",
          }}>
            The AI-first LMS that auto-generates courses, quizzes, and personalized learning paths — powered by a 24/7 Socratic tutor that guides without giving away answers.
          </p>

          {/* CTAs */}
          <div style={{ display: "flex", gap: "12px", justifyContent: "center", flexWrap: "wrap" }}>
            <Link href="/dashboard" style={{
              background: "linear-gradient(135deg, #ea580c, #f97316)",
              color: "#fff", fontWeight: 700, fontSize: "0.9375rem",
              padding: "14px 32px", borderRadius: "10px", textDecoration: "none",
              boxShadow: "0 0 32px rgba(249,115,22,0.4)",
              display: "inline-flex", alignItems: "center", gap: "8px",
            }}>
              Start for Free <span>→</span>
            </Link>
            <Link href="/dashboard" style={{
              border: "1px solid rgba(255,255,255,0.1)",
              background: "rgba(255,255,255,0.04)",
              color: "#cbd5e1", fontWeight: 600, fontSize: "0.9375rem",
              padding: "14px 32px", borderRadius: "10px", textDecoration: "none",
              backdropFilter: "blur(12px)",
              display: "inline-flex", alignItems: "center", gap: "8px",
            }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#f87171", display: "inline-block" }} />
              View Dashboard
            </Link>
          </div>

          {/* Social proof */}
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "20px", marginTop: "40px" }}>
            <div style={{ display: "flex" }}>
              {["#8b5cf6","#3b82f6","#10b981","#f97316","#ec4899"].map((c, i) => (
                <div key={i} style={{
                  width: 32, height: 32, borderRadius: "50%",
                  background: c, border: "2px solid #05060f",
                  marginLeft: i > 0 ? -8 : 0, display: "flex",
                  alignItems: "center", justifyContent: "center",
                  fontSize: "0.7rem", fontWeight: 700, color: "#fff",
                }}>{String.fromCharCode(65 + i)}</div>
              ))}
            </div>
            <span style={{ color: "#64748b", fontSize: "0.875rem" }}>
              Trusted by <strong style={{ color: "#f1f5f9" }}>500+</strong> enterprise teams
            </span>
          </div>
        </div>

        {/* Bottom gradient fade */}
        <div style={{
          position: "absolute", bottom: 0, left: 0, right: 0, height: "120px",
          background: "linear-gradient(to top, #05060f, transparent)",
          pointerEvents: "none",
        }} />
      </section>

      {/* ── LOGOS BAR ── */}
      <section style={{ borderTop: "1px solid rgba(255,255,255,0.05)", borderBottom: "1px solid rgba(255,255,255,0.05)", padding: "32px 1.5rem", background: "rgba(255,255,255,0.01)" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto", textAlign: "center" }}>
          <p style={{ color: "#334155", fontSize: "0.7rem", fontWeight: 700, letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "20px" }}>
            Trusted by industry leaders
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "40px" }}>
            {["Acme Corp", "TechFlow", "DataSphere", "InnovateLabs", "NexusAI", "BuildCo"].map(b => (
              <span key={b} style={{ color: "#334155", fontWeight: 700, fontSize: "0.9rem", letterSpacing: "0.05em" }}>{b}</span>
            ))}
          </div>
        </div>
      </section>

      {/* ── CORE FEATURES ── */}
      <section id="features" style={{ padding: "100px 1.5rem" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "60px" }}>
            <div style={{
              display: "inline-flex", alignItems: "center", gap: "6px",
              border: "1px solid rgba(249,115,22,0.3)", background: "rgba(249,115,22,0.08)",
              borderRadius: "999px", padding: "5px 14px",
              fontSize: "0.72rem", fontWeight: 700, color: "#fb923c",
              letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "20px",
            }}>⚡ Core Platform</div>
            <h2 style={{ fontSize: "clamp(2rem,4vw,3rem)", fontWeight: 800, letterSpacing: "-0.03em", color: "#f8fafc", margin: "0 0 16px" }}>
              Everything you need to<br />
              <span style={{ background: "linear-gradient(90deg,#fb923c,#fbbf24)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>train at scale</span>
            </h2>
            <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: "520px", margin: "0 auto", lineHeight: 1.7 }}>
              Course creation to learner analytics — AI-powered and built on production-grade infrastructure.
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "16px" }}>
            {[
              { icon: "📚", title: "Course & Library CRUD", desc: "Create, organize and manage training courses with rich media. Full CRUD with real PostgreSQL.", accent: "#3b82f6" },
              { icon: "🎬", title: "Lesson & Video CMS", desc: "Structured lessons with video uploads, rich text, resource attachments and drag-and-drop reorder.", accent: "#8b5cf6" },
              { icon: "📝", title: "Quiz & Assessment Builder", desc: "MCQ, T/F, short answer and essay types with auto-scoring, passing thresholds and feedback.", accent: "#f59e0b" },
              { icon: "📊", title: "Learner Progress Tracking", desc: "Per-learner progress, time tracking, completion stats and score aggregation across all courses.", accent: "#10b981" },
            ].map((f) => (
              <GradientCard key={f.title} accent={f.accent}>
                <div style={{ fontSize: "1.75rem", marginBottom: "16px" }}>{f.icon}</div>
                <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "#f1f5f9", margin: "0 0 10px" }}>{f.title}</h3>
                <p style={{ fontSize: "0.8125rem", color: "#64748b", lineHeight: 1.6, margin: 0 }}>{f.desc}</p>
              </GradientCard>
            ))}
          </div>
        </div>
      </section>

      {/* ── AI PLATFORM ── */}
      <section id="ai" style={{ padding: "100px 1.5rem", background: "rgba(255,255,255,0.01)", position: "relative", overflow: "hidden" }}>
        {/* Glow */}
        <div style={{
          position: "absolute", top: "50%", left: "50%",
          transform: "translate(-50%,-50%)",
          width: "800px", height: "400px", borderRadius: "50%",
          background: "radial-gradient(ellipse, rgba(249,115,22,0.06) 0%, transparent 70%)",
          pointerEvents: "none",
        }} />
        <div style={{ maxWidth: "1100px", margin: "0 auto", position: "relative" }}>
          <div style={{ textAlign: "center", marginBottom: "60px" }}>
            <div style={{
              display: "inline-flex", alignItems: "center", gap: "6px",
              border: "1px solid rgba(249,115,22,0.3)", background: "rgba(249,115,22,0.08)",
              borderRadius: "999px", padding: "5px 14px",
              fontSize: "0.72rem", fontWeight: 700, color: "#fb923c",
              letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "20px",
            }}>🤖 AI Platform</div>
            <h2 style={{ fontSize: "clamp(2rem,4vw,3rem)", fontWeight: 800, letterSpacing: "-0.03em", color: "#f8fafc", margin: "0 0 16px" }}>
              AI that{" "}
              <span style={{ background: "linear-gradient(90deg,#fb923c,#fbbf24)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>teaches</span>
              , not just generates
            </h2>
            <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: "520px", margin: "0 auto", lineHeight: 1.7 }}>
              Socratic questioning, personalized paths, and smart content generation — never just handing out answers.
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))", gap: "16px" }}>
            {[
              {
                icon: "🧑‍🏫", title: "AI Learning Copilot", badge: "P0 — Core",
                badgeColor: "rgba(249,115,22,0.15)", badgeText: "#fb923c",
                accent: "#f97316",
                points: [
                  "24/7 tutor with RAG over course content",
                  "Socratic questioning — hints, not answers",
                  "Context-aware per lesson and course",
                  "Conversation memory per learner",
                  "Floating chat widget with smart suggestions",
                ],
              },
              {
                icon: "⚡", title: "AI Quiz Generator", badge: "P0 — Core",
                badgeColor: "rgba(139,92,246,0.15)", badgeText: "#a78bfa",
                accent: "#8b5cf6",
                points: [
                  "Auto-generate from lesson transcripts",
                  "MCQ, True/False, short answer types",
                  "Easy / medium / hard difficulty levels",
                  "Smart distractor generation",
                  "One-click add to any lesson",
                ],
              },
              {
                icon: "🎯", title: "AI Learning Paths", badge: "P1 — Pro",
                badgeColor: "rgba(16,185,129,0.15)", badgeText: "#34d399",
                accent: "#10b981",
                points: [
                  "Role and skills-gap based recommendations",
                  "Career goal alignment scoring",
                  "Priority-ranked course suggestions",
                  "Skills gap visualization",
                  "Auto-regenerates as you progress",
                ],
              },
            ].map((f) => (
              <GradientCard key={f.title} accent={f.accent}>
                <div style={{
                  width: 44, height: 44, borderRadius: 10,
                  background: "rgba(255,255,255,0.05)",
                  border: "1px solid rgba(255,255,255,0.08)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: "1.4rem", marginBottom: "16px",
                }}>{f.icon}</div>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "14px" }}>
                  <h3 style={{ fontSize: "1rem", fontWeight: 700, color: "#f1f5f9", margin: 0 }}>{f.title}</h3>
                  <span style={{
                    background: f.badgeColor, color: f.badgeText,
                    border: `1px solid ${f.badgeText}40`,
                    borderRadius: "999px", padding: "2px 10px",
                    fontSize: "0.68rem", fontWeight: 700,
                  }}>{f.badge}</span>
                </div>
                <ul style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: "10px" }}>
                  {f.points.map((p) => (
                    <li key={p} style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "0.8125rem", color: "#64748b" }}>
                      <span style={{
                        width: 5, height: 5, borderRadius: "50%",
                        background: f.accent, flexShrink: 0, marginTop: 6,
                        boxShadow: `0 0 6px ${f.accent}`,
                      }} />
                      {p}
                    </li>
                  ))}
                </ul>
              </GradientCard>
            ))}
          </div>
        </div>
      </section>

      {/* ── ENTERPRISE ── */}
      <section id="enterprise" style={{ padding: "100px 1.5rem" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "60px" }}>
            <div style={{
              display: "inline-flex", alignItems: "center", gap: "6px",
              border: "1px solid rgba(251,191,36,0.3)", background: "rgba(251,191,36,0.08)",
              borderRadius: "999px", padding: "5px 14px",
              fontSize: "0.72rem", fontWeight: 700, color: "#fbbf24",
              letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "20px",
            }}>🚀 Enterprise</div>
            <h2 style={{ fontSize: "clamp(2rem,4vw,3rem)", fontWeight: 800, letterSpacing: "-0.03em", color: "#f8fafc", margin: "0 0 16px" }}>
              Enterprise-ready{" "}
              <span style={{ background: "linear-gradient(90deg,#fbbf24,#f97316)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>capabilities</span>
            </h2>
            <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: "520px", margin: "0 auto", lineHeight: 1.7 }}>
              Live sessions, certifications, badges, SCORM compliance, and skills assessments for the full learning lifecycle.
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: "12px" }}>
            {[
              { icon: "🔴", title: "Live Sessions", desc: "Schedule, record, and transcribe live training with Zoom/Jitsi.", accent: "#ef4444" },
              { icon: "📜", title: "Certifications", desc: "Auto-issue PDF certificates on completion with expiry tracking.", accent: "#f59e0b" },
              { icon: "🏅", title: "Badges & Achievements", desc: "5 badge types: completion, excellence, speed, streak, mentor.", accent: "#f97316" },
              { icon: "📐", title: "Skills Gap Analysis", desc: "Pre/post assessments with radar charts and improvement tracking.", accent: "#8b5cf6" },
              { icon: "🎥", title: "AI Video Summaries", desc: "Auto-generated chapter markers, summaries and transcripts.", accent: "#3b82f6" },
              { icon: "💬", title: "Discussion Forums", desc: "Course forums with AI moderation and auto Q&A responses.", accent: "#10b981" },
              { icon: "📦", title: "SCORM / xAPI", desc: "Import/export SCORM packages. Track via xAPI statements.", accent: "#14b8a6" },
              { icon: "🐳", title: "Docker + Helm", desc: "Containerized, Kubernetes-ready, CI/CD and self-hostable.", accent: "#0ea5e9" },
            ].map((f) => (
              <GradientCard key={f.title} accent={f.accent} small>
                <div style={{ fontSize: "1.5rem", marginBottom: "12px" }}>{f.icon}</div>
                <h3 style={{ fontSize: "0.875rem", fontWeight: 700, color: "#f1f5f9", margin: "0 0 6px" }}>{f.title}</h3>
                <p style={{ fontSize: "0.78rem", color: "#64748b", lineHeight: 1.6, margin: 0 }}>{f.desc}</p>
              </GradientCard>
            ))}
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section style={{ padding: "80px 1.5rem", position: "relative", overflow: "hidden" }}>
        <div style={{
          position: "absolute", inset: 0,
          background: "linear-gradient(135deg, rgba(234,88,12,0.08) 0%, rgba(251,191,36,0.04) 50%, rgba(234,88,12,0.08) 100%)",
          borderTop: "1px solid rgba(249,115,22,0.12)",
          borderBottom: "1px solid rgba(249,115,22,0.12)",
        }} />
        <div style={{ maxWidth: "900px", margin: "0 auto", position: "relative" }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "32px", textAlign: "center" }}>
            {[
              { value: "55+", label: "API Endpoints", sub: "Production-grade REST" },
              { value: "17", label: "Data Models", sub: "Complete schema coverage" },
              { value: "99.9%", label: "Uptime SLA", sub: "Enterprise reliability" },
              { value: "30+", label: "Test Cases", sub: "Fully tested backend" },
            ].map((s) => (
              <div key={s.label}>
                <div style={{
                  fontSize: "clamp(2.5rem,5vw,3.5rem)", fontWeight: 900,
                  background: "linear-gradient(90deg,#fb923c,#fbbf24)",
                  WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                  lineHeight: 1, letterSpacing: "-0.04em",
                }}>{s.value}</div>
                <div style={{ fontSize: "0.9375rem", fontWeight: 700, color: "#e2e8f0", margin: "6px 0 4px" }}>{s.label}</div>
                <div style={{ fontSize: "0.78rem", color: "#475569" }}>{s.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── TECH STACK ── */}
      <section style={{ padding: "100px 1.5rem", background: "rgba(255,255,255,0.01)" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "56px" }}>
            <h2 style={{ fontSize: "clamp(1.75rem,3.5vw,2.5rem)", fontWeight: 800, letterSpacing: "-0.03em", color: "#f8fafc", margin: "0 0 12px" }}>
              Built on Modern Stack
            </h2>
            <p style={{ color: "#64748b", fontSize: "1rem", maxWidth: "420px", margin: "0 auto" }}>
              Production-grade architecture built for scale and developer experience.
            </p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(230px,1fr))", gap: "16px" }}>
            {[
              { name: "FastAPI", role: "Backend", desc: "Python async framework. 55+ routes, auto OpenAPI docs, Alembic migrations.", accent: "#14b8a6" },
              { name: "Next.js 14", role: "Frontend", desc: "App Router + Server Components. TypeScript-first, mobile-responsive.", accent: "#e2e8f0" },
              { name: "PostgreSQL", role: "Database", desc: "Async SQLAlchemy 2.0 + Alembic. 17 models with full relationship graphs.", accent: "#3b82f6" },
              { name: "Docker + K8s", role: "Infrastructure", desc: "Helm charts, cloud-native, CI/CD-ready and self-hostable.", accent: "#0ea5e9" },
            ].map((t) => (
              <GradientCard key={t.name} accent={t.accent}>
                <div style={{ fontSize: "0.7rem", fontWeight: 700, letterSpacing: "0.12em", textTransform: "uppercase", color: "#475569", marginBottom: "8px" }}>{t.role}</div>
                <div style={{ fontSize: "1.5rem", fontWeight: 800, color: t.accent, marginBottom: "12px", letterSpacing: "-0.02em" }}>{t.name}</div>
                <p style={{ fontSize: "0.8125rem", color: "#64748b", lineHeight: 1.6, margin: 0 }}>{t.desc}</p>
              </GradientCard>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section id="pricing" style={{ padding: "120px 1.5rem", textAlign: "center", position: "relative", overflow: "hidden" }}>
        <div style={{
          position: "absolute", top: 0, left: "50%", transform: "translateX(-50%)",
          width: "700px", height: "400px",
          background: "radial-gradient(ellipse, rgba(249,115,22,0.1) 0%, transparent 70%)",
          pointerEvents: "none",
        }} />
        <div style={{ position: "relative", maxWidth: "640px", margin: "0 auto" }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: "6px",
            border: "1px solid rgba(249,115,22,0.3)", background: "rgba(249,115,22,0.08)",
            borderRadius: "999px", padding: "5px 14px",
            fontSize: "0.72rem", fontWeight: 700, color: "#fb923c",
            letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "28px",
          }}>🎉 Free &amp; Open Source</div>
          <h2 style={{ fontSize: "clamp(2rem,4vw,3.25rem)", fontWeight: 800, letterSpacing: "-0.04em", color: "#f8fafc", margin: "0 0 20px" }}>
            Ready to transform<br />
            <span style={{ background: "linear-gradient(90deg,#fb923c,#fbbf24)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              your training?
            </span>
          </h2>
          <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: "460px", margin: "0 auto 40px", lineHeight: 1.7 }}>
            Self-hosted, open source, AI-powered. Start training your team today — no credit card required.
          </p>
          <div style={{ display: "flex", gap: "12px", justifyContent: "center", flexWrap: "wrap" }}>
            <Link href="/dashboard" style={{
              background: "linear-gradient(135deg,#ea580c,#f97316)",
              color: "#fff", fontWeight: 700, fontSize: "0.9375rem",
              padding: "14px 32px", borderRadius: "10px", textDecoration: "none",
              boxShadow: "0 0 32px rgba(249,115,22,0.4)",
              display: "inline-flex", alignItems: "center", gap: "8px",
            }}>Launch Dashboard →</Link>
            <a href="#" style={{
              border: "1px solid rgba(255,255,255,0.1)", background: "rgba(255,255,255,0.04)",
              color: "#94a3b8", fontWeight: 600, fontSize: "0.9375rem",
              padding: "14px 32px", borderRadius: "10px", textDecoration: "none",
              backdropFilter: "blur(12px)",
              display: "inline-flex", alignItems: "center", gap: "8px",
            }}>⭐ View on GitHub</a>
          </div>
          <p style={{ marginTop: "20px", fontSize: "0.8125rem", color: "#334155" }}>MIT License · Self-hostable · Open Source</p>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={{ borderTop: "1px solid rgba(255,255,255,0.05)", padding: "60px 1.5rem 32px", background: "#030509" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(200px,1fr))", gap: "40px", marginBottom: "48px" }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "14px" }}>
                <div style={{ width: 28, height: 28, borderRadius: 7, background: "linear-gradient(135deg,#f97316,#fb923c)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.9rem" }}>🚂</div>
                <span style={{ fontWeight: 700, color: "#f1f5f9" }}>DClaw <span style={{ color: "#fb923c" }}>Train</span></span>
              </div>
              <p style={{ color: "#334155", fontSize: "0.8125rem", lineHeight: 1.7, maxWidth: "200px" }}>
                AI-powered LMS. Built on the DClaw Stack.
              </p>
              <div style={{ display: "flex", gap: "8px", marginTop: "16px" }}>
                {["GitHub", "Twitter"].map(s => (
                  <a key={s} href="#" style={{
                    border: "1px solid rgba(255,255,255,0.07)", background: "rgba(255,255,255,0.03)",
                    color: "#475569", fontSize: "0.75rem", fontWeight: 600,
                    padding: "5px 12px", borderRadius: "6px", textDecoration: "none",
                  }}>{s}</a>
                ))}
              </div>
            </div>
            <div>
              <h4 style={{ fontSize: "0.8125rem", fontWeight: 700, color: "#f1f5f9", marginBottom: "16px" }}>Product</h4>
              {["AI Tutor","Course Builder","Quiz Generator","Analytics","Live Sessions","Certifications"].map(i => (
                <p key={i} style={{ color: "#334155", fontSize: "0.8125rem", marginBottom: "8px", cursor: "pointer" }}>{i}</p>
              ))}
            </div>
            <div>
              <h4 style={{ fontSize: "0.8125rem", fontWeight: 700, color: "#f1f5f9", marginBottom: "16px" }}>Resources</h4>
              {["Documentation","API Reference","GitHub","Docker Hub","Changelog"].map(i => (
                <p key={i} style={{ color: "#334155", fontSize: "0.8125rem", marginBottom: "8px", cursor: "pointer" }}>{i}</p>
              ))}
            </div>
            <div>
              <h4 style={{ fontSize: "0.8125rem", fontWeight: 700, color: "#f1f5f9", marginBottom: "16px" }}>Contact</h4>
              <p style={{ color: "#f1f5f9", fontSize: "0.875rem", fontWeight: 600, marginBottom: "6px" }}>Ramsai Kamavaram</p>
              <a href="mailto:kamavaram.ramsai@gmail.com" style={{ color: "#fb923c", fontSize: "0.8125rem", textDecoration: "none" }}>
                kamavaram.ramsai@gmail.com
              </a>
              <div style={{
                marginTop: "16px", display: "inline-flex", alignItems: "center", gap: "7px",
                border: "1px solid rgba(16,185,129,0.3)", background: "rgba(16,185,129,0.08)",
                borderRadius: "999px", padding: "4px 12px",
                fontSize: "0.72rem", fontWeight: 600, color: "#34d399",
              }}>
                <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#34d399", boxShadow: "0 0 8px #34d399" }} />
                All systems operational
              </div>
            </div>
          </div>

          <div style={{ borderTop: "1px solid rgba(255,255,255,0.04)", paddingTop: "24px", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px" }}>
            <p style={{ color: "#1e293b", fontSize: "0.78rem" }}>© {new Date().getFullYear()} DClaw Train. Open source under MIT License.</p>
            <div style={{ display: "flex", gap: "20px" }}>
              {["Privacy Policy","Terms of Service","Security"].map(l => (
                <a key={l} href="#" style={{ color: "#1e293b", fontSize: "0.78rem", textDecoration: "none" }}>{l}</a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function GradientCard({ children, accent, small }: { children: React.ReactNode; accent: string; small?: boolean }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        position: "relative", borderRadius: "14px",
        padding: "1px",
        background: hovered
          ? `linear-gradient(135deg, ${accent}60, rgba(255,255,255,0.08))`
          : "linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02))",
        transition: "all 0.3s ease",
        transform: hovered ? "translateY(-2px)" : "none",
        boxShadow: hovered ? `0 16px 40px rgba(0,0,0,0.4), 0 0 30px ${accent}15` : "0 4px 20px rgba(0,0,0,0.2)",
      }}
    >
      <div style={{
        borderRadius: "13px",
        background: hovered ? "rgba(255,255,255,0.03)" : "rgba(255,255,255,0.02)",
        backdropFilter: "blur(8px)",
        padding: small ? "20px" : "24px",
        height: "100%",
        transition: "background 0.3s",
      }}>
        {children}
      </div>
    </div>
  );
}
