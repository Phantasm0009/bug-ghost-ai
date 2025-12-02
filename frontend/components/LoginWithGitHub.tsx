"use client";
import { useAuth } from "@/lib/auth";

export default function LoginWithGitHub() {
  const { user, logout } = useAuth();

  const startLogin = () => {
    window.location.href = `http://localhost:8000/api/auth/github/login`;
  };

  return (
    <div className="flex items-center gap-2">
      {user ? (
        <>
          {user.avatar_url && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={user.avatar_url} alt="avatar" className="w-6 h-6 rounded-full" />
          )}
          <span className="text-sm text-gray-700 dark:text-gray-300">{user.name || user.username}</span>
          <button onClick={logout} className="border px-3 py-1 rounded text-sm">Logout</button>
        </>
      ) : (
        <button onClick={startLogin} className="border px-3 py-1 rounded text-sm">Login with GitHub</button>
      )}
    </div>
  );
}
