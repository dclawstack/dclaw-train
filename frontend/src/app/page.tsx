import Link from "next/link";
import { GraduationCap } from "lucide-react";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-white px-4">
      <GraduationCap className="mb-6 h-16 w-16 text-brand" />
      <h1 className="mb-4 text-5xl font-bold" style={{ color: "#F97316" }}>
        DClaw Train
      </h1>
      <p className="mb-8 text-lg text-gray-600">
        Employee training & certification tracking
      </p>
      <Link
        href="/dashboard"
        className="rounded-lg bg-brand px-6 py-3 font-semibold text-white transition hover:bg-orange-600"
      >
        Go to Dashboard
      </Link>
    </main>
  );
}
