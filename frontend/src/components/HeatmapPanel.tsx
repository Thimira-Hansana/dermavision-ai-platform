type Props = {
  gradcamUrl: string | null;
};

export function HeatmapPanel({ gradcamUrl }: Props) {
  return (
    <section className="rounded-[2rem] border border-white/30 bg-white/75 p-6 shadow-panel backdrop-blur dark:border-white/10 dark:bg-white/5">
      <p className="text-sm uppercase tracking-[0.2em] text-ember">Grad-CAM</p>
      {gradcamUrl ? (
        <img
          src={`${import.meta.env.VITE_API_URL ?? "http://localhost:8000"}${gradcamUrl}`}
          alt="Grad-CAM heatmap"
          className="mt-4 h-full w-full rounded-3xl object-cover"
        />
      ) : (
        <div className="mt-4 rounded-3xl border border-dashed border-slate/20 p-10 text-center text-slate dark:border-mist/20 dark:text-mist">
          Heatmap will appear after a successful prediction.
        </div>
      )}
    </section>
  );
}
