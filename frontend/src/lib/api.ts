export interface Training {
  id: string;
  name: string;
  format: string;
  enrollment_link: string;
  completion_rate: number;
  average_score: number;
  certification_expiry: string;
  created_at: string;
}

export interface LearnerProgress {
  learner_name: string;
  status: string;
  score: number;
}

export async function api<T>(
  path: string,
  init?: RequestInit
): Promise<T> {
  const res = await fetch(`/api/v1${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}
