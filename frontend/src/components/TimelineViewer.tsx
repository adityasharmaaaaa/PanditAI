"use client";

import { useState } from "react";

interface DashaPeriod {
  lord: string;
  start: string;
  end: string;
  type?: string;
  sub_periods?: DashaPeriod[];
}

interface TimelineProps {
  timeline?: DashaPeriod[];
}

export default function TimelineViewer({ timeline }: TimelineProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  if (!timeline || timeline.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-white/30">
        No timeline data available.
      </div>
    );
  }

  const toggleExpand = (idx: string) => {
    setExpanded(expanded === idx ? null : idx);
  };

  return (
    <div className="max-w-3xl mx-auto animate-reveal">
      <div className="relative border-l border-white/10 ml-4 space-y-8 py-4">
        {timeline.map((period, idx) => {
          const isCurrent =
            new Date(period.start) <= new Date() &&
            new Date(period.end) >= new Date();

          return (
            <div key={idx} className="relative pl-8">
              {/* Timeline Dot */}
              <div
                className={`absolute -left-[5px] top-2 w-2.5 h-2.5 rounded-full border-2 ${
                  isCurrent
                    ? "bg-amber-400 border-amber-400 shadow-[0_0_10px_#fbbf24] animate-pulse"
                    : "bg-black border-white/30"
                }`}
              />

              {/* Card */}
              <div
                className={`p-6 rounded-2xl border transition-all duration-300 cursor-pointer ${
                  isCurrent
                    ? "bg-amber-900/10 border-amber-500/30 shadow-lg"
                    : "bg-white/5 border-white/10 hover:bg-white/10"
                }`}
                onClick={() => toggleExpand(`${idx}`)}
              >
                <div className="flex justify-between items-center mb-2">
                  <h3
                    className={`text-xl font-serif ${
                      isCurrent ? "text-amber-200" : "text-white/90"
                    }`}
                  >
                    {period.lord} Mahadasha
                  </h3>
                  <span className="text-xs font-mono opacity-50 uppercase tracking-wider">
                    {period.start} — {period.end}
                  </span>
                </div>

                {isCurrent && (
                  <div className="text-xs font-bold text-amber-400 mb-2">
                    ● CURRENTLY ACTIVE
                  </div>
                )}

                {/* Sub-periods (Antardasha) */}
                <div
                  className={`overflow-hidden transition-all duration-500 ${
                    expanded === `${idx}`
                      ? "max-h-96 opacity-100 mt-4"
                      : "max-h-0 opacity-0"
                  }`}
                >
                  <div className="space-y-2 pl-4 border-l border-white/10">
                    {period.sub_periods?.map((sub, sIdx) => (
                      <div
                        key={sIdx}
                        className="flex justify-between text-sm py-1"
                      >
                        <span className="text-white/70">{sub.lord}</span>
                        <span className="text-white/30 font-mono text-xs">
                          {sub.end}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="text-center mt-2 opacity-30 text-xs">
                  {expanded === `${idx}` ? "Collapse ▲" : "View Antardashas ▼"}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
