"use client";

import { useState } from "react";
import ErrorForm from "@/components/ErrorForm";
import SessionResult from "@/components/SessionResult";
import { DebugSessionResponse } from "@/lib/types";

export default function Home() {
  const [result, setResult] = useState<DebugSessionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmitSuccess = (session: DebugSessionResponse) => {
    setResult(session);
    setIsLoading(false);
  };

  const handleNewSession = () => {
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
      <div className="container mx-auto px-4 py-12">
        {!result ? (
          <>
            {/* Hero Section */}
            <div className="text-center mb-12">
              <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Bug Ghost AI
              </h1>
              <p className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 mb-2">
                The AI Debug Replayer
              </p>
              <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Paste an error. Get reproducible code, tests, and a fix — powered by AI.
              </p>
            </div>

            {/* Features */}
            <div className="grid md:grid-cols-3 gap-6 mb-12 max-w-4xl mx-auto">
              <div className="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg">
                <div className="text-3xl mb-3">🔍</div>
                <h3 className="font-semibold text-lg mb-2">Analyze</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  AI analyzes your error and code context
                </p>
              </div>
              <div className="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg">
                <div className="text-3xl mb-3">⚡</div>
                <h3 className="font-semibold text-lg mb-2">Reproduce</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Generate minimal reproduction code & tests
                </p>
              </div>
              <div className="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg">
                <div className="text-3xl mb-3">🎯</div>
                <h3 className="font-semibold text-lg mb-2">Fix</h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Get root cause analysis and fix suggestions
                </p>
              </div>
            </div>

            {/* Form */}
            <div className="max-w-4xl mx-auto">
              <ErrorForm
                onSubmitSuccess={handleSubmitSuccess}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
              />
            </div>
            <div className="flex gap-4 items-center">
              <a
                href="/sandbox"
                className="border px-4 py-2 rounded hover:bg-gray-100"
              >
                Try Sandbox
              </a>
              <a
                href={`http://localhost:8000/api/auth/github/login`}
                className="border px-4 py-2 rounded hover:bg-gray-100"
              >
                Login with GitHub
              </a>
            </div>
          </>
        ) : (
          <SessionResult session={result} onNewSession={handleNewSession} />
        )}
      </div>
    </div>
  );
}
