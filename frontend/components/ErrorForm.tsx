"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import api from "@/lib/api";
import { DebugSessionCreate, DebugSessionResponse } from "@/lib/types";
import { Loader2 } from "lucide-react";

interface ErrorFormProps {
  onSubmitSuccess: (session: DebugSessionResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const LANGUAGES = [
  "JavaScript",
  "TypeScript",
  "Python",
  "Java",
  "Go",
  "Rust",
  "C++",
  "C#",
  "Ruby",
  "PHP",
  "Other",
];

export default function ErrorForm({
  onSubmitSuccess,
  isLoading,
  setIsLoading,
}: ErrorFormProps) {
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DebugSessionCreate>();

  const onSubmit = async (data: DebugSessionCreate) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.post<DebugSessionResponse>(
        "/api/debug-sessions",
        data
      );
      onSubmitSuccess(response.data);
    } catch (err: any) {
      console.error("Error creating session:", err);
      setError(
        err.response?.data?.detail || "Failed to create session. Please try again."
      );
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="bg-white dark:bg-slate-800 rounded-xl shadow-xl p-8 space-y-6"
    >
      <h2 className="text-2xl font-bold mb-6">Paste Your Error</h2>

      {/* Language */}
      <div>
        <label className="block text-sm font-medium mb-2">
          Language <span className="text-red-500">*</span>
        </label>
        <select
          {...register("language", { required: "Language is required" })}
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Select a language...</option>
          {LANGUAGES.map((lang) => (
            <option key={lang} value={lang}>
              {lang}
            </option>
          ))}
        </select>
        {errors.language && (
          <p className="text-red-500 text-sm mt-1">{errors.language.message}</p>
        )}
      </div>

      {/* Runtime Info */}
      <div>
        <label className="block text-sm font-medium mb-2">
          Runtime Info <span className="text-gray-400">(optional)</span>
        </label>
        <input
          {...register("runtime_info")}
          type="text"
          placeholder="e.g., Node 18.x, Python 3.11, etc."
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Error Text */}
      <div>
        <label className="block text-sm font-medium mb-2">
          Error Message / Stack Trace <span className="text-red-500">*</span>
        </label>
        <textarea
          {...register("error_text", { required: "Error text is required" })}
          rows={6}
          placeholder="Paste your error message or stack trace here..."
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
        />
        {errors.error_text && (
          <p className="text-red-500 text-sm mt-1">{errors.error_text.message}</p>
        )}
      </div>

      {/* Code Snippet */}
      <div>
        <label className="block text-sm font-medium mb-2">
          Relevant Code Snippet <span className="text-gray-400">(optional but recommended)</span>
        </label>
        <textarea
          {...register("code_snippet")}
          rows={8}
          placeholder="Paste the relevant code where the error occurs..."
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
        />
      </div>

      {/* Context */}
      <div>
        <label className="block text-sm font-medium mb-2">
          Context Description <span className="text-gray-400">(optional)</span>
        </label>
        <textarea
          {...register("context_description")}
          rows={3}
          placeholder="When does this error occur? What were you doing? Any other relevant context..."
          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Analyzing Error...</span>
          </>
        ) : (
          <span>Generate Reproduction</span>
        )}
      </button>
    </form>
  );
}
