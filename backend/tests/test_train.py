import pytest
from uuid import uuid4


# ────────────────────────────────────────────────────────────
#  Health
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ────────────────────────────────────────────────────────────
#  Courses CRUD
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_course(client):
    payload = {
        "title": "Python Basics",
        "description": "Learn Python fundamentals",
        "format": "Video",
        "category": "Programming",
        "tags": "python,beginner",
    }
    response = await client.post("/api/v1/courses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Basics"
    assert data["format"] == "Video"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_list_courses(client):
    # Create a few courses
    for i in range(3):
        await client.post("/api/v1/courses", json={
            "title": f"Course {i}",
            "format": "Video",
        })

    response = await client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3
    assert len(data["items"]) >= 3


@pytest.mark.asyncio
async def test_get_course(client):
    # Create
    create_resp = await client.post("/api/v1/courses", json={
        "title": "Test Course", "format": "Quiz",
    })
    course_id = create_resp.json()["id"]

    # Get
    response = await client.get(f"/api/v1/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Course"


@pytest.mark.asyncio
async def test_update_course(client):
    create_resp = await client.post("/api/v1/courses", json={
        "title": "Old Title", "format": "Video",
    })
    course_id = create_resp.json()["id"]

    response = await client.patch(f"/api/v1/courses/{course_id}", json={
        "title": "New Title", "is_published": True,
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["is_published"] is True


@pytest.mark.asyncio
async def test_delete_course(client):
    create_resp = await client.post("/api/v1/courses", json={
        "title": "To Delete", "format": "Video",
    })
    course_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/courses/{course_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/courses/{course_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_search_courses(client):
    await client.post("/api/v1/courses", json={
        "title": "Advanced Machine Learning", "format": "Video",
    })
    await client.post("/api/v1/courses", json={
        "title": "Basic Cooking", "format": "Workshop",
    })

    response = await client.get("/api/v1/courses?search=Machine")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any("Machine" in c["title"] for c in data["items"])


# ────────────────────────────────────────────────────────────
#  Lessons
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_lesson(client):
    # Create course first
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Course with Lessons", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    payload = {
        "course_id": course_id,
        "title": "Lesson 1: Introduction",
        "content": "Welcome to the course",
        "order": 0,
    }
    response = await client.post("/api/v1/lessons", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Lesson 1: Introduction"
    assert data["course_id"] == course_id


@pytest.mark.asyncio
async def test_list_lessons_by_course(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Lesson List Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    for i in range(3):
        await client.post("/api/v1/lessons", json={
            "course_id": course_id,
            "title": f"Lesson {i}",
            "order": i,
        })

    response = await client.get(f"/api/v1/courses/{course_id}/lessons")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_reorder_lessons(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Reorder Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    ids = []
    for i in range(3):
        resp = await client.post("/api/v1/lessons", json={
            "course_id": course_id,
            "title": f"Lesson {i}",
            "order": i,
        })
        ids.append(resp.json()["id"])

    # Reverse order
    reversed_ids = list(reversed(ids))
    resp = await client.post(f"/api/v1/courses/{course_id}/lessons/reorder", json={
        "lesson_ids": reversed_ids,
    })
    assert resp.status_code == 200


# ────────────────────────────────────────────────────────────
#  Lesson Resources
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_add_resource(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Resource Course", "format": "Document",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Lesson with files", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]

    response = await client.post("/api/v1/resources", json={
        "lesson_id": lesson_id,
        "title": "Slides PDF",
        "resource_type": "pdf",
        "url": "https://example.com/slides.pdf",
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Slides PDF"
    assert response.json()["resource_type"] == "pdf"


# ────────────────────────────────────────────────────────────
#  Quizzes & Questions
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_quiz(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Quiz Course", "format": "Quiz",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Quiz Lesson", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]

    response = await client.post("/api/v1/quizzes", json={
        "lesson_id": lesson_id,
        "title": "Test Quiz",
        "passing_score": 70.0,
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Quiz"


@pytest.mark.asyncio
async def test_add_question(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Question Course", "format": "Quiz",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Question Lesson", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]
    quiz_resp = await client.post("/api/v1/quizzes", json={
        "lesson_id": lesson_id, "title": "Question Quiz",
    })
    quiz_id = quiz_resp.json()["id"]

    response = await client.post("/api/v1/questions", json={
        "quiz_id": quiz_id,
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "text": "What is 2+2?",
        "options": '["3","4","5","6"]',
        "correct_answer": "4",
        "points": 1.0,
        "order": 0,
    })
    assert response.status_code == 201
    assert response.json()["text"] == "What is 2+2?"


@pytest.mark.asyncio
async def test_list_questions_no_answers(client):
    """Questions should not expose correct_answer in list view."""
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Safe Course", "format": "Quiz",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Safe Lesson", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]
    quiz_resp = await client.post("/api/v1/quizzes", json={
        "lesson_id": lesson_id, "title": "Safe Quiz",
    })
    quiz_id = quiz_resp.json()["id"]

    await client.post("/api/v1/questions", json={
        "quiz_id": quiz_id, "question_type": "multiple_choice",
        "difficulty": "medium", "text": "Secret question?",
        "options": '["A","B","C"]', "correct_answer": "B",
        "points": 1.0, "order": 0,
    })

    response = await client.get(f"/api/v1/quizzes/{quiz_id}/questions")
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) > 0
    assert questions[0]["correct_answer"] == "[hidden]"


# ────────────────────────────────────────────────────────────
#  Quiz Attempts
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_submit_quiz_attempt(client):
    # Setup
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Attempt Course", "format": "Quiz",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Attempt Lesson", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]
    quiz_resp = await client.post("/api/v1/quizzes", json={
        "lesson_id": lesson_id, "title": "Attempt Quiz",
    })
    quiz_id = quiz_resp.json()["id"]

    q1 = await client.post("/api/v1/questions", json={
        "quiz_id": quiz_id, "question_type": "multiple_choice",
        "difficulty": "easy", "text": "Q1?",
        "options": '["X","Y"]', "correct_answer": "X",
        "points": 1.0, "order": 0,
    })
    q1_id = q1.json()["id"]

    # Submit attempt
    response = await client.post("/api/v1/quiz-attempts", json={
        "quiz_id": quiz_id,
        "learner_id": "learner-1",
        "answers": [{"question_id": q1_id, "answer": "X"}],
    })
    assert response.status_code == 201
    data = response.json()
    assert data["passed"] is True
    assert data["score"] == 1.0


# ────────────────────────────────────────────────────────────
#  Enrollments
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_enroll_learner(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Enrollment Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    response = await client.post("/api/v1/enrollments", json={
        "course_id": course_id,
        "learner_id": "learner-42",
    })
    assert response.status_code == 201
    assert response.json()["learner_id"] == "learner-42"
    assert response.json()["status"] == "Enrolled"


@pytest.mark.asyncio
async def test_duplicate_enrollment_is_idempotent(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Idempotent Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    r1 = await client.post("/api/v1/enrollments", json={
        "course_id": course_id, "learner_id": "learner-dup",
    })
    r2 = await client.post("/api/v1/enrollments", json={
        "course_id": course_id, "learner_id": "learner-dup",
    })
    assert r1.json()["id"] == r2.json()["id"]


# ────────────────────────────────────────────────────────────
#  Learner Progress
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_record_learner_progress(client):
    # Setup course → enrollment → progress
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Progress Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Progress Lesson", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]
    enrollment_resp = await client.post("/api/v1/enrollments", json={
        "course_id": course_id, "learner_id": "progress-learner",
    })
    enrollment_id = enrollment_resp.json()["id"]

    response = await client.post("/api/v1/progress", json={
        "enrollment_id": enrollment_id,
        "lesson_id": lesson_id,
        "status": "In Progress",
        "time_spent_seconds": 300,
        "score": 85.0,
    })
    assert response.status_code == 201
    assert response.json()["status"] == "In Progress"
    assert response.json()["time_spent_seconds"] == 300


@pytest.mark.asyncio
async def test_progress_accumulates_time(client):
    """Repeated progress updates should accumulate time."""
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Accum Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "Accum Lesson", "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]
    enrollment_resp = await client.post("/api/v1/enrollments", json={
        "course_id": course_id, "learner_id": "accum-learner",
    })
    enrollment_id = enrollment_resp.json()["id"]

    await client.post("/api/v1/progress", json={
        "enrollment_id": enrollment_id, "lesson_id": lesson_id,
        "status": "In Progress", "time_spent_seconds": 100,
    })
    r2 = await client.post("/api/v1/progress", json={
        "enrollment_id": enrollment_id, "lesson_id": lesson_id,
        "status": "In Progress", "time_spent_seconds": 150,
    })
    assert r2.json()["time_spent_seconds"] == 250  # 100 + 150


# ────────────────────────────────────────────────────────────
#  AI Tutor
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_ai_tutor_response(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Tutor Course", "format": "Video",
        "description": "A course for testing the AI tutor",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id,
        "title": "Tutor Lesson",
        "content": "This lesson covers Python programming basics including variables, loops, and functions.",
        "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]

    response = await client.post("/api/v1/ai/tutor", json={
        "learner_id": "learner-tutor",
        "lesson_id": lesson_id,
        "message": "Can you explain variables?",
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "conversation_id" in data
    assert len(data.get("suggested_questions", [])) > 0


@pytest.mark.asyncio
async def test_ai_tutor_no_direct_answers(client):
    """Tutor should not give direct answers."""
    course_resp = await client.post("/api/v1/courses", json={
        "title": "No Cheat Course", "format": "Quiz",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id, "title": "No Cheat Lesson",
        "content": "The answer to everything is 42.",
        "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]

    response = await client.post("/api/v1/ai/tutor", json={
        "learner_id": "cheater-1",
        "lesson_id": lesson_id,
        "message": "Just tell me the answer",
    })
    data = response.json()
    assert "I'd love to help you figure this out yourself" in data["reply"]


# ────────────────────────────────────────────────────────────
#  AI Quiz Generation
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_ai_generate_quiz(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Gen Quiz Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id,
        "title": "Rich Content Lesson",
        "content": "Python is a high-level programming language. "
                   "It supports multiple paradigms including object-oriented, "
                   "functional, and procedural programming. Python's simple syntax "
                   "makes it ideal for beginners. Variables in Python are dynamically typed. "
                   "Functions are defined using the def keyword. Loops include for and while.",
        "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]

    response = await client.post("/api/v1/ai/generate-quiz", json={
        "lesson_id": lesson_id,
        "num_questions": 3,
        "difficulty": "medium",
        "question_types": ["multiple_choice", "true_false"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "quiz_id" in data
    assert len(data["questions"]) > 0


# ────────────────────────────────────────────────────────────
#  Analytics
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_analytics_overview(client):
    response = await client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_courses" in data
    assert "total_enrollments" in data


@pytest.mark.asyncio
async def test_learner_analytics(client):
    # Enroll a learner
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Analytics Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]
    await client.post("/api/v1/enrollments", json={
        "course_id": course_id, "learner_id": "analytics-learner",
    })

    response = await client.get("/api/v1/analytics/learners/analytics-learner")
    assert response.status_code == 200
    data = response.json()
    assert data["courses_enrolled"] >= 1


# ────────────────────────────────────────────────────────────
#  Learning Paths
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_generate_learning_path(client):
    # Create some published courses
    for i in range(3):
        await client.post("/api/v1/courses", json={
            "title": f"Path Course {i}",
            "format": "Video",
            "category": "Software Engineering",
            "is_published": True,
        })

    response = await client.post("/api/v1/learning-paths", json={
        "learner_id": "path-learner",
        "role": "Software Engineer",
        "career_goals": ["Become Senior Developer"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "recommended_courses" in data


# ────────────────────────────────────────────────────────────
#  Live Sessions
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_schedule_live_session(client):
    from datetime import datetime, timedelta
    future_time = (datetime.utcnow() + timedelta(days=7)).isoformat()

    response = await client.post("/api/v1/live-sessions", json={
        "title": "Weekly Q&A",
        "description": "Ask anything about the course",
        "scheduled_at": future_time,
        "duration_minutes": 60,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Weekly Q&A"


@pytest.mark.asyncio
async def test_list_upcoming_sessions(client):
    response = await client.get("/api/v1/live-sessions/upcoming?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ────────────────────────────────────────────────────────────
#  Certificates & Badges
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_generate_certificate_requires_completion(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Cert Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    # Learner enrolled but not completed
    await client.post("/api/v1/enrollments", json={
        "course_id": course_id, "learner_id": "cert-learner",
    })

    response = await client.post("/api/v1/certificates/generate", json={
        "course_id": course_id,
        "learner_id": "cert-learner",
        "learner_name": "Cert Learner",
    })
    assert response.status_code == 400  # Not yet completed


@pytest.mark.asyncio
async def test_award_badge(client):
    response = await client.post("/api/v1/badges", json={
        "learner_id": "badge-learner",
        "badge_type": "completion",
        "title": "First Course Complete",
        "description": "Completed your first course!",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["learner_id"] == "badge-learner"
    assert data["badge_type"] == "completion"


# ────────────────────────────────────────────────────────────
#  Skills Assessment
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_submit_skills_assessment(client):
    response = await client.post("/api/v1/skills/assessment", json={
        "learner_id": "skills-learner",
        "assessment_type": "pre",
        "skills_data": {"python": 45, "sql": 60, "testing": 30},
    })
    assert response.status_code == 201
    data = response.json()
    assert data["assessment_type"] == "pre"


@pytest.mark.asyncio
async def test_skills_gap_analysis(client):
    # Submit pre-assessment
    await client.post("/api/v1/skills/assessment", json={
        "learner_id": "gap-learner",
        "assessment_type": "pre",
        "skills_data": {"python": 40, "sql": 50},
    })
    # Submit post-assessment
    await client.post("/api/v1/skills/assessment", json={
        "learner_id": "gap-learner",
        "assessment_type": "post",
        "skills_data": {"python": 75, "sql": 65},
    })

    response = await client.get("/api/v1/learners/gap-learner/skills/gap")
    assert response.status_code == 200
    data = response.json()
    assert data["pre_assessment"] is not None
    assert data["post_assessment"] is not None
    assert data["improvements"] is not None
    assert data["gaps"] is not None


# ────────────────────────────────────────────────────────────
#  Discussion Forums
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_forum_topic(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Forum Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]

    response = await client.post("/api/v1/forum/topics", json={
        "course_id": course_id,
        "learner_id": "forum-learner",
        "title": "How do I use list comprehensions?",
        "content": "I'm struggling with list comprehensions in Python. Can someone explain?",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "How do I use list comprehensions?"


@pytest.mark.asyncio
async def test_reply_to_topic(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Reply Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]
    topic_resp = await client.post("/api/v1/forum/topics", json={
        "course_id": course_id,
        "learner_id": "question-asker",
        "title": "Need help with decorators",
        "content": "How do Python decorators work?",
    })
    topic_id = topic_resp.json()["id"]

    response = await client.post("/api/v1/forum/replies", json={
        "topic_id": topic_id,
        "learner_id": "helper-learner",
        "content": "Decorators are functions that modify other functions.",
    })
    assert response.status_code == 201


# ────────────────────────────────────────────────────────────
#  SCORM / xAPI
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_import_scorm_package(client):
    response = await client.post("/api/v1/scorm/import", json={
        "title": "SCORM Compliance Training",
        "version": "1.2",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "SCORM Compliance Training"


@pytest.mark.asyncio
async def test_store_xapi_statement(client):
    response = await client.post("/api/v1/xapi/statements", json={
        "learner_id": "xapi-learner",
        "verb": "completed",
        "object_id": "http://example.com/courses/python-basics",
        "result": {"score": 95, "success": True},
    })
    assert response.status_code == 200
    data = response.json()
    assert data["verb"] == "completed"


# ────────────────────────────────────────────────────────────
#  Video Summarization
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_summarize_video(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Video Course", "format": "Video",
    })
    course_id = course_resp.json()["id"]
    lesson_resp = await client.post("/api/v1/lessons", json={
        "course_id": course_id,
        "title": "Video Lesson",
        "description": "A comprehensive lesson about data structures",
        "content": "Data structures are fundamental to computer science.",
        "video_url": "https://example.com/video.mp4",
        "order": 0,
    })
    lesson_id = lesson_resp.json()["id"]

    response = await client.post("/api/v1/ai/summarize-video", json={
        "lesson_id": lesson_id,
    })
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "chapters" in data
    assert len(data["chapters"]) > 0


# ────────────────────────────────────────────────────────────
#  Course Structure (Builder)
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_course_structure(client):
    course_resp = await client.post("/api/v1/courses", json={
        "title": "Structured Course", "format": "Video",
        "description": "A well-structured course",
    })
    course_id = course_resp.json()["id"]

    for i in range(2):
        await client.post("/api/v1/lessons", json={
            "course_id": course_id,
            "title": f"Module {i+1}",
            "content": f"Content for module {i+1}",
            "order": i,
        })

    response = await client.get(f"/api/v1/courses/{course_id}/structure")
    assert response.status_code == 200
    data = response.json()
    assert len(data["lessons"]) == 2


# ────────────────────────────────────────────────────────────
#  Pagination
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_course_pagination(client):
    for i in range(25):
        await client.post("/api/v1/courses", json={
            "title": f"Paginated Course {i}", "format": "Video",
        })

    response = await client.get("/api/v1/courses?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 10
    assert data["total"] >= 25
    assert data["pages"] >= 3

    # Page 2
    response2 = await client.get("/api/v1/courses?page=2&page_size=10")
    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2["items"]) <= 10


# ────────────────────────────────────────────────────────────
#  Error Handling
# ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_404_on_nonexistent_course(client):
    response = await client.get(f"/api/v1/courses/{uuid4()}")
    assert response.status_code == 404
