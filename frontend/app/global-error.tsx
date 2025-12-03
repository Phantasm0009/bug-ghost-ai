"use client";

import { AlertTriangle } from "lucide-react";

export default function GlobalError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-6 py-5 rounded-xl max-w-xl w-full">
            <div className="flex items-center space-x-3 mb-2">
              <AlertTriangle className="w-6 h-6" />
              <h2 className="text-lg font-semibold">App crashed</h2>
            </div>
            <p className="text-sm opacity-80 mb-4">{error.message || "An unexpected error occurred."}</p>
            <button onClick={() => reset()} className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
              Reload
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
