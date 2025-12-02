"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { DebugSessionResponse } from "@/lib/types";
import SessionResult from "@/components/SessionResult";
import { Loader2, AlertCircle } from "lucide-react";
import Link from "next/link";

export default function SessionDetailPage() {
  const params = useParams();
  const sessionId = params?.id as string;

  const [session, setSession] = useState<DebugSessionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const response = await api.get<DebugSessionResponse>(
          `/api/debug-sessions/${sessionId}`
        );
        setSession(response.data);
      } catch (err: any) {
        setError("Failed to load session");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (sessionId) {
      fetchSession();
    }
  }, [sessionId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-12">
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
        <div className="container mx-auto px-4 py-12">
          <div className="max-w-2xl mx-auto bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-6 py-4 rounded-lg flex items-center space-x-3">
            <AlertCircle className="w-6 h-6" />
            <div>
              <p className="font-semibold">{error || "Session not found"}</p>
              <Link href="/sessions" className="underline text-sm">
                Back to sessions
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-blue-950 dark:to-indigo-950">
      <div className="container mx-auto px-4 py-12">
        <SessionResult session={session} onNewSession={() => {}} />
      </div>
    </div>
  );
}
