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
      <div className="h-64 flex items-center justify-center type-sm text-muted-foreground">
        No timeline data available.
      </div>
    );
  }

  const toggleExpand = (idx: string) => {
    setExpanded(expanded === idx ? null : idx);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="relative border-l border-border ml-4 space-y-4 py-4">
        {timeline.map((period, idx) => {
          const isCurrent =
            new Date(period.start) <= new Date() &&
            new Date(period.end) >= new Date();

          return (
            <div key={idx} className="relative pl-4">
              <div
                className={`absolute -left-2 top-2 w-2 h-2 rounded-[var(--radius)] border ${
                  isCurrent
                    ? "bg-primary border-primary"
                    : "bg-background border-border"
                }`}
              />

              <button
                type="button"
                onClick={() => toggleExpand(`${idx}`)}
                className={`w-full text-left p-4 rounded-[var(--radius)] border transition-colors focus-ring ${
                  isCurrent
                    ? "bg-primary/5 border-primary/20"
                    : "bg-card border-border hover:border-primary/20"
                }`}
                aria-expanded={expanded === `${idx}`}
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2 mb-2">
                  <h3 className="type-lg font-heading text-foreground">
                    {period.lord} Mahadasha
                  </h3>
                  <span className="type-sm text-muted-foreground uppercase tracking-widest">
                    {period.start} - {period.end}
                  </span>
                </div>

                {isCurrent && (
                  <div className="type-sm font-semibold text-primary mb-2">
                    Currently active
                  </div>
                )}

                <div
                  className={`overflow-hidden transition-[max-height,opacity] duration-200 ${
                    expanded === `${idx}`
                      ? "max-h-96 opacity-100 mt-2"
                      : "max-h-0 opacity-0"
                  }`}
                >
                  <div className="space-y-2 pl-4 border-l border-border">
                    {period.sub_periods?.map((sub, sIdx) => (
                      <div key={sIdx} className="flex justify-between type-sm">
                        <span className="text-foreground">{sub.lord}</span>
                        <span className="text-muted-foreground">
                          {sub.end}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="text-center mt-2 type-sm text-muted-foreground">
                  {expanded === `${idx}` ? "Collapse" : "View antardashas"}
                </div>
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
