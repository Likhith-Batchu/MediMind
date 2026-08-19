/**
 * Phase 0 placeholder landing page.
 * Purpose: confirm the frontend boots and can (eventually) reach the
 * backend API. Real landing page design comes later, once auth exists.
 */

"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [apiStatus, setApiStatus] = useState<string>("checking...");

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/health")
      .then((res) => res.json())
      .then((data) => setApiStatus(data.status === "ok" ? "connected" : "error"))
      .catch(() => setApiStatus("backend not reachable"));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-4xl font-bold text-brand">MediMind AI</h1>
      <p className="text-slate-600">Smarter Healthcare. Connected Care.</p>
      <div className="mt-6 rounded-lg border border-slate-200 bg-white px-6 py-4 shadow-sm">
        <p className="text-sm text-slate-500">Backend API status:</p>
        <p
          className={`font-mono text-sm ${
            apiStatus === "connected" ? "text-green-600" : "text-amber-600"
          }`}
        >
          {apiStatus}
        </p>
      </div>
    </main>
  );
}
