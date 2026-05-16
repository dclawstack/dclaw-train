import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "DClaw Train — AI-Powered LMS",
  description: "Employee training & certification tracking. AI tutor, course builder, quiz generator, analytics, and more.",
  keywords: ["LMS", "AI training", "employee learning", "course builder", "quiz generator"],
  openGraph: {
    title: "DClaw Train — AI-Powered LMS",
    description: "Train your team at lightspeed. AI tutor, course builder, quiz generator, analytics, and more.",
    type: "website",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
