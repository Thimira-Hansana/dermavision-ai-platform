import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { HeatmapPanel } from "../components/HeatmapPanel";
import { PredictionResultCard } from "../components/PredictionResultCard";
import { predictImage } from "../services/api";
import type { PredictionResponse } from "../types/api";

export function PredictionPage() {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({
    mutationFn: predictImage,
  });

  const previewUrl = file ? URL.createObjectURL(file) : null;
  const prediction: PredictionResponse | undefined = mutation.data;

  return (
    <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
      <section className="rounded-[2rem] border border-white/30 bg-white/75 p-6 shadow-panel dark:border-white/10 dark:bg-white/5">
        <p className="text-sm uppercase tracking-[0.2em] text-ember">Prediction Workflow</p>
        <h1 className="mt-3 font-display text-4xl">Upload a dermoscopy image</h1>
        <label className="mt-6 flex min-h-72 cursor-pointer flex-col items-center justify-center rounded-[1.75rem] border-2 border-dashed border-slate/20 bg-sand/70 p-6 text-center dark:border-mist/20 dark:bg-ink/30">
          <input
            type="file"
            accept="image/png,image/jpeg"
            className="hidden"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
          {previewUrl ? (
            <img src={previewUrl} alt="Preview" className="h-64 w-full rounded-3xl object-cover" />
          ) : (
            <div>
              <p className="font-semibold">Drop an image or click to browse</p>
              <p className="mt-2 text-sm text-slate dark:text-mist">PNG and JPEG up to 10 MB.</p>
            </div>
          )}
        </label>
        <button
          type="button"
          disabled={!file || mutation.isPending}
          onClick={() => file && mutation.mutate(file)}
          className="mt-6 rounded-full bg-ember px-6 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {mutation.isPending ? "Running..." : "Run prediction"}
        </button>
        {mutation.isError ? (
          <p className="mt-4 text-sm text-red-700">Prediction failed. Check backend connectivity and file type.</p>
        ) : null}
      </section>
      <div className="space-y-8">
        {prediction ? <PredictionResultCard prediction={prediction} /> : null}
        <HeatmapPanel gradcamUrl={prediction?.gradcam_url ?? null} />
      </div>
    </div>
  );
}
