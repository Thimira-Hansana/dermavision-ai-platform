import { useQuery } from "@tanstack/react-query";
import { fetchHistory } from "../services/api";

export function HistoryPage() {
  const { data, isLoading } = useQuery({ queryKey: ["history"], queryFn: fetchHistory });

  return (
    <section className="rounded-[2rem] bg-white/70 p-8 shadow-panel dark:bg-white/5">
      <p className="text-sm uppercase tracking-[0.2em] text-ember">Prediction History</p>
      <h1 className="mt-3 font-display text-4xl">Recent inference log</h1>
      <div className="mt-8 overflow-hidden rounded-[1.75rem] border border-slate/10">
        <table className="min-w-full text-left">
          <thead className="bg-slate/10 text-sm uppercase tracking-[0.15em] text-slate dark:bg-white/10 dark:text-mist">
            <tr>
              <th className="px-4 py-3">File</th>
              <th className="px-4 py-3">Class</th>
              <th className="px-4 py-3">Confidence</th>
              <th className="px-4 py-3">Model</th>
              <th className="px-4 py-3">Time</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td className="px-4 py-6" colSpan={5}>
                  Loading...
                </td>
              </tr>
            ) : (
              data?.map((row) => (
                <tr key={row.id} className="border-t border-slate/10 dark:border-white/10">
                  <td className="px-4 py-3">{row.filename}</td>
                  <td className="px-4 py-3">{row.predicted_class}</td>
                  <td className="px-4 py-3">{(row.confidence * 100).toFixed(1)}%</td>
                  <td className="px-4 py-3">{row.model_version}</td>
                  <td className="px-4 py-3">{new Date(row.created_at).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
