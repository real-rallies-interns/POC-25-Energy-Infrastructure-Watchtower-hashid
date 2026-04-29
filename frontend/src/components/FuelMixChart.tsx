"use client";

import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

interface FuelMixChartProps {
  data: any;
  colors: string[];
}

export function FuelMixChartWrapper({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-full aspect-[4/3] min-h-[192px] relative">
      <div className="absolute inset-0">
        {children}
      </div>
    </div>
  );
}

export default function FuelMixChart({ data, colors }: FuelMixChartProps) {
  return (
    <FuelMixChartWrapper>
      <ResponsiveContainer width="100%" height="100%" debounce={100}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={70}
            paddingAngle={2}
            dataKey="percentage"
            nameKey="source"
            stroke="none"
          >
            {data?.map((entry: any) => (
              <Cell key={`cell-${entry.source}`} fill={colors[data.indexOf(entry) % colors.length]} />
            ))}
          </Pie>
          <RechartsTooltip
            contentStyle={{ backgroundColor: '#0B1117', borderColor: '#1F2937', borderRadius: '8px' }}
            itemStyle={{ color: '#f8fafc' }}
          />
        </PieChart>
      </ResponsiveContainer>
    </FuelMixChartWrapper>
  );
}
