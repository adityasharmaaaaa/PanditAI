"use client";

import { useState } from "react";

interface Yoga {
  name: string;
  desc: string;
  category?: string;
  planets?: string[];
}

interface YogaListProps {
  yogas?: Yoga[];
}

export default function YogaList({ yogas }: YogaListProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (!yogas || yogas.length === 0) {
    return (
      <div className="h-64 flex flex-col items-center justify-center text-white/30 animate-pulse">
        <div className="text-4xl mb-4">🧘</div>
        <p>No major Yogas found in this chart.</p>
      </div>
    );
  }

  return (
    <div className="animate-reveal">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {yogas.map((yoga, idx) => {
          const isExpanded = expandedIndex === idx;

          return (
            <div
              key={idx}
              className={`group relative bg-[#1a1a1e] border border-white/10 rounded-2xl p-6 transition-all duration-300 hover:border-amber-500/30 ${
                isExpanded ? "bg-[#202025] scale-[1.02]" : "hover:bg-[#202025]"
              }`}
            >
              {/* Glow Effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />

              <div className="relative z-10">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-serif text-amber-100 font-medium tracking-wide">
                    {yoga.name}
                  </h3>
                  {yoga.category && (
                    <span
                      className={`px-3 py-1 text-[10px] uppercase tracking-widest rounded-full border ${
                        yoga.category === "Raja"
                          ? "bg-purple-500/10 border-purple-500/30 text-purple-300"
                          : yoga.category === "Mahapurusha"
                          ? "bg-amber-500/10 border-amber-500/30 text-amber-300"
                          : "bg-blue-500/10 border-blue-500/30 text-blue-300"
                      }`}
                    >
                      {yoga.category}
                    </span>
                  )}
                </div>

                {yoga.planets && yoga.planets.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {yoga.planets.map((p, pIdx) => (
                      <span
                        key={pIdx}
                        className="text-xs font-medium text-white/40 bg-white/5 px-2 py-1 rounded"
                      >
                        {p}
                      </span>
                    ))}
                  </div>
                )}

                {/* Dropdown Toggle */}
                <button
                  onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                  className="flex items-center gap-2 text-xs text-amber-200/70 hover:text-amber-200 transition-colors uppercase tracking-widest font-bold mt-2"
                >
                  {isExpanded ? (
                    <>
                      Hide Meaning <span className="text-[10px]">▲</span>
                    </>
                  ) : (
                    <>
                      See Meaning <span className="text-[10px]">▼</span>
                    </>
                  )}
                </button>

                {/* Expandable Content */}
                <div
                  className={`grid transition-all duration-300 ease-in-out ${
                    isExpanded
                      ? "grid-rows-[1fr] opacity-100 mt-4"
                      : "grid-rows-[0fr] opacity-0"
                  }`}
                >
                  <div className="overflow-hidden">
                    <div className="p-4 bg-black/20 rounded-lg border border-white/5">
                      <p className="text-sm text-white/80 leading-relaxed italic border-l-2 border-amber-500/50 pl-3">
                        "{yoga.desc}"
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
