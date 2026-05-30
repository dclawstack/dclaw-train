"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", h);
    return () => window.removeEventListener("scroll", h);
  }, []);

  return (
    <div style={{ background: "#080810", minHeight: "100vh", color: "#c8d3e0" }}>

      {/* ── NAV ── */}
      <nav style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 50,
        height: 60,
        display: "flex", alignItems: "center",
        padding: "0 40px",
        background: scrolled ? "rgba(8,8,16,0.9)" : "transparent",
        backdropFilter: scrolled ? "blur(16px)" : "none",
        borderBottom: scrolled ? "1px solid rgba(255,255,255,0.06)" : "none",
        transition: "all 0.3s",
        justifyContent: "space-between",
      }}>
        <Link href="/" style={{ display:"flex", alignItems:"center", gap:10, textDecoration:"none" }}>
          <span style={{
            display:"flex", alignItems:"center", justifyContent:"center",
            width:30, height:30, borderRadius:7,
            background:"linear-gradient(135deg,#ea580c,#f97316)",
            fontSize:15,
          }}>🚂</span>
          <span style={{ fontWeight:700, fontSize:"0.9375rem", color:"#f1f5f9", letterSpacing:"-0.02em" }}>
            DClaw <span style={{ color:"#f97316" }}>Train</span>
          </span>
        </Link>

        <div style={{ display:"flex", gap:32 }}>
          {["Features","AI","Enterprise","Pricing"].map(l => (
            <a key={l} href={`#${l.toLowerCase()}`}
              style={{ color:"#64748b", fontSize:"0.8125rem", fontWeight:500, textDecoration:"none" }}
              onMouseEnter={e=>(e.currentTarget.style.color="#e2e8f0")}
              onMouseLeave={e=>(e.currentTarget.style.color="#64748b")}
            >{l}</a>
          ))}
        </div>

        <div style={{ display:"flex", gap:10, alignItems:"center" }}>
          <Link href="/dashboard" style={{ color:"#64748b", fontSize:"0.8125rem", fontWeight:500, textDecoration:"none", padding:"6px 12px" }}>
            Sign in
          </Link>
          <Link href="/dashboard" className="landing-btn-primary" style={{ fontSize:"0.8125rem", padding:"8px 18px" }}>
            Get Started
          </Link>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section style={{
        position:"relative", overflow:"hidden",
        display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center",
        textAlign:"center",
        minHeight:"100vh",
        padding:"120px 24px 80px",
      }}>
        {/* Radial glow — one centered, subtle */}
        <div style={{
          position:"absolute", top:0, left:"50%", transform:"translateX(-50%)",
          width:900, height:600, borderRadius:"50%",
          background:"radial-gradient(ellipse at center top, rgba(249,115,22,0.08) 0%, transparent 65%)",
          pointerEvents:"none",
        }}/>
        {/* Dot grid */}
        <div style={{
          position:"absolute", inset:0,
          backgroundImage:"radial-gradient(rgba(255,255,255,0.06) 1px, transparent 1px)",
          backgroundSize:"32px 32px",
          WebkitMaskImage:"radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%)",
          maskImage:"radial-gradient(ellipse 80% 80% at 50% 50%, black 40%, transparent 100%)",
          pointerEvents:"none",
        }}/>

        <div style={{ position:"relative", maxWidth:720 }}>
          {/* Pill badge */}
          <div style={{
            display:"inline-flex", alignItems:"center", gap:8,
            background:"rgba(249,115,22,0.06)",
            border:"1px solid rgba(249,115,22,0.18)",
            borderRadius:999, padding:"5px 16px",
            fontSize:"0.75rem", fontWeight:600, color:"#fb923c",
            marginBottom:32, letterSpacing:"0.02em",
          }}>
            <span style={{ width:6, height:6, borderRadius:"50%", background:"#f97316", display:"inline-block" }}/>
            AI-Powered Learning Management · v1.2
          </div>

          <h1 style={{
            margin:"0 0 24px",
            fontSize:"clamp(2.75rem,5.5vw,4.25rem)",
            fontWeight:800, lineHeight:1.08,
            letterSpacing:"-0.04em",
            color:"#f1f5f9",
          }}>
            Train your team<br />
            <span className="gradient-text">at lightspeed</span>
          </h1>

          <p style={{
            margin:"0 auto 40px",
            maxWidth:520,
            fontSize:"1.0625rem", lineHeight:1.7,
            color:"#64748b",
          }}>
            The AI-first LMS that generates courses, quizzes, and personalized learning paths —
            with a 24/7 Socratic tutor that guides without giving away answers.
          </p>

          <div style={{ display:"flex", gap:12, justifyContent:"center", flexWrap:"wrap" }}>
            <Link href="/dashboard" className="landing-btn-primary">
              Start for free →
            </Link>
            <Link href="/dashboard" className="landing-btn-ghost">
              View Dashboard
            </Link>
          </div>

          <div style={{
            display:"flex", alignItems:"center", justifyContent:"center",
            gap:16, marginTop:40, fontSize:"0.8125rem", color:"#475569",
          }}>
            <div style={{ display:"flex" }}>
              {["#6366f1","#0ea5e9","#10b981","#f97316","#e879f9"].map((c,i) => (
                <div key={i} style={{
                  width:28, height:28, borderRadius:"50%", background:c,
                  border:"2px solid #080810", marginLeft:i?-8:0,
                  display:"flex", alignItems:"center", justifyContent:"center",
                  fontSize:"0.65rem", fontWeight:700, color:"#fff",
                }}>{String.fromCharCode(65+i)}</div>
              ))}
            </div>
            <span>Trusted by <strong style={{ color:"#94a3b8" }}>500+</strong> teams worldwide</span>
          </div>
        </div>
      </section>

      {/* ── LOGO BAR ── */}
      <div style={{
        borderTop:"1px solid rgba(255,255,255,0.04)",
        borderBottom:"1px solid rgba(255,255,255,0.04)",
        padding:"28px 40px",
        display:"flex", justifyContent:"center", alignItems:"center",
        flexWrap:"wrap", gap:"48px",
      }}>
        <p style={{ color:"#1e293b", fontSize:"0.7rem", fontWeight:700, letterSpacing:"0.14em", textTransform:"uppercase", margin:0 }}>
          Trusted by
        </p>
        {["Acme Corp","TechFlow","DataSphere","InnovateLabs","NexusAI","BuildCo"].map(n=>(
          <span key={n} style={{ color:"#1e293b", fontWeight:700, fontSize:"0.875rem", letterSpacing:"0.04em" }}>{n}</span>
        ))}
      </div>

      {/* ── FEATURES ── */}
      <section id="features" style={{ padding:"100px 40px" }}>
        <div style={{ maxWidth:1080, margin:"0 auto" }}>
          <SectionHeader tag="Core Platform" title={<>Everything you need to<br/><span className="gradient-text">train at scale</span></>}
            sub="Course creation, lesson management, quizzes, and learner tracking — built on a production-grade stack." />

          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(230px,1fr))", gap:16 }}>
            {[
              { icon:"📚", title:"Course & Library CRUD", desc:"Create, organize, and manage training courses with full CRUD and real PostgreSQL persistence." },
              { icon:"🎬", title:"Lesson & Video CMS",   desc:"Structured lessons with video uploads, rich text content, resources, and reordering." },
              { icon:"📝", title:"Quiz Builder",         desc:"MCQ, T/F, short answer, and essay types. Auto-scoring, passing thresholds, and detailed feedback." },
              { icon:"📊", title:"Progress Tracking",    desc:"Per-learner progress, time-on-task, completion rates, and score aggregation across courses." },
            ].map(f=>(
              <div key={f.title} className="landing-card" style={{ padding:24 }}>
                <div style={{ fontSize:"1.5rem", marginBottom:16 }}>{f.icon}</div>
                <h3 style={{ margin:"0 0 8px", fontSize:"0.9375rem", fontWeight:700, color:"#e2e8f0", letterSpacing:"-0.01em" }}>{f.title}</h3>
                <p style={{ margin:0, fontSize:"0.8125rem", color:"#475569", lineHeight:1.65 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── AI ── */}
      <section id="ai" style={{ padding:"100px 40px", background:"rgba(255,255,255,0.015)" }}>
        <div style={{ maxWidth:1080, margin:"0 auto" }}>
          <SectionHeader tag="AI Platform" title={<>AI that <span className="gradient-text">teaches</span>,<br/>not just generates</>}
            sub="Socratic questioning, personalized paths, and smart content generation — guided learning, not spoon-feeding." />

          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:16 }}>
            {[
              {
                icon:"🧑‍🏫", title:"AI Learning Copilot", tag:"P0",
                points:["24/7 tutor with RAG over course content","Socratic method — hints, not answers","Context-aware per lesson and course","Conversation memory per learner","Floating chat widget with suggestions"],
              },
              {
                icon:"⚡", title:"AI Quiz Generator", tag:"P0",
                points:["Generate quizzes from lesson transcripts","MCQ, True/False, short answer types","Easy / medium / hard difficulty","Smart distractor generation","One-click add to any lesson"],
              },
              {
                icon:"🎯", title:"AI Learning Paths", tag:"P1",
                points:["Role and skills-gap based recommendations","Career goal alignment scoring","Priority-ranked course suggestions","Skills gap visualization","Auto-regenerates as you progress"],
              },
            ].map(f=>(
              <div key={f.title} className="landing-card" style={{ padding:24 }}>
                <div style={{ display:"flex", alignItems:"center", gap:12, marginBottom:20 }}>
                  <div style={{
                    width:40, height:40, borderRadius:8,
                    background:"rgba(249,115,22,0.08)",
                    border:"1px solid rgba(249,115,22,0.15)",
                    display:"flex", alignItems:"center", justifyContent:"center", fontSize:"1.25rem",
                  }}>{f.icon}</div>
                  <div>
                    <div style={{ display:"flex", alignItems:"center", gap:8 }}>
                      <h3 style={{ margin:0, fontSize:"0.9375rem", fontWeight:700, color:"#e2e8f0" }}>{f.title}</h3>
                      <span style={{
                        fontSize:"0.65rem", fontWeight:700, color:"#f97316",
                        background:"rgba(249,115,22,0.1)", border:"1px solid rgba(249,115,22,0.2)",
                        borderRadius:999, padding:"1px 8px",
                      }}>{f.tag}</span>
                    </div>
                  </div>
                </div>
                <ul style={{ margin:0, padding:0, listStyle:"none", display:"flex", flexDirection:"column", gap:9 }}>
                  {f.points.map(p=>(
                    <li key={p} style={{ display:"flex", alignItems:"flex-start", gap:10, fontSize:"0.8125rem", color:"#475569" }}>
                      <span style={{ width:4, height:4, borderRadius:"50%", background:"#f97316", flexShrink:0, marginTop:6 }}/>
                      {p}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── ENTERPRISE ── */}
      <section id="enterprise" style={{ padding:"100px 40px" }}>
        <div style={{ maxWidth:1080, margin:"0 auto" }}>
          <SectionHeader tag="Enterprise" title={<>Enterprise-ready<br/><span className="gradient-text">capabilities</span></>}
            sub="Live sessions, certifications, SCORM compliance, and skills assessments for the full learning lifecycle." />

          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(210px,1fr))", gap:12 }}>
            {[
              { icon:"🔴", title:"Live Sessions",        desc:"Schedule, record, and transcribe live training with Zoom/Jitsi integration." },
              { icon:"📜", title:"Certifications",       desc:"Auto-issue PDF certificates with expiry and revocation support." },
              { icon:"🏅", title:"Badges",               desc:"5 badge types: completion, excellence, speed, streak, mentor." },
              { icon:"📐", title:"Skills Gap Analysis",  desc:"Pre/post assessments with improvement tracking and visualization." },
              { icon:"🎥", title:"Video Summaries",      desc:"AI-generated chapter markers, summaries, and transcripts." },
              { icon:"💬", title:"Discussion Forums",    desc:"Course forums with AI moderation and auto Q&A." },
              { icon:"📦", title:"SCORM / xAPI",         desc:"Import/export SCORM packages. Track via xAPI statements." },
              { icon:"🐳", title:"Docker + Helm",        desc:"Cloud-native, Kubernetes-ready, CI/CD-friendly." },
            ].map(f=>(
              <div key={f.title} className="landing-card" style={{ padding:20 }}>
                <div style={{ fontSize:"1.375rem", marginBottom:10 }}>{f.icon}</div>
                <h3 style={{ margin:"0 0 6px", fontSize:"0.8125rem", fontWeight:700, color:"#e2e8f0" }}>{f.title}</h3>
                <p style={{ margin:0, fontSize:"0.75rem", color:"#475569", lineHeight:1.6 }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section style={{
        padding:"72px 40px",
        borderTop:"1px solid rgba(255,255,255,0.04)",
        borderBottom:"1px solid rgba(255,255,255,0.04)",
        background:"rgba(249,115,22,0.03)",
      }}>
        <div style={{ maxWidth:900, margin:"0 auto", display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(160px,1fr))", gap:32, textAlign:"center" }}>
          {[
            { val:"55+",   lab:"API Endpoints" },
            { val:"17",    lab:"Data Models" },
            { val:"99.9%", lab:"Uptime SLA" },
            { val:"30+",   lab:"Test Cases" },
          ].map(s=>(
            <div key={s.lab}>
              <div style={{ fontSize:"clamp(2rem,4vw,3rem)", fontWeight:800, letterSpacing:"-0.04em", lineHeight:1 }} className="gradient-text">{s.val}</div>
              <div style={{ marginTop:8, fontSize:"0.875rem", fontWeight:600, color:"#94a3b8" }}>{s.lab}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── TECH STACK ── */}
      <section style={{ padding:"100px 40px", background:"rgba(255,255,255,0.015)" }}>
        <div style={{ maxWidth:1080, margin:"0 auto" }}>
          <SectionHeader title={<>Built on a <span className="gradient-text">modern stack</span></>}
            sub="Production-grade architecture designed for scale, security, and developer experience." />
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(220px,1fr))", gap:16 }}>
            {[
              { name:"FastAPI",     role:"Backend",        desc:"Python async, auto OpenAPI docs, 55+ routes, Alembic migrations." },
              { name:"Next.js 14",  role:"Frontend",       desc:"App Router, Server Components, TypeScript-first, Tailwind CSS." },
              { name:"PostgreSQL",  role:"Database",       desc:"Async SQLAlchemy 2.0, Alembic migrations, 17 models." },
              { name:"Docker + K8s",role:"Infrastructure", desc:"Helm charts, cloud-native, CI/CD-ready, self-hostable." },
            ].map(t=>(
              <div key={t.name} className="landing-card" style={{ padding:24 }}>
                <div style={{ fontSize:"0.68rem", fontWeight:700, letterSpacing:"0.12em", textTransform:"uppercase", color:"#334155", marginBottom:8 }}>{t.role}</div>
                <div style={{ fontSize:"1.25rem", fontWeight:800, color:"#e2e8f0", letterSpacing:"-0.02em", marginBottom:10 }}>{t.name}</div>
                <p style={{ margin:0, fontSize:"0.8125rem", color:"#475569", lineHeight:1.65 }}>{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section id="pricing" style={{ padding:"120px 40px", textAlign:"center", position:"relative", overflow:"hidden" }}>
        <div style={{
          position:"absolute", top:0, left:"50%", transform:"translateX(-50%)",
          width:800, height:400,
          background:"radial-gradient(ellipse at top, rgba(249,115,22,0.07) 0%, transparent 65%)",
          pointerEvents:"none",
        }}/>
        <div style={{ position:"relative", maxWidth:580, margin:"0 auto" }}>
          <div className="section-tag">🎉 Free &amp; Open Source</div>
          <h2 style={{ margin:"0 0 20px", fontSize:"clamp(2rem,4vw,3rem)", fontWeight:800, letterSpacing:"-0.04em", color:"#f1f5f9" }}>
            Ready to transform<br/><span className="gradient-text">your training?</span>
          </h2>
          <p style={{ margin:"0 auto 40px", maxWidth:440, fontSize:"1rem", color:"#64748b", lineHeight:1.7 }}>
            Self-hosted, open source, AI-powered. No credit card required.
          </p>
          <div style={{ display:"flex", gap:12, justifyContent:"center", flexWrap:"wrap" }}>
            <Link href="/dashboard" className="landing-btn-primary">Launch Dashboard →</Link>
            <a href="#" className="landing-btn-ghost">⭐ GitHub</a>
          </div>
          <p style={{ marginTop:20, fontSize:"0.78rem", color:"#1e293b" }}>MIT License · Self-hostable · Open Source</p>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer style={{ borderTop:"1px solid rgba(255,255,255,0.05)", padding:"56px 40px 32px", background:"#050508" }}>
        <div style={{ maxWidth:1080, margin:"0 auto" }}>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(180px,1fr))", gap:40, marginBottom:48 }}>
            <div>
              <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:12 }}>
                <span style={{
                  width:26, height:26, borderRadius:6,
                  background:"linear-gradient(135deg,#ea580c,#f97316)",
                  display:"flex", alignItems:"center", justifyContent:"center", fontSize:"0.875rem",
                }}>🚂</span>
                <span style={{ fontWeight:700, color:"#e2e8f0", fontSize:"0.9375rem" }}>
                  DClaw <span style={{ color:"#f97316" }}>Train</span>
                </span>
              </div>
              <p style={{ margin:"0 0 16px", fontSize:"0.8125rem", color:"#1e293b", lineHeight:1.7, maxWidth:180 }}>
                AI-powered LMS built on the DClaw Stack.
              </p>
            </div>

            {[
              { heading:"Product",   items:["AI Tutor","Course Builder","Quiz Generator","Analytics","Live Sessions"] },
              { heading:"Resources", items:["Docs","API Reference","GitHub","Docker Hub","Changelog"] },
            ].map(col=>(
              <div key={col.heading}>
                <h4 style={{ margin:"0 0 14px", fontSize:"0.78rem", fontWeight:700, color:"#e2e8f0", letterSpacing:"0.08em", textTransform:"uppercase" }}>{col.heading}</h4>
                {col.items.map(i=>(
                  <p key={i} style={{ margin:"0 0 8px", fontSize:"0.8125rem", color:"#1e293b" }}>{i}</p>
                ))}
              </div>
            ))}

            <div>
              <h4 style={{ margin:"0 0 14px", fontSize:"0.78rem", fontWeight:700, color:"#e2e8f0", letterSpacing:"0.08em", textTransform:"uppercase" }}>Contact</h4>
              <p style={{ margin:"0 0 4px", fontSize:"0.875rem", fontWeight:600, color:"#e2e8f0" }}>Ramsai Kamavaram</p>
              <a href="mailto:kamavaram.ramsai@gmail.com" style={{ fontSize:"0.8125rem", color:"#f97316", textDecoration:"none" }}>
                kamavaram.ramsai@gmail.com
              </a>
              <div style={{
                marginTop:16, display:"inline-flex", alignItems:"center", gap:6,
                background:"rgba(16,185,129,0.06)", border:"1px solid rgba(16,185,129,0.18)",
                borderRadius:999, padding:"4px 12px",
                fontSize:"0.7rem", fontWeight:600, color:"#34d399",
              }}>
                <span style={{ width:5, height:5, borderRadius:"50%", background:"#34d399" }}/>
                All systems operational
              </div>
            </div>
          </div>

          <div style={{
            borderTop:"1px solid rgba(255,255,255,0.04)", paddingTop:24,
            display:"flex", justifyContent:"space-between", alignItems:"center",
            flexWrap:"wrap", gap:12,
          }}>
            <p style={{ margin:0, fontSize:"0.75rem", color:"#1e293b" }}>
              © {new Date().getFullYear()} DClaw Train — MIT License
            </p>
            <div style={{ display:"flex", gap:20 }}>
              {["Privacy","Terms","Security"].map(l=>(
                <a key={l} href="#" style={{ fontSize:"0.75rem", color:"#1e293b", textDecoration:"none" }}>{l}</a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function SectionHeader({ tag, title, sub }: { tag?: string; title: React.ReactNode; sub: string }) {
  return (
    <div style={{ textAlign:"center", marginBottom:56 }}>
      {tag && <div className="section-tag">{tag}</div>}
      <h2 style={{ margin:"0 0 16px", fontSize:"clamp(2rem,4vw,2.875rem)", fontWeight:800, letterSpacing:"-0.035em", color:"#f1f5f9", lineHeight:1.1 }}>
        {title}
      </h2>
      <p style={{ margin:"0 auto", maxWidth:520, fontSize:"1rem", color:"#64748b", lineHeight:1.7 }}>{sub}</p>
    </div>
  );
}
