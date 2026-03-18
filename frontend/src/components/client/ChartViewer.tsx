"use client";

import { useState, useEffect } from "react";

export default function ChartViewer() {
  const [d1Image, setD1Image] = useState<string | null>(null);
  const [d9Image, setD9Image] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchChart = async (style: "d1" | "d9", details: any) => {
    try {
      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/chart-image?style=${style}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(details),
      });
      if (res.ok) {
        const blob = await res.blob();
        return URL.createObjectURL(blob);
      }
    } catch (e) {
      console.error(`Failed to fetch ${style} chart`, e);
    }
    return null;
  };

  useEffect(() => {
    const loadCharts = async () => {
      const storedDetails = localStorage.getItem("birth_details");
      if (!storedDetails) {
        setLoading(false);
        return;
      }

      const details = JSON.parse(storedDetails);
      const [d1, d9] = await Promise.all([
        fetchChart("d1", details),
        fetchChart("d9", details),
      ]);

      setD1Image(d1);
      setD9Image(d9);
      setLoading(false);
    };

    loadCharts();
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Array.from({ length: 2 }).map((_, idx) => (
          <div
            key={`chart-skeleton-${idx}`}
            className="rounded-[var(--radius)] border border-border p-4 bg-card shadow-[var(--shadow-subtle)] space-y-4"
          >
            <div className="skeleton h-6 w-1/2" />
            <div className="skeleton h-64 w-full" />
            <div className="skeleton h-4 w-3/4" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="flex flex-col items-center p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-subtle)]">
        <h3 className="type-lg font-heading text-foreground mb-4">
          Lagna Chart (D1)
        </h3>
        {d1Image ? (
          <img
            src={d1Image}
            alt="Lagna chart"
            className="w-full max-w-sm rounded-[var(--radius)] border border-border shadow-[var(--shadow-subtle)]"
          />
        ) : (
          <div className="w-full h-64 bg-background rounded-[var(--radius)] border border-border flex items-center justify-center type-sm text-muted-foreground">
            Chart unavailable
          </div>
        )}
        <p className="type-sm text-muted-foreground mt-4 text-center">
          The primary birth chart representing your physical body and general
          destiny.
        </p>
      </div>

      <div className="flex flex-col items-center p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-subtle)]">
        <h3 className="type-lg font-heading text-foreground mb-4">
          Navamsa Chart (D9)
        </h3>
        {d9Image ? (
          <img
            src={d9Image}
            alt="Navamsa chart"
            className="w-full max-w-sm rounded-[var(--radius)] border border-border shadow-[var(--shadow-subtle)]"
          />
        ) : (
          <div className="w-full h-64 bg-background rounded-[var(--radius)] border border-border flex items-center justify-center type-sm text-muted-foreground">
            Chart unavailable
          </div>
        )}
        <p className="type-sm text-muted-foreground mt-4 text-center">
          The chart of the soul and internal strength, primarily used for
          marriage and karma.
        </p>
      </div>
    </div>
  );
}
