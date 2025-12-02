import Link from "next/link";
import { Bug } from "lucide-react";
import LoginWithGitHub from "@/components/LoginWithGitHub";

export default function Navbar() {
  return (
    <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2">
            <Bug className="w-6 h-6 text-blue-600" />
            <span className="font-bold text-xl">Bug Ghost AI</span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link
              href="/"
              className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Home
            </Link>
            <Link
              href="/sessions"
              className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Sessions
            </Link>
            <Link
              href="/teams"
              className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
            >
              Teams
            </Link>
            <Link
              href="/sandbox"
              className="text-gray-700 dark:text-gray-300 hover:text-green-600 dark:hover:text-green-400 transition-colors"
            >
              Sandbox
            </Link>
            <LoginWithGitHub />
          </div>
        </div>
      </div>
    </nav>
  );
}
