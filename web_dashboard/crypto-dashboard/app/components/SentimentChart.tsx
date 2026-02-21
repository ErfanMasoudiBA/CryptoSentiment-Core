"use client";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";

interface SentimentChartProps {
  positive: number;
  negative: number;
  neutral: number;
  coinName?: string;
}

const COLORS = {
  positive: "#10b981", // green
  negative: "#ef4444", // red
  neutral: "#6b7280", // gray
};

export default function SentimentChart({
  positive,
  negative,
  neutral,
  coinName,
}: SentimentChartProps) {
  const total = positive + negative + neutral;

  if (total === 0) {
    return (
      <div className="bg-slate-800 rounded-lg p-8 border border-slate-700">
        <p className="text-slate-400 text-center">No data available</p>
      </div>
    );
  }

  const data = [
    { name: "Positive", value: positive, color: COLORS.positive },
    { name: "Negative", value: negative, color: COLORS.negative },
    { name: "Neutral", value: neutral, color: COLORS.neutral },
  ].filter((item) => item.value > 0);

  const renderLabel = (entry: { value: number }) => {
    const percent = ((entry.value / total) * 100).toFixed(1);
    return `${percent}%`;
  };

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <h2 className="text-lg md:text-xl font-bold text-white mb-4 md:mb-6 text-center">
        {coinName ? `${coinName} Sentiment` : "Market Sentiment"}
      </h2>
      <div className="w-full max-w-md flex justify-center">
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderLabel}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "#1e293b",
                border: "1px solid #334155",
                borderRadius: "8px",
                color: "#fff",
              }}
            />
            <Legend wrapperStyle={{ color: "#e2e8f0" }} iconType="circle" />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 md:mt-6 grid grid-cols-3 gap-2 md:gap-4 w-full max-w-md">
        <div className="text-center p-2 md:p-3">
          <div className="text-lg md:text-2xl font-bold text-green-400">
            {positive}
          </div>
          <div className="text-xs md:text-sm text-slate-400">Positive</div>
        </div>
        <div className="text-center p-2 md:p-3">
          <div className="text-lg md:text-2xl font-bold text-red-400">
            {negative}
          </div>
          <div className="text-xs md:text-sm text-slate-400">Negative</div>
        </div>
        <div className="text-center p-2 md:p-3">
          <div className="text-lg md:text-2xl font-bold text-slate-400">
            {neutral}
          </div>
          <div className="text-xs md:text-sm text-slate-400">Neutral</div>
        </div>
      </div>
    </div>
  );
}
