"use client";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import api from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function GitHubCallbackPage() {
  const router = useRouter();
  const params = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);
  const { setUser: setAuthUser } = useAuth();

  useEffect(() => {
    const code = params.get("code");
    if (!code) {
      setError("Missing GitHub code");
      return;
    }
    const run = async () => {
      try {
        const { data } = await api.get(`/api/auth/github/callback?code=${code}`);
        const u = data?.user || data;
        setUser(u);
        // Persist in auth store
        if (u) {
          setAuthUser({
            id: u.id,
            username: u.username,
            name: u.name,
            avatar_url: u.avatar_url,
          });
        }
        // TODO: store token/cookie if backend issues JWT later
        // Navigate to home
        setTimeout(() => router.push("/"), 1200);
      } catch (e: any) {
        const msg = e?.response?.data?.detail || e?.message || "Login failed";
        setError(msg);
      }
    };
    run();
  }, [params, router]);

  return (
    <div className="max-w-lg mx-auto p-6 space-y-4">
      <h1 className="text-xl font-semibold">GitHub Login</h1>
      {!error && !user && <p>Completing login…</p>}
      {error && <div className="border border-red-300 bg-red-50 text-red-700 p-3 rounded">{error}</div>}
      {user && (
        <div className="border rounded p-3 bg-gray-50">
          <div className="font-medium mb-2">Logged in as:</div>
          <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(user, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
