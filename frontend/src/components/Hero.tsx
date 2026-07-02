import { Link } from "react-router-dom";

export function Hero() {
  return (
    <section className="grid gap-8 rounded-[2rem] border border-white/30 bg-white/70 p-8 shadow-panel backdrop-blur dark:border-white/10 dark:bg-slate/20 md:grid-cols-[1.4fr_1fr]">
      <div>
        <p className="mb-3 text-sm uppercase tracking-[0.3em] text-ember">Explainable Medical AI</p>
        <h1 className="font-display text-4xl leading-tight md:text-6xl">
          Skin lesion triage with clear evidence, reproducible pipelines, and production APIs.
        </h1>
        <p className="mt-6 max-w-2xl text-lg text-slate dark:text-mist">
          DermaVision AI classifies HAM10000 dermoscopy images, surfaces Grad-CAM evidence,
          tracks experiments, and ships with a frontend, backend, Docker stack, and evaluation
          tooling.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link to="/predict" className="rounded-full bg-ember px-6 py-3 font-semibold text-white">
            Run Prediction
          </Link>
          <Link
            to="/docs"
            className="rounded-full border border-slate/20 px-6 py-3 font-semibold text-slate dark:border-mist/20 dark:text-mist"
          >
            Architecture & Docs
          </Link>
        </div>
      </div>
      <div className="grid gap-4">
        {[
          ["7", "diagnostic classes"],
          ["Grad-CAM", "visual explanation"],
          ["FastAPI", "typed inference API"],
          ["MLflow + DVC", "experiment workflow"],
        ].map(([value, label]) => (
          <div key={label} className="rounded-3xl bg-ink p-5 text-sand dark:bg-white/10">
            <div className="font-display text-3xl">{value}</div>
            <div className="mt-2 text-sm uppercase tracking-[0.2em] text-mist">{label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
