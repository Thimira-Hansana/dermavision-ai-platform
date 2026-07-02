import { Hero } from "../components/Hero";

export function LandingPage() {
  return (
    <div className="space-y-8">
      <Hero />
      <section className="grid gap-5 md:grid-cols-3">
        {[
          "Clean-architecture Python package with dataset discovery, training, evaluation, and export scripts.",
          "Async FastAPI backend with prediction history, Prometheus metrics, and static Grad-CAM artifact serving.",
          "Vite + React interface for clinicians, researchers, or reviewers to inspect evidence and system status.",
        ].map((text) => (
          <article key={text} className="rounded-[1.75rem] bg-white/60 p-6 shadow-panel dark:bg-white/5">
            <p className="text-base leading-7 text-slate dark:text-mist">{text}</p>
          </article>
        ))}
      </section>
    </div>
  );
}
