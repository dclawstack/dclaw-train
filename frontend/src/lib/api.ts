const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

// ── Generic typed fetch ──
export const api = fetchJson;

// ── Types ──

export interface Course {
  id: string;
  title: string;
  description?: string;
  format: string;
  thumbnail_url?: string;
  category?: string;
  tags?: string;
  is_published: boolean;
  created_at: string;
  updated_at: string;
  lesson_count?: number;
  enrollment_count?: number;
}

export interface Lesson {
  id: string;
  course_id: string;
  title: string;
  description?: string;
  content?: string;
  video_url?: string;
  video_transcript?: string;
  video_summary?: string;
  video_chapters?: string;
  duration_minutes?: number;
  order: number;
  is_published: boolean;
  created_at: string;
  updated_at: string;
}

export interface LessonResource {
  id: string;
  lesson_id: string;
  title: string;
  resource_type: string;
  url: string;
  created_at: string;
}

export interface Quiz {
  id: string;
  lesson_id: string;
  title: string;
  description?: string;
  passing_score: number;
  time_limit_minutes?: number;
  is_published: boolean;
  question_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  quiz_id: string;
  question_type: string;
  difficulty: string;
  text: string;
  options?: string;
  correct_answer: string;
  explanation?: string;
  points: number;
  order: number;
  created_at: string;
}

export interface QuizAttempt {
  id: string;
  quiz_id: string;
  learner_id: string;
  score: number;
  total_points: number;
  passed: boolean;
  started_at: string;
  completed_at?: string;
}

export interface Enrollment {
  id: string;
  course_id: string;
  learner_id: string;
  status: string;
  progress_percentage: number;
  enrolled_at: string;
  completed_at?: string;
  last_accessed_at: string;
}

export interface LearnerProgress {
  id: string;
  enrollment_id: string;
  lesson_id: string;
  status: string;
  time_spent_seconds: number;
  score?: number;
  completed_at?: string;
  last_accessed_at: string;
}

export interface TutorConversation {
  reply: string;
  conversation_id: string;
  suggested_questions?: string[];
}

export interface AnalyticsOverview {
  total_courses: number;
  total_enrollments: number;
  total_completions: number;
  average_completion_rate: number;
  average_score: number;
  at_risk_learners: number;
}

export interface LearnerAnalytics {
  learner_id: string;
  courses_enrolled: number;
  courses_completed: number;
  total_time_spent_hours: number;
  average_score: number;
  engagement_score: number;
  at_risk: boolean;
}

export interface CourseAnalytics {
  course_id: string;
  title: string;
  enrollment_count: number;
  completion_count: number;
  completion_rate: number;
  average_score: number;
  average_time_to_complete_days: number;
}

export interface LearningPathCourse {
  course_id: string;
  title: string;
  reason: string;
  priority: number;
}

export interface LearningPath {
  id: string;
  learner_id: string;
  recommended_courses: LearningPathCourse[];
  skills_gap?: Record<string, number>;
  reasoning?: string;
  generated_at: string;
}

export interface LiveSession {
  id: string;
  course_id?: string;
  title: string;
  description?: string;
  session_url?: string;
  status: string;
  scheduled_at: string;
  duration_minutes: number;
  recording_url?: string;
  transcript?: string;
  max_participants?: number;
  created_at?: string;
}

export interface Certificate {
  id: string;
  course_id: string;
  learner_id: string;
  certificate_url?: string;
  issued_at: string;
  expires_at?: string;
}

export interface Badge {
  id: string;
  learner_id: string;
  badge_type: string;
  course_id?: string;
  title: string;
  description?: string;
  icon_url?: string;
  earned_at: string;
}

export interface SkillAssessment {
  id: string;
  learner_id: string;
  assessment_type: string;
  course_id?: string;
  skills_data: string;
  overall_score: number;
  completed_at: string;
}

export interface SkillsGap {
  learner_id: string;
  pre_assessment?: Record<string, number>;
  post_assessment?: Record<string, number>;
  improvements?: Record<string, number>;
  gaps?: Record<string, number>;
}

export interface ForumTopic {
  id: string;
  course_id: string;
  learner_id: string;
  title: string;
  content: string;
  is_pinned: boolean;
  reply_count?: number;
  created_at: string;
  updated_at: string;
}

export interface ForumReply {
  id: string;
  topic_id: string;
  learner_id: string;
  content: string;
  is_ai_response: boolean;
  created_at: string;
}

export interface QuizGeneration {
  quiz_id: string;
  questions: Question[];
}

