"use client";

import { useState, useRef, useEffect } from "react";
import { tutorApi, TutorConversation } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Props {
  learnerId: string;
  lessonId?: string;
  courseId?: string;
}

export default function TutorBot({ learnerId, lessonId, courseId }: Props) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggested, setSuggested] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(content?: string) {
    const text = content || input.trim();
    if (!text || loading) return;

    const userMsg: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setSuggested([]);
    setLoading(true);

    try {
      const res = await tutorApi.ask(learnerId, text, lessonId, courseId);
      const aiMsg: Message = { role: "assistant", content: res.reply };
      setMessages((prev) => [...prev, aiMsg]);
      setSuggested(res.suggested_questions || []);
    } catch (e: any) {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I'm having trouble. Try again." }]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <>
      {/* Floating button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-brand text-white shadow-lg hover:bg-orange-600 transition-colors"
          title="Ask AI Tutor"
        >
          <span className="text-2xl">🤖</span>
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div className="fixed bottom-6 right-6 z-50 flex h-[500px] w-[380px] flex-col rounded-xl border bg-white shadow-2xl">
          {/* Header */}
          <div className="flex items-center justify-between rounded-t-xl bg-brand px-4 py-3 text-white">
            <div>
              <h3 className="text-sm font-semibold">AI Learning Copilot</h3>
              <p className="text-xs text-orange-100">Ask me anything about this lesson</p>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="rounded-md p-1 hover:bg-orange-600"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
            {messages.length === 0 && (
              <div className="py-8 text-center text-sm text-gray-400">
                <p className="mb-2 text-3xl">🤖</p>
                <p className="font-medium text-gray-500">Your 24/7 AI Tutor</p>
                <p className="mt-1">I can explain concepts, answer questions, and guide your learning.</p>
                <p className="mt-2 text-xs text-orange-500">
                  💡 I use Socratic questioning — I won't give away direct answers!
                </p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                    msg.role === "user"
                      ? "bg-brand text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="rounded-lg bg-gray-100 px-3 py-2 text-sm text-gray-400">
                  Thinking...
                </div>
              </div>
            )}

            {/* Suggested questions */}
            {suggested.length > 0 && (
              <div className="space-y-1 pt-1">
                <p className="text-xs text-gray-400">Suggested questions:</p>
                {suggested.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(q)}
                    className="block w-full rounded-md border border-gray-200 px-3 py-1.5 text-left text-xs text-gray-600 hover:bg-orange-50 hover:border-brand"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t px-4 py-3">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a question..."
                className="flex-1 rounded-md border px-3 py-2 text-sm focus:border-brand focus:outline-none"
                disabled={loading}
              />
              <button
                onClick={() => sendMessage()}
                disabled={loading || !input.trim()}
                className="rounded-md bg-brand px-3 py-2 text-sm font-medium text-white hover:bg-orange-600 disabled:opacity-50"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
