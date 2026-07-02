export function AboutPage() {
  return (
    <section className="rounded-[2rem] bg-white/70 p-8 shadow-panel dark:bg-white/5">
      <p className="text-sm uppercase tracking-[0.2em] text-ember">About</p>
      <h1 className="mt-3 font-display text-4xl">Research-first skin lesion analysis</h1>
      <div className="mt-6 space-y-4 text-slate dark:text-mist">
        <p>
          DermaVision AI is built on the HAM10000 dataset and targets educational, research, and
          portfolio usage. It combines classification, optional segmentation-assisted cropping,
          explainability, experiment tracking, and deployment assets in a single repository.
        </p>
        <p>
          The system is not a medical device. Outputs should be treated as model-generated
          suggestions that require review by qualified clinicians.
        </p>
      </div>
    </section>
  );
}
