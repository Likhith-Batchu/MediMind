
"use client";

import { FormEvent, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const initialValues = {
  Age: "45",
  Gender: "Male",
  TB: "1.0",
  DB: "0.3",
  Alkphos: "200",
  Sgpt: "30",
  Sgot: "35",
  TP: "6.8",
  ALB: "3.5",
  A_G_Ratio: "1.0",
};

type Prediction = {
  model: string;
  experimental_output: string;
  class_id: number;
  class_probability: {
    non_liver_class: number;
    liver_disease_class: number;
  };
  notice: string;
};

const fields = [
  { key: "TB", label: "Total bilirubin", unit: "mg/dL" },
  { key: "DB", label: "Direct bilirubin", unit: "mg/dL" },
  { key: "Alkphos", label: "Alkaline phosphatase", unit: "U/L" },
  { key: "Sgpt", label: "SGPT / ALT", unit: "U/L" },
  { key: "Sgot", label: "SGOT / AST", unit: "U/L" },
  { key: "TP", label: "Total proteins", unit: "g/dL" },
  { key: "ALB", label: "Albumin", unit: "g/dL" },
  { key: "A_G_Ratio", label: "Albumin / Globulin ratio", unit: "Ratio" },
] as const;

export default function Home() {
  const [values, setValues] = useState(initialValues);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateValue(key: keyof typeof initialValues, value: string) {
    setValues((current) => ({ ...current, [key]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    const payload = {
      Age: Number(values.Age),
      Gender: values.Gender,
      TB: Number(values.TB),
      DB: Number(values.DB),
      Alkphos: Number(values.Alkphos),
      Sgpt: Number(values.Sgpt),
      Sgot: Number(values.Sgot),
      TP: Number(values.TP),
      ALB: Number(values.ALB),
      A_G_Ratio: Number(values.A_G_Ratio),
    };

    try {
      const response = await fetch(`${API_URL}/api/v1/ai/liver-risk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        const detail =
          typeof data.detail === "string"
            ? data.detail
            : "Please check your inputs and try again.";
        throw new Error(detail);
      }

      setPrediction(data as Prediction);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to contact the MediMind AI backend."
      );
    } finally {
      setLoading(false);
    }
  }

  function resetForm() {
    setValues(initialValues);
    setPrediction(null);
    setError("");
  }

  return (
    <main className="min-h-screen bg-[#f5f8f7] text-slate-800">
      <header className="border-b border-emerald-950/10 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8">
          <a href="/" className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-900 text-2xl text-white">
              ✳
            </div>
            <div>
              <div className="text-xl font-bold tracking-tight text-emerald-950">
                MediMind <span className="text-emerald-700">AI</span>
              </div>
              <div className="text-xs text-slate-500">
                Smarter Healthcare. Connected Care.
              </div>
            </div>
          </a>

          <div className="hidden items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-semibold text-emerald-800 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            ML PROTOTYPE
          </div>
        </div>
      </header>

      <section className="relative overflow-hidden bg-[#103c32] text-white">
        <div className="pointer-events-none absolute -right-20 -top-32 h-96 w-96 rounded-full border border-white/10" />
        <div className="pointer-events-none absolute -right-4 -top-16 h-64 w-64 rounded-full border border-white/10" />

        <div className="relative mx-auto max-w-7xl px-5 py-12 sm:px-8 sm:py-16">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-300/25 bg-white/5 px-3 py-1.5 text-xs font-medium text-emerald-100">
            <span className="text-emerald-300">✦</span>
            LIVER HEALTH & CLINICAL ASSISTANCE
          </div>

          <h1 className="max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
            Liver Health
            <span className="block text-emerald-300">
              Assessment Workspace
            </span>
          </h1>

          <p className="mt-5 max-w-2xl text-sm leading-7 text-emerald-50/75 sm:text-base">
            Explore MediMind&apos;s experimental machine-learning pipeline
            using structured laboratory measurements. Enter the parameters
            below to run a prediction using the trained model.
          </p>

          <div className="mt-8 flex flex-wrap gap-3 text-xs text-emerald-50/80">
            <span className="rounded-lg border border-white/15 px-3 py-2">
              Research prototype
            </span>
            <span className="rounded-lg border border-white/15 px-3 py-2">
              Random Forest
            </span>
            <span className="rounded-lg border border-white/15 px-3 py-2">
              FastAPI integration
            </span>
          </div>
        </div>
      </section>

      <div className="mx-auto grid max-w-7xl gap-6 px-5 py-8 sm:px-8 lg:grid-cols-[1.25fr_0.75fr] lg:py-10">
        <section className="rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-100 px-6 py-5 sm:px-8">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-xl">
                ♧
              </div>
              <div>
                <h2 className="text-lg font-bold text-slate-900">
                  Laboratory parameters
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  Enter values matching the model&apos;s input features.
                </p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-7 p-6 sm:p-8">
            <div>
              <h3 className="mb-4 text-xs font-bold uppercase tracking-[0.16em] text-emerald-800">
                Patient information
              </h3>

              <div className="grid gap-4 sm:grid-cols-2">
                <label className="field-label">
                  Age
                  <span className="field-hint">Years</span>
                  <input
                    className="field-input"
                    type="number"
                    min="1"
                    max="120"
                    required
                    value={values.Age}
                    onChange={(e) => updateValue("Age", e.target.value)}
                  />
                </label>

                <label className="field-label">
                  Gender
                  <span className="field-hint">Dataset category</span>
                  <select
                    className="field-input"
                    value={values.Gender}
                    onChange={(e) => updateValue("Gender", e.target.value)}
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </label>
              </div>
            </div>

            <div>
              <h3 className="mb-4 text-xs font-bold uppercase tracking-[0.16em] text-emerald-800">
                Biochemical measurements
              </h3>

              <div className="grid gap-4 sm:grid-cols-2">
                {fields.map((field) => (
                  <label className="field-label" key={field.key}>
                    {field.label}
                    <span className="field-hint">{field.unit}</span>
                    <input
                      className="field-input"
                      type="number"
                      step="any"
                      min="0.000001"
                      required
                      value={values[field.key]}
                      onChange={(e) =>
                        updateValue(field.key, e.target.value)
                      }
                    />
                  </label>
                ))}
              </div>
            </div>

            {error && (
              <div
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
              >
                <strong>Request failed.</strong> {error}
              </div>
            )}

            <div className="flex flex-col gap-3 border-t border-slate-100 pt-6 sm:flex-row">
              <button
                type="submit"
                disabled={loading}
                className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-emerald-900 px-5 py-3.5 font-semibold text-white shadow-sm transition hover:bg-emerald-800 disabled:cursor-wait disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                    Running model...
                  </>
                ) : (
                  <>Run experimental analysis <span>→</span></>
                )}
              </button>

              <button
                type="button"
                onClick={resetForm}
                className="rounded-xl border border-slate-200 px-5 py-3.5 font-semibold text-slate-600 transition hover:bg-slate-50"
              >
                Reset
              </button>
            </div>

            <p className="text-xs leading-5 text-slate-400">
              Use only synthetic or appropriately authorized data for
              demonstrations. Do not enter identifiable patient information.
            </p>
          </form>
        </section>

        <aside className="space-y-6">
          <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="bg-[#153d34] px-6 py-5 text-white">
              <div className="flex items-center justify-between">
                <h2 className="font-bold">Model output</h2>
                <span className="rounded-full border border-white/20 px-2.5 py-1 text-[10px] font-semibold tracking-wider text-emerald-100">
                  LIVE API
                </span>
              </div>
              <p className="mt-1 text-sm text-emerald-100/70">
                Results from your trained pipeline
              </p>
            </div>

            <div className="p-6">
              {!prediction && !loading && (
                <div className="flex min-h-64 flex-col items-center justify-center text-center">
                  <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50 text-3xl">
                    ◈
                  </div>
                  <h3 className="font-semibold text-slate-800">
                    Your results will appear here
                  </h3>
                  <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                    Complete the form and run the model to view the actual
                    response returned by MediMind&apos;s API.
                  </p>
                </div>
              )}

              {loading && (
                <div
                  role="status"
                  className="flex min-h-64 flex-col items-center justify-center text-center"
                >
                  <div className="h-10 w-10 animate-spin rounded-full border-4 border-emerald-100 border-t-emerald-800" />
                  <p className="mt-4 font-semibold">Processing input</p>
                  <p className="mt-2 text-sm text-slate-500">
                    Waiting for the ML service...
                  </p>
                </div>
              )}

              {prediction && (
                <div className="space-y-6">
                  <div className="rounded-xl border border-emerald-100 bg-emerald-50/60 p-4">
                    <p className="text-xs font-bold uppercase tracking-wider text-emerald-800">
                      Experimental classification
                    </p>
                    <h3 className="mt-2 text-xl font-bold text-emerald-950">
                      {prediction.experimental_output}
                    </h3>
                    <p className="mt-2 text-xs text-emerald-800/70">
                      Model class: {prediction.class_id}
                    </p>
                  </div>

                  <div>
                    <h3 className="mb-4 text-sm font-bold text-slate-800">
                      Model-reported class scores
                    </h3>

                    {[
                      {
                        label: "Liver-disease class",
                        value:
                          prediction.class_probability.liver_disease_class,
                      },
                      {
                        label: "Non-liver class",
                        value: prediction.class_probability.non_liver_class,
                      },
                    ].map((item) => (
                      <div key={item.label} className="mb-5">
                        <div className="mb-2 flex items-center justify-between gap-3 text-sm">
                          <span className="text-slate-600">{item.label}</span>
                          <strong className="text-slate-900">
                            {(item.value * 100).toFixed(1)}%
                          </strong>
                        </div>
                        <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
                          <div
                            className="h-full rounded-full bg-emerald-700 transition-all duration-500"
                            style={{
                              width: `${Math.max(
                                0,
                                Math.min(100, item.value * 100)
                              )}%`,
                            }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="rounded-lg bg-slate-50 p-3">
                    <p className="text-xs leading-5 text-slate-500">
                      Model: <strong>{prediction.model}</strong>
                      <br />
                      Scores are model outputs, not calibrated clinical
                      probabilities.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </section>

          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
            <div className="flex items-start gap-3">
              <span className="text-xl text-amber-800">ⓘ</span>
              <div>
                <h3 className="font-bold text-amber-950">
                  Research prototype only
                </h3>
                <p className="mt-2 text-sm leading-6 text-amber-900/80">
                  This model has not been clinically validated. Its output
                  must not be used to diagnose disease, rule out disease,
                  or guide treatment. Clinical decisions require qualified
                  medical professionals.
                </p>
              </div>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-5">
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Current milestone
            </p>
            <div className="mt-4 space-y-3">
              {[
                "Dataset and initial EDA",
                "Two models trained and compared",
                "FastAPI inference endpoint",
                "Frontend integration",
              ].map((item, index) => (
                <div key={item} className="flex items-center gap-3 text-sm">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-xs font-bold text-emerald-800">
                    {index + 1}
                  </span>
                  <span className="text-slate-700">{item}</span>
                </div>
              ))}
            </div>
            <p className="mt-4 border-t border-slate-100 pt-3 text-xs text-slate-400">
              Automated endpoint tests and broader validation remain
              necessary before this milestone is complete.
            </p>
          </section>
        </aside>
      </div>

      <footer className="border-t border-slate-200 bg-white px-5 py-6 text-center text-xs text-slate-400">
        MediMind AI · Smarter Healthcare. Connected Care.
        <br />
        Experimental student research prototype.
      </footer>
    </main>
  );
}
