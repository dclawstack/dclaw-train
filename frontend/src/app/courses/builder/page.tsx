"use client";

import { useState } from "react";
import { coursesApi, lessonsApi, quizzesApi, enrollmentsApi, progressApi, Course, Lesson, Quiz } from "@/lib/api";
import TutorBot from "@/components/tutor-bot";

export default function CourseBuilderPage() {
  const [courseId, setCourseId] = useState("");
  const [course, setCourse] = useState<any>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [lessonTitle, setLessonTitle] = useState("");
  const [lessonContent, setLessonContent] = useState("");
  const [addingLesson, setAddingLesson] = useState(false);

  const [selectedLesson, setSelectedLesson] = useState<string | null>(null);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);

  async function loadCourse() {
    if (!courseId.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const c = await coursesApi.structure(courseId);
      setCourse(c);
      const l = await lessonsApi.listByCourse(courseId);
      setLessons(l);
    } catch (e: any) {
      setError(e.message || "Failed to load course");
      setCourse(null);
      setLessons([]);
    } finally {
      setLoading(false);
    }
  }

  async function addLesson() {
    if (!lessonTitle.trim() || !courseId) return;
    setAddingLesson(true);
    try {
      await lessonsApi.create({
        course_id: courseId,
        title: lessonTitle,
        content: lessonContent,
        order: lessons.length,
        is_published: true,
      });
      setLessonTitle("");
      setLessonContent("");
      await loadCourse();
    } catch (e: any) {
      alert(e.message);
    } finally {
      setAddingLesson(false);
    }
  }

  async function handleDeleteLesson(lessonId: string) {
    if (!confirm("Delete this lesson?")) return;
    try {
      await lessonsApi.delete(lessonId);
      setLessons(lessons.filter((l) => l.id !== lessonId));
    } catch (e: any) {
      alert(e.message);
    }
  }

  async function loadQuizzes(lessonId: string) {
    setSelectedLesson(lessonId);
    try {
      const q = await quizzesApi.listByLesson(lessonId);
      setQuizzes(q);
    } catch {
      setQuizzes([]);
    }
  }

  async function generateQuiz(lessonId: string) {
    try {
      await quizzesApi.generate(lessonId, 5, "medium");
      await loadQuizzes(lessonId);
    } catch (e: any) {
      alert("Failed to generate quiz: " + e.message);
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-6 text-3xl font-bold text-brand">Course Builder</h1>

      {/* Course loader */}
      <div className="mb-6 flex gap-3">
        <input
          type="text"
          value={courseId}
          onChange={(e) => setCourseId(e.target.value)}
          placeholder="Paste course ID"
          className="flex-1 rounded-md border px-3 py-2 text-sm focus:border-brand focus:outline-none"
        />
        <button
          onClick={loadCourse}
          disabled={loading || !courseId.trim()}
          className="rounded-md bg-brand px-4 py-2 text-sm font-medium text-white hover:bg-orange-600 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Load Course"}
        </button>
      </div>

      {error && <div className="mb-4 rounded-md bg-red-50 px-4 py-3 text-sm text-red-600">{error}</div>}

      {course && (
        <>
          {/* Course header */}
          <div className="mb-6 rounded-lg border bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold">{course.title}</h2>
            <p className="mt-1 text-sm text-gray-500">
              Format: {course.format} · {course.lessons?.length || 0} lessons ·{" "}
              {course.is_published ? "Published" : "Draft"}
            </p>
            {course.description && <p className="mt-2 text-sm text-gray-600">{course.description}</p>}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Lessons panel */}
            <div>
              <h3 className="mb-3 text-lg font-semibold">Lessons</h3>

              {/* Add lesson form */}
              <div className="mb-4 rounded-lg border bg-white p-4 shadow-sm">
                <input
                  type="text"
                  value={lessonTitle}
                  onChange={(e) => setLessonTitle(e.target.value)}
                  placeholder="Lesson title"
                  className="mb-2 w-full rounded-md border px-3 py-2 text-sm focus:border-brand focus:outline-none"
                />
                <textarea
                  value={lessonContent}
                  onChange={(e) => setLessonContent(e.target.value)}
                  placeholder="Lesson content (rich text supported)"
                  rows={3}
                  className="mb-2 w-full rounded-md border px-3 py-2 text-sm focus:border-brand focus:outline-none"
                />
                <button
                  onClick={addLesson}
                  disabled={addingLesson || !lessonTitle.trim()}
                  className="rounded-md bg-brand px-4 py-1.5 text-xs font-medium text-white hover:bg-orange-600 disabled:opacity-50"
                >
                  {addingLesson ? "Adding..." : "+ Add Lesson"}
                </button>
              </div>

              {/* Lesson list */}
              <div className="space-y-2">
                {lessons.map((lesson, i) => (
                  <div
                    key={lesson.id}
                    className={`rounded-lg border p-4 shadow-sm cursor-pointer transition-colors ${
                      selectedLesson === lesson.id
                        ? "border-brand bg-orange-50"
                        : "bg-white hover:border-gray-300"
                    }`}
                    onClick={() => loadQuizzes(lesson.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="text-xs font-bold text-gray-400">#{i + 1}</span>
                        <h4 className="ml-2 inline font-medium text-sm">{lesson.title}</h4>
                      </div>
                      <button
                        onClick={(e) => { e.stopPropagation(); handleDeleteLesson(lesson.id); }}
                        className="text-xs text-red-500 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </div>
                    {lesson.content && (
                      <p className="mt-1 text-xs text-gray-500 line-clamp-2">{lesson.content}</p>
                    )}
                    <div className="mt-2 flex gap-3 text-xs text-gray-400">
                      {lesson.video_url && <span>🎬 Video</span>}
                      <span>{lesson.duration_minutes ? `${lesson.duration_minutes} min` : ""}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quizzes panel */}
            <div>
              <h3 className="mb-3 text-lg font-semibold">
                {selectedLesson ? "Quizzes" : "Select a lesson to view quizzes"}
              </h3>

              {selectedLesson && (
                <>
                  <button
                    onClick={() => generateQuiz(selectedLesson)}
                    className="mb-3 rounded-md bg-green-600 px-4 py-1.5 text-xs font-medium text-white hover:bg-green-700"
                  >
                    🤖 AI Generate Quiz
                  </button>

                  {quizzes.length === 0 ? (
                    <div className="py-8 text-center text-sm text-gray-400">
                      No quizzes for this lesson. Generate one with AI!
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {quizzes.map((quiz) => (
                        <div key={quiz.id} className="rounded-lg border bg-white p-4 shadow-sm">
                          <div className="flex items-center justify-between">
                            <h4 className="font-medium text-sm">{quiz.title}</h4>
                            <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                              quiz.is_published ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"
                            }`}>
                              {quiz.is_published ? "Published" : "Draft"}
                            </span>
                          </div>
                          <div className="mt-2 text-xs text-gray-500">
                            {quiz.question_count || 0} questions · Pass: {quiz.passing_score}%
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </>
      )}

      {/* Tutor bot */}
      <TutorBot learnerId="builder-user" courseId={courseId} />
    </main>
  );
}
