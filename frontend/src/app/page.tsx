"use client";

import { useEffect, useState, ReactNode } from "react";
import dynamic from "next/dynamic";
import { Download, AlertTriangle, Activity, Zap, Server } from "lucide-react";

// Dynamically import components to avoid SSR issues
const PlantMap = dynamic(() => import("../components/PlantMap"), { ssr: false });
const FuelMixChart = dynamic(() => import("../components/FuelMixChart"), { ssr: false });

const IntelligenceLabel = ({ children }: { children: ReactNode }) => (
  <span className="text-[10px] text-[#38BDF8] font-black uppercase tracking-[0.2em] mb-2 block glow-cyan-text">
    {children}
  </span>
);

export default function Home() {
  const [plants, setPlants] = useState(null);
  const [fuelMix, setFuelMix] = useState<any>(null);
  const [outages, setOutages] = useState<any[]>([]);
  const [intelligence, setIntelligence] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Add a small delay to ensure the layout has settled before triggering chart measurements
    const timer = setTimeout(() => setMounted(true), 100);
    
    const fetchData = async () => {
      try {
        const [plantsRes, mixRes, outagesRes, intRes] = await Promise.all([
          fetch("http://localhost:8000/api/plants").then(r => r.json()),
          fetch("http://localhost:8000/api/fuel-mix").then(r => r.json()),
          fetch("http://localhost:8000/api/outages").then(r => r.json()),
          fetch("http://localhost:8000/api/intelligence").then(r => r.json())
        ]);
        setPlants(plantsRes);
        setFuelMix(mixRes);
        setOutages(outagesRes);
        setIntelligence(intRes);
      } catch (error) {
        console.error("Failed to fetch live data, falling back to mock data...");
        // Mock Fallback
        setFuelMix({
          timestamp: new Date().toISOString(),
          mix: [
            { source: "Natural Gas", percentage: 40, category: "Brown" },
            { source: "Coal", percentage: 20, category: "Brown" },
            { source: "Nuclear", percentage: 18, category: "Green" },
            { source: "Wind", percentage: 12, category: "Green" }
          ],
          summary: { green_percentage: 30, brown_percentage: 70, carbon_intensity_gCO2_kWh: 400 }
        });
        setOutages([
          { id: "1", time: "10:00", region: "Mock Region", event: "Simulated Outage", impact_mw: 100, status: "Investigating", severity: "High" }
        ]);
        setIntelligence({
          insight_a: "Energy is the Foundation of Economic Growth—an unstable or carbon-heavy grid is a long-term risk to capital.",
          insight_b: "The Ministry of Power, Grid Operators (ISOs/RTOs), and utility companies manage the physical assets."
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    return () => clearTimeout(timer);
  }, []);

  const COLORS = ['#FCA5A5', '#9CA3AF', '#818CF8', '#A7F3D0', '#38BDF8', '#FCD34D', '#D1D5DB'];

  if (loading) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-[#030712] text-[#38BDF8]">
        <Activity className="h-8 w-8 animate-pulse mr-3" />
        <span className="text-lg font-medium tracking-widest">INITIALIZING REAL RAILS...</span>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#030712] text-slate-200 font-sans" suppressHydrationWarning>

      {/* 70% MAIN STAGE */}
      <div className="w-[70%] h-full relative border-r border-[#1F2937]">
        {/* Map Header Bar */}
        <div className="absolute top-0 left-0 right-0 z-[1000] flex items-center justify-between px-6 py-4 bg-[#030712]/90 backdrop-blur-md border-b border-[#1F2937]">
          <div className="flex items-center gap-3">
            <Zap className="h-6 w-6 text-[#38BDF8]" />
            <h1 className="text-lg font-extrabold tracking-wide text-white uppercase">
              <span className="text-[#38BDF8]">Real Rails </span> Energy Infrastructure Watchtower
            </h1>
            <span className="text-xs text-slate-400 ml-4 font-medium">Grid Health & Asset Intelligence</span>
          </div>
          <div className="flex items-center gap-3 px-4 py-2 bg-[#0B1117] border border-[#38BDF8]/50 rounded-md text-xs glow-cyan">
            <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span>
            <span className="text-[#38BDF8] font-bold tracking-widest">LIVE DATA FEED</span>
          </div>
        </div>

        {/* Map Container */}
        <div className="h-full w-full">
          <PlantMap plants={plants} />
        </div>
      </div>

      {/* 30% INTELLIGENCE SIDEBAR */}
      <div className="w-[30%] h-full flex flex-col bg-[#030712] border-l border-[#1F2937]">

        {/* Sticky Header */}
        <div className="sticky top-0 z-[100] p-6 pt-16 bg-[#030712]/95 backdrop-blur-md border-b border-[#1F2937]">
          <p className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold mb-1">Grid Intelligence Summary</p>
          <h1 className="text-xl font-bold text-white tracking-tight">Energy Sovereignty</h1>
        </div>

        {/* Scrollable Content Container */}
        <div className="flex-1 overflow-y-auto">
          {/* Section A: High-level Metric */}
          <div className="p-6 border-b border-[#1F2937] flex gap-4">
            <div className="flex-1 bg-[#0B1117] border border-[#1F2937] rounded-lg p-4 glow-cyan transition-all">
              <p className="text-xs text-slate-400 mb-1">Carbon Intensity</p>
              <div className="flex items-end gap-2">
                <span className="text-2xl font-bold text-[#38BDF8]">{fuelMix?.summary?.carbon_intensity_gCO2_kWh}</span>
                <span className="text-xs text-slate-500 mb-1">gCO₂/kWh</span>
              </div>
            </div>
            <div className="flex-1 bg-[#0B1117] border border-[#1F2937] rounded-lg p-4 transition-all">
              <p className="text-xs text-slate-400 mb-1">Green vs Brown</p>
              <div className="flex items-end gap-2">
                <span className="text-2xl font-bold text-[#A7F3D0]">{fuelMix?.summary?.green_percentage}%</span>
                <span className="text-xs text-slate-500 mb-1">/ {fuelMix?.summary?.brown_percentage}%</span>
              </div>
            </div>
          </div>

          {/* Section B & C: Intelligence */}
          <div className="p-6 border-b border-[#1F2937] space-y-6">
            <div>
              <IntelligenceLabel>Why This Matters</IntelligenceLabel>
              <p className="text-sm text-slate-300 leading-relaxed">{intelligence?.insight_a}</p>
            </div>
            <div>
              <IntelligenceLabel>Who Controls The Rail</IntelligenceLabel>
              <p className="text-sm text-slate-300 leading-relaxed">{intelligence?.insight_b}</p>
            </div>
          </div>

          {/* Section D: Fuel Mix Chart */}
          <div className="p-6 border-b border-[#1F2937]">
            <IntelligenceLabel>Current Fuel Mix</IntelligenceLabel>
            {mounted && fuelMix?.mix && (
              <FuelMixChart data={fuelMix.mix} colors={COLORS} />
            )}
            {/* Legend */}
            <div className="flex flex-wrap gap-2 mt-2">
              {fuelMix?.mix?.map((entry: any, index: number) => (
                <div key={entry.source} className="flex items-center gap-1.5 text-xs">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }}></div>
                  <span className="text-slate-400">{entry.source}</span>
                  <span className="text-white font-medium">{entry.percentage}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Section E: Outage Timeline */}
          <div className="p-6 flex-1 border-b border-[#1F2937]">
            <div className="flex items-center justify-between mb-4">
              <IntelligenceLabel>Outage Watchtower</IntelligenceLabel>
              <span className="text-[10px] bg-red-900/30 text-red-400 px-2 py-0.5 rounded border border-red-900/50">LIVE EVENT FEED</span>
            </div>
            <div className="space-y-3">
              {mounted && outages?.map((outage) => (
                <div key={outage.id} className="bg-[#0B1117] border border-[#1F2937] p-3 rounded-lg flex items-start gap-3">
                  <AlertTriangle className={`h-4 w-4 mt-0.5 ${outage.severity === 'High' ? 'text-red-400' : outage.severity === 'Medium' ? 'text-yellow-400' : 'text-slate-400'}`} />
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs font-bold text-white">{outage.region}</span>
                      <span className="text-[10px] text-slate-500">{outage.time}</span>
                    </div>
                    <p className="text-xs text-slate-400 mb-1">{outage.event}</p>
                    <div className="flex items-center gap-2 text-[10px]">
                      <span className="bg-[#1F2937] px-1.5 py-0.5 rounded text-slate-300">Impact: {outage.impact_mw} MW</span>
                      <span className={outage.status === 'Resolved' ? 'text-green-400' : 'text-orange-400'}>{outage.status}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Section F: Download Sample Data button */}
          <div className="p-6 mt-auto">
            <button className="w-full py-3 bg-[#0B1117] hover:bg-[#1F2937] border border-[#38BDF8]/30 hover:border-[#38BDF8] rounded-md flex items-center justify-center gap-2 text-[#38BDF8] transition-all group">
              <Download className="h-4 w-4 group-hover:animate-bounce" />
              <span className="text-xs font-semibold tracking-wider">DOWNLOAD SAMPLE DATA</span>
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}
