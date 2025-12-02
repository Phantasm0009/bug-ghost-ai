"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";

type Team = { id: string; name: string; created_at?: string };
type User = { id: string; username?: string; name?: string };

export default function TeamsPage() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [newName, setNewName] = useState("");
  const [error, setError] = useState<string | null>(null);

  const loadTeams = async () => {
    try {
      const { data } = await api.get("/api/teams");
      setTeams(data?.teams || []);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || "Failed to load teams");
    }
  };

  const createTeam = async () => {
    setError(null);
    try {
      await api.post("/api/teams", { name: newName });
      setNewName("");
      await loadTeams();
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || "Create failed");
    }
  };

  useEffect(() => {
    loadTeams();
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Teams</h1>
      <div className="flex gap-2 items-center">
        <input
          className="border rounded px-3 py-2"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="New team name"
        />
        <button onClick={createTeam} className="bg-black text-white px-4 py-2 rounded">Create</button>
      </div>
      {error && <div className="border border-red-300 bg-red-50 text-red-700 p-3 rounded">{error}</div>}
      <ul className="space-y-2">
        {teams.map((t) => (
          <li key={t.id} className="border rounded p-3 bg-gray-50 flex items-center justify-between">
            <div>
              <div className="font-medium">{t.name}</div>
              <div className="text-xs text-gray-600">{t.id}</div>
            </div>
            <AddMemberForm teamId={t.id} />
          </li>
        ))}
      </ul>
    </div>
  );
}

function AddMemberForm({ teamId }: { teamId: string }) {
  const [userId, setUserId] = useState("");
  const [role, setRole] = useState("member");
  const [msg, setMsg] = useState<string | null>(null);

  const addMember = async () => {
    setMsg(null);
    try {
      await api.post(`/api/teams/${teamId}/members`, { user_id: userId, role });
      setMsg("Added");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || e?.message || "Failed");
    }
  };

  return (
    <div className="flex items-center gap-2">
      <input
        className="border rounded px-2 py-1 text-sm"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        placeholder="User ID"
      />
      <select className="border rounded px-2 py-1 text-sm" value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="member">Member</option>
        <option value="admin">Admin</option>
      </select>
      <button onClick={addMember} className="border px-3 py-1 rounded text-sm">Add</button>
      {msg && <span className="text-xs text-gray-600">{msg}</span>}
    </div>
  );
}
