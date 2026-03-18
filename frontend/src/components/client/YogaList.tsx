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
      <div className="h-64 flex flex-col items-center justify-center text-muted-foreground type-sm">
        No major yogas found in this chart.
      </div>
    );
  }

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {yogas.map((yoga, idx) => {
          const isExpanded = expandedIndex === idx;

          return (
            <div
              key={idx}
              className={`relative p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-subtle)] transition-colors ${
                isExpanded ? "border-primary/20" : "hover:border-primary/20"
              }`}
            >
              <div className="flex justify-between items-start mb-2 gap-2">
                <h3 className="type-lg font-heading text-foreground">
                  {yoga.name}
                </h3>
                {yoga.category && (
                  <span className="px-2 py-2 type-sm uppercase tracking-widest rounded-[var(--radius)] border border-border text-muted-foreground bg-background">
                    {yoga.category}
                  </span>
                )}
              </div>

              {yoga.planets && yoga.planets.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {yoga.planets.map((p, pIdx) => (
                    <span
                      key={pIdx}
                      className="type-sm text-muted-foreground bg-background border border-border px-2 py-2 rounded-[var(--radius)]"
                    >
                      {p}
                    </span>
                  ))}
                </div>
              )}

              <button
                type="button"
                onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                className="focus-ring type-sm uppercase tracking-widest text-primary font-semibold"
                aria-expanded={isExpanded}
                aria-controls={`yoga-desc-${idx}`}
              >
                {isExpanded ? "Hide meaning" : "See meaning"}
              </button>

              <div
                id={`yoga-desc-${idx}`}
                className={`grid transition-[grid-template-rows,opacity] duration-200 ${
                  isExpanded
                    ? "grid-rows-[1fr] opacity-100 mt-4"
                    : "grid-rows-[0fr] opacity-0"
                }`}
              >
                <div className="overflow-hidden">
                  <div className="p-4 bg-background rounded-[var(--radius)] border border-border">
                    <p className="type-sm text-foreground leading-relaxed">
                      "{yoga.desc}"
                    </p>
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
