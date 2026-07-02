import { useQuery } from "@tanstack/react-query";
import { fetchModelInfo } from "../services/api";

export function SettingsPage() {
  const { data } = useQuery({ queryKey: ["model-info"], queryFn: fetchModelInfo });

  return (
    <section className="rounded-[2rem] bg-white/70 p-8 shadow-panel dark:bg-white/5">
      <p className="text-sm uppercase tracking-[0.2em] text-ember">Settings</p>
      <h1 className="mt-3 font-display text-4xl">Runtime configuration</h1>
      {data ? (
        <div className="mt-8 grid gap-5 md:grid-cols-2">
          <div className="rounded-[1.75rem] bg-sand p-5 dark:bg-ink/60">
            <p className="text-sm uppercase tracking-[0.2em] text-slate dark:text-mist">Model</p>
            <p className="mt-2 text-xl font-semibold">{data.model_name}</p>
            <p className="text-sm">{data.model_version}</p>
          </div>
          <div className="rounded-[1.75rem] bg-sand p-5 dark:bg-ink/60">
            <p className="text-sm uppercase tracking-[0.2em] text-slate dark:text-mist">Device</p>
            <p className="mt-2 text-xl font-semibold">{data.device}</p>
            <p className="text-sm">{data.model_ready ? "Checkpoint loaded" : "Waiting for training artifact"}</p>
          </div>
        </div>
      ) : null}
    </section>
  );
}
