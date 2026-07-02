const sections = [
  ["Training", "Use Poetry to install dependencies, then run `poetry run dermavision-train`."],
  ["Evaluation", "Run `poetry run dermavision-evaluate` to generate metrics and confusion matrices."],
  ["API", "Launch `uvicorn backend.main:app --reload` and inspect Swagger at `/docs`."],
  ["Frontend", "Run `npm install` then `npm run dev` inside `frontend/`."],
];

export function DocumentationPage() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] bg-white/70 p-8 shadow-panel dark:bg-white/5">
        <p className="text-sm uppercase tracking-[0.2em] text-ember">Documentation</p>
        <h1 className="mt-3 font-display text-4xl">Operational guide</h1>
      </section>
      <div className="grid gap-6 md:grid-cols-2">
        {sections.map(([title, body]) => (
          <article key={title} className="rounded-[1.75rem] bg-white/70 p-6 shadow-panel dark:bg-white/5">
            <h2 className="font-display text-2xl">{title}</h2>
            <p className="mt-3 text-slate dark:text-mist">{body}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
