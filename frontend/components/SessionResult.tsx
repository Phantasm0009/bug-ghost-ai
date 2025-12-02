"use client";

import { useState } from "react";
import { DebugSessionResponse } from "@/lib/types";
import CodeBlock from "./CodeBlock";
import { AlertCircle, CheckCircle2, Clock, ArrowLeft } from "lucide-react";
import { format } from "date-fns";

interface SessionResultProps {
  session: DebugSessionResponse;
  onNewSession: () => void;
}

type TabType = "repro" | "test" | "explanation" | "fix" | "context";

export default function SessionResult({
  session,
  onNewSession,
}: SessionResultProps) {
  const [activeTab, setActiveTab] = useState<TabType>("explanation");

  const tabs: { id: TabType; label: string }[] = [
    { id: "explanation", label: "Root Cause" },
    { id: "fix", label: "Fix Suggestion" },
    { id: "repro", label: "Repro Code" },
    { id: "test", label: "Test Code" },
    { id: "context", label: "Original Error" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={onNewSession}
          className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>New Session</span>
        </button>

        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Analysis Complete</h2>
            {session.status === "completed" && (
              <span className="flex items-center space-x-2 text-green-600">
                <CheckCircle2 className="w-5 h-5" />
                <span>Success</span>
              </span>
            )}
            {session.status === "processing" && (
              <span className="flex items-center space-x-2 text-yellow-600">
                <Clock className="w-5 h-5" />
                <span>Processing</span>
              </span>
            )}
            {session.status === "failed" && (
              <span className="flex items-center space-x-2 text-red-600">
                <AlertCircle className="w-5 h-5" />
                <span>Failed</span>
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500 dark:text-gray-400">Language</span>
              <p className="font-semibold">{session.language}</p>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">Runtime</span>
              <p className="font-semibold">{session.runtime_info || "N/A"}</p>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">Model</span>
              <p className="font-semibold">{session.llm_model || "N/A"}</p>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-400">Created</span>
              <p className="font-semibold">
                {format(new Date(session.created_at), "MMM d, h:mm a")}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
        <div className="border-b border-gray-200 dark:border-gray-700">
          <div className="flex overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 font-medium transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? "border-b-2 border-blue-600 text-blue-600"
                    : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="p-6">
          {activeTab === "explanation" && (
            <div className="prose dark:prose-invert max-w-none">
              <h3 className="text-xl font-semibold mb-4">Root Cause Analysis</h3>
              <div className="whitespace-pre-wrap bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                {session.explanation || "No explanation available"}
              </div>
            </div>
          )}

          {activeTab === "fix" && (
            <div className="prose dark:prose-invert max-w-none">
              <h3 className="text-xl font-semibold mb-4">Suggested Fix</h3>
              <div className="whitespace-pre-wrap bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                {session.fix_suggestion || "No fix suggestion available"}
              </div>
            </div>
          )}

          {activeTab === "repro" && (
            <div>
              <h3 className="text-xl font-semibold mb-4">Reproduction Code</h3>
              <CodeBlock
                code={session.repro_code || "No reproduction code available"}
                language={session.language}
              />
            </div>
          )}

          {activeTab === "test" && (
            <div>
              <h3 className="text-xl font-semibold mb-4">Unit Test</h3>
              <CodeBlock
                code={session.test_code || "No test code available"}
                language={session.language}
              />
            </div>
          )}

          {activeTab === "context" && (
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">Error Message</h3>
                <CodeBlock code={session.error_text} />
              </div>
              {session.code_snippet && (
                <div>
                  <h3 className="text-xl font-semibold mb-2">Code Snippet</h3>
                  <CodeBlock code={session.code_snippet} language={session.language} />
                </div>
              )}
              {session.context_description && (
                <div>
                  <h3 className="text-xl font-semibold mb-2">Context</h3>
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                    {session.context_description}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
