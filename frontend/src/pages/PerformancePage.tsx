import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const performanceData = [
  { model: "Baseline", macroF1: 0.58 },
  { model: "ResNet50", macroF1: 0.69 },
  { model: "DenseNet121", macroF1: 0.71 },
  { model: "EfficientNet-B0", macroF1: 0.74 },
  { model: "ConvNeXt Tiny", macroF1: 0.76 },
];

export function PerformancePage() {
  return (
    <section className="rounded-[2rem] bg-white/70 p-8 shadow-panel dark:bg-white/5">
      <p className="text-sm uppercase tracking-[0.2em] text-ember">Model Performance</p>
      <h1 className="mt-3 font-display text-4xl">Benchmark view</h1>
      <div className="mt-8 h-80 rounded-[1.75rem] bg-sand p-4 dark:bg-ink/60">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={performanceData}>
            <defs>
              <linearGradient id="macroF1" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#D1683F" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#D1683F" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis dataKey="model" />
            <YAxis domain={[0.5, 0.85]} />
            <Tooltip />
            <Area type="monotone" dataKey="macroF1" stroke="#D1683F" fillOpacity={1} fill="url(#macroF1)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