export interface VideoSummary {
  lesson_id: string;
  summary: string;
  chapters: { title: string; timestamp: string; description?: string }[];
  transcript?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// ── API Functions ──

// Courses
export const coursesApi = {
  list: (params?: { page?: number; page_size?: number; published_only?: boolean; search?: string }) => {
    const qs = new URLSearchParams();
    if (params?.page) qs.set("page", String(params.page));
    if (params?.page_size) qs.set("page_size", String(params.page_size));
    if (params?.published_only) qs.set("published_only", "true");
    if (params?.search) qs.set("search", params.search);
    return fetchJson<PaginatedResponse<Course>>(`/api/v1/courses?${qs}`);
  },
  get: (id: string) => fetchJson<Course>(`/api/v1/courses/${id}`),
  create: (data: Partial<Course>) => fetchJson<Course>("/api/v1/courses", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: Partial<Course>) => fetchJson<Course>(`/api/v1/courses/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  delete: (id: string) => fetchJson<void>(`/api/v1/courses/${id}`, { method: "DELETE" }),
  structure: (id: string) => fetchJson<any>(`/api/v1/courses/${id}/structure`),
};

// Lessons
export const lessonsApi = {
  listByCourse: (courseId: string) => fetchJson<Lesson[]>(`/api/v1/courses/${courseId}/lessons`),
  get: (id: string) => fetchJson<Lesson>(`/api/v1/lessons/${id}`),
  create: (data: Partial<Lesson>) => fetchJson<Lesson>("/api/v1/lessons", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: Partial<Lesson>) => fetchJson<Lesson>(`/api/v1/lessons/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  delete: (id: string) => fetchJson<void>(`/api/v1/lessons/${id}`, { method: "DELETE" }),
  reorder: (courseId: string, lessonIds: string[]) => fetchJson<void>(`/api/v1/courses/${courseId}/lessons/reorder`, { method: "POST", body: JSON.stringify({ lesson_ids: lessonIds }) }),
  resources: (lessonId: string) => fetchJson<LessonResource[]>(`/api/v1/lessons/${lessonId}/resources`),
};

// Quizzes
export const quizzesApi = {
  listByLesson: (lessonId: string) => fetchJson<Quiz[]>(`/api/v1/lessons/${lessonId}/quizzes`),
  update: (id: string, data: Partial<Quiz>) => fetchJson<Quiz>(`/api/v1/quizzes/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  questions: (quizId: string) => fetchJson<Question[]>(`/api/v1/quizzes/${quizId}/questions`),
  generate: (lessonId: string, numQuestions?: number, difficulty?: string) =>
    fetchJson<QuizGeneration>("/api/v1/ai/generate-quiz", {
      method: "POST",
      body: JSON.stringify({ lesson_id: lessonId, num_questions: numQuestions || 5, difficulty: difficulty || "medium" }),
    }),
  submitAttempt: (quizId: string, learnerId: string, answers: { question_id: string; answer: string }[]) =>
    fetchJson<QuizAttempt>("/api/v1/quiz-attempts", {
      method: "POST",
      body: JSON.stringify({ quiz_id: quizId, learner_id: learnerId, answers }),
    }),
};

// Enrollments
export const enrollmentsApi = {
  enroll: (courseId: string, learnerId: string) => fetchJson<Enrollment>("/api/v1/enrollments", { method: "POST", body: JSON.stringify({ course_id: courseId, learner_id: learnerId }) }),
  listByCourse: (courseId: string) => fetchJson<Enrollment[]>(`/api/v1/courses/${courseId}/enrollments`),
  listByLearner: (learnerId: string) => fetchJson<Enrollment[]>(`/api/v1/learners/${learnerId}/enrollments`),
};

// Progress
export const progressApi = {
  record: (enrollmentId: string, lessonId: string, status: string, timeSpentSeconds: number, score?: number) =>
    fetchJson<LearnerProgress>("/api/v1/progress", {
      method: "POST",
      body: JSON.stringify({ enrollment_id: enrollmentId, lesson_id: lessonId, status, time_spent_seconds: timeSpentSeconds, score }),
    }),
  listByEnrollment: (enrollmentId: string) => fetchJson<LearnerProgress[]>(`/api/v1/enrollments/${enrollmentId}/progress`),
};

// AI Tutor
export const tutorApi = {
  ask: (learnerId: string, message: string, lessonId?: string, courseId?: string) =>
    fetchJson<TutorConversation>("/api/v1/ai/tutor", {
      method: "POST",
      body: JSON.stringify({ learner_id: learnerId, message, lesson_id: lessonId, course_id: courseId }),
    }),
};

// Analytics
export const analyticsApi = {
  overview: () => fetchJson<AnalyticsOverview>("/api/v1/analytics/overview"),
  learner: (learnerId: string) => fetchJson<LearnerAnalytics>(`/api/v1/analytics/learners/${learnerId}`),
  course: (courseId: string) => fetchJson<CourseAnalytics>(`/api/v1/analytics/courses/${courseId}`),
  atRisk: () => fetchJson<{ at_risk_learner_ids: string[]; count: number }>("/api/v1/analytics/at-risk"),
};

// Learning Paths
export const learningPathApi = {
  generate: (learnerId: string, role?: string, careerGoals?: string[]) =>
    fetchJson<LearningPath>("/api/v1/learning-paths", {
      method: "POST",
      body: JSON.stringify({ learner_id: learnerId, role, career_goals: careerGoals }),
    }),
  get: (learnerId: string) => fetchJson<LearningPath>(`/api/v1/learners/${learnerId}/learning-path`),
};

// Live Sessions
export const liveSessionApi = {
  listByCourse: (courseId: string) => fetchJson<LiveSession[]>(`/api/v1/courses/${courseId}/sessions`),
  upcoming: (limit?: number) => fetchJson<LiveSession[]>(`/api/v1/live-sessions/upcoming?limit=${limit || 10}`),
  create: (data: Partial<LiveSession>) => fetchJson<LiveSession>("/api/v1/live-sessions", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: Partial<LiveSession>) => fetchJson<LiveSession>(`/api/v1/live-sessions/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
};

// Certificates & Badges
export const certApi = {
  generate: (courseId: string, learnerId: string, learnerName: string) =>
    fetchJson<Certificate>("/api/v1/certificates/generate", {
      method: "POST",
      body: JSON.stringify({ course_id: courseId, learner_id: learnerId, learner_name: learnerName }),
    }),
  list: (learnerId: string) => fetchJson<Certificate[]>(`/api/v1/learners/${learnerId}/certificates`),
};

export const badgeApi = {
  award: (learnerId: string, badgeType: string, title: string, description?: string) =>
    fetchJson<Badge>("/api/v1/badges", {
      method: "POST",
      body: JSON.stringify({ learner_id: learnerId, badge_type: badgeType, title, description }),
    }),
  list: (learnerId: string) => fetchJson<Badge[]>(`/api/v1/learners/${learnerId}/badges`),
};

// Skills
export const skillsApi = {
  submit: (learnerId: string, assessmentType: string, skillsData: Record<string, number>) =>
    fetchJson<SkillAssessment>("/api/v1/skills/assessment", {
      method: "POST",
      body: JSON.stringify({ learner_id: learnerId, assessment_type: assessmentType, skills_data: skillsData }),
    }),
  gap: (learnerId: string, courseId?: string) =>
    fetchJson<SkillsGap>(`/api/v1/learners/${learnerId}/skills/gap${courseId ? `?course_id=${courseId}` : ""}`),
};

// Forum
export const forumApi = {
  listTopics: (courseId: string) => fetchJson<ForumTopic[]>(`/api/v1/courses/${courseId}/forum/topics`),
  getTopic: (topicId: string) => fetchJson<any>(`/api/v1/forum/topics/${topicId}`),
  createTopic: (courseId: string, learnerId: string, title: string, content: string) =>
    fetchJson<ForumTopic>("/api/v1/forum/topics", {
      method: "POST",
      body: JSON.stringify({ course_id: courseId, learner_id: learnerId, title, content }),
    }),
  reply: (topicId: string, learnerId: string, content: string) =>
    fetchJson<ForumReply>("/api/v1/forum/replies", {
      method: "POST",
      body: JSON.stringify({ topic_id: topicId, learner_id: learnerId, content }),
    }),
};

// AI Video
export const videoApi = {
  summarize: (lessonId: string) =>
    fetchJson<VideoSummary>("/api/v1/ai/summarize-video", {
      method: "POST",
      body: JSON.stringify({ lesson_id: lessonId }),
    }),
};

// SCORM
export const scormApi = {
  import: (title: string, version?: string) =>
    fetchJson<any>("/api/v1/scorm/import", { method: "POST", body: JSON.stringify({ title, version: version || "1.2" }) }),
  export: (courseId: string) => fetchJson<any>(`/api/v1/scorm/export/${courseId}`, { method: "POST" }),
};

export { ApiError };
