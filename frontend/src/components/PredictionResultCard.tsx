import type { PredictionResponse } from "../types/api";

type Props = {
  prediction: PredictionResponse;
};

export function PredictionResultCard({ prediction }: Props) {
  return (
    <section className="rounded-[2rem] border border-white/30 bg-white/75 p-6 shadow-panel backdrop-blur dark:border-white/10 dark:bg-white/5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-ember">Prediction</p>
          <h2 className="font-display text-4xl">{prediction.diagnosis_name}</h2>
          <p className="mt-2 text-slate dark:text-mist">{prediction.predicted_class}</p>
        </div>
        <div className="rounded-3xl bg-ink px-5 py-4 text-sand dark:bg-sand dark:text-ink">
          <div className="text-sm uppercase tracking-[0.2em]">Confidence</div>
          <div className="font-display text-4xl">{(prediction.confidence * 100).toFixed(1)}%</div>
        </div>
      </div>
      <div className="mt-6 space-y-3">
        {prediction.top_3_predictions.map((item) => {
          const label = item.class_name ?? item.class ?? "unknown";
          return (
            <div key={label}>
              <div className="mb-1 flex justify-between text-sm">
                <span>{label}</span>
                <span>{(item.confidence * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 rounded-full bg-mist/60 dark:bg-white/10">
                <div
                  className="h-3 rounded-full bg-ember"
                  style={{ width: `${Math.max(item.confidence * 100, 3)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-3xl bg-sand p-4 dark:bg-ink/60">
          <p className="text-sm uppercase tracking-[0.2em] text-slate dark:text-mist">Model</p>
          <p className="mt-2 font-semibold">{prediction.model_version}</p>
          <p className="text-sm">{prediction.model_ready ? "Trained artifact loaded" : "Demo mode"}</p>
        </div>
        <div className="rounded-3xl bg-sand p-4 dark:bg-ink/60">
          <p className="text-sm uppercase tracking-[0.2em] text-slate dark:text-mist">Latency</p>
          <p className="mt-2 font-semibold">{prediction.inference_time_ms.toFixed(1)} ms</p>
          <p className="text-sm">{new Date(prediction.timestamp).toLocaleString()}</p>
        </div>
      </div>
      <p className="mt-6 text-sm text-slate dark:text-mist">{prediction.disclaimer}</p>
    </section>
  );
}
