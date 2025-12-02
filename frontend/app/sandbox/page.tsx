"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

type RunResponse = {
  run_id: string;
  language: string;
  status: string;
  stdout?: string;
  stderr?: string;
  exit_code?: number;
  image?: string;
  created_at: string;
  completed_at?: string;
};

const defaultSnippets: Record<string, string> = {
  python: "print('Hello from Python sandbox!')\nfor i in range(3):\n    print(f'Count: {i}')",
  javascript:
    "console.log('Hello from Node!');\nfor (let i=0;i<3;i++){ console.log('Count: ' + i); }",
  java: `public class Main {\n  public static void main(String[] args){\n    System.out.println("Hello from Java!");\n    for(int i=0;i<3;i++){ System.out.println("Count: "+i); }\n  }\n}`,
};

export default function SandboxPage() {
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(defaultSnippets["python"]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [imagesReady, setImagesReady] = useState<boolean>(false);
  const [building, setBuilding] = useState<boolean>(false);
  const [buildLogs, setBuildLogs] = useState<string>("");

  const onLangChange = (lang: string) => {
    setLanguage(lang);
    setCode(defaultSnippets[lang] || "");
  };

  const run = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const { data } = await api.post<RunResponse>("/api/runs", {
        language,
        code,
        timeout_sec: 15,
      });
      setResult(data);
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || "Run failed";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const checkImages = async () => {
    try {
      const { data } = await api.get("/api/sandbox/images");
      const imgs = data?.images || {};
      const ok = imgs["bug-ghost-sandbox-python:latest"] && imgs["bug-ghost-sandbox-node:latest"] && imgs["bug-ghost-sandbox-java:latest"];
      setImagesReady(!!ok);
    } catch (e) {
      setImagesReady(false);
    }
  };

  const buildImages = async () => {
    setBuilding(true);
    setBuildLogs("");
    setError(null);
    try {
      const { data } = await api.post("/api/sandbox/images/build", { languages: ["python", "javascript", "java"] });
      const results = data?.results || {};
      const logs = Object.keys(results)
        .map((k) => `=== ${k} (${results[k]?.image}) ===\n${(results[k]?.logs || []).join("\n")}`)
        .join("\n\n");
      setBuildLogs(logs);
      // re-check
      await checkImages();
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || "Build failed";
      setError(msg);
    } finally {
      setBuilding(false);
    }
  };

  useEffect(() => {
    checkImages();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Sandbox Runner</h1>
      <p className="text-sm text-gray-600">Run code in an isolated container (non-root, no network, resource limited).</p>

      <div className="flex gap-4 items-center">
        <label className="text-sm">Language</label>
        <select
          className="border rounded px-3 py-2"
          value={language}
          onChange={(e) => onLangChange(e.target.value)}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript (Node)</option>
          <option value="java">Java</option>
        </select>
        <button
          onClick={run}
          disabled={loading}
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-60"
        >
          {loading ? "Running..." : "Run"}
        </button>
        <button
          onClick={buildImages}
          disabled={building}
          className="border px-3 py-2 rounded disabled:opacity-60"
        >
          {building ? "Building images..." : "Build Sandbox Images"}
        </button>
        <span className={`text-sm ${imagesReady ? "text-green-600" : "text-orange-600"}`}>
          {imagesReady ? "Images ready" : "Images missing"}
        </span>
      </div>

      <div>
        <label className="block text-sm mb-1">Code</label>
        <textarea
          className="w-full border rounded p-3 font-mono text-sm h-60"
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
      </div>

      {error && (
        <div className="border border-red-300 bg-red-50 text-red-700 p-3 rounded">{error}</div>
      )}

      {result && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h2 className="font-medium mb-1">Stdout</h2>
            <pre className="border rounded p-3 bg-gray-50 whitespace-pre-wrap text-sm min-h-[140px]">{result.stdout || ""}</pre>
          </div>
          <div>
            <h2 className="font-medium mb-1">Stderr</h2>
            <pre className="border rounded p-3 bg-gray-50 whitespace-pre-wrap text-sm min-h-[140px]">{result.stderr || ""}</pre>
          </div>
          <div className="text-sm text-gray-600">
            <div><span className="font-medium">Run ID:</span> {result.run_id}</div>
            <div><span className="font-medium">Status:</span> {result.status}</div>
            <div><span className="font-medium">Image:</span> {result.image}</div>
          </div>
        </div>
      )}

      {buildLogs && (
        <div>
          <h2 className="font-medium mb-1">Build Logs</h2>
          <pre className="border rounded p-3 bg-gray-50 whitespace-pre-wrap text-xs max-h-80 overflow-auto">{typeof buildLogs === "string" ? buildLogs : JSON.stringify(buildLogs, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
