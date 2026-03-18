"use client";

import { useState } from "react";
import Link from "next/link";
import LocationAutocomplete from "@/components/client/LocationAutocomplete";

interface BirthDetails {
  name: string;
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  latitude: number;
  longitude: number;
  timezone: number;
}

const DEFAULT_DETAILS: BirthDetails = {
  name: "",
  year: 1995,
  month: 1,
  day: 1,
  hour: 12,
  minute: 0,
  latitude: 28.61,
  longitude: 77.2,
  timezone: 5.5,
};

export default function MatchingClient() {
  const [p1, setP1] = useState<BirthDetails>({
    ...DEFAULT_DETAILS,
    name: "Narendra Modi",
    year: 1950,
    month: 9,
    day: 17,
    hour: 11,
    minute: 0,
    latitude: 23.62,
    longitude: 72.47,
  });
  const [p2, setP2] = useState<BirthDetails>({
    ...DEFAULT_DETAILS,
    name: "Giorgia Meloni",
    year: 1977,
    month: 1,
    day: 15,
    hour: 18,
    minute: 30,
    latitude: 41.9,
    longitude: 12.49,
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleMatch = async () => {
    setLoading(true);
    try {
      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ p1, p2 }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("Matching failed");
    } finally {
      setLoading(false);
    }
  };

  const updateP1 = (field: keyof BirthDetails, val: any) =>
    setP1((prev) => ({ ...prev, [field]: val }));
  const updateP2 = (field: keyof BirthDetails, val: any) =>
    setP2((prev) => ({ ...prev, [field]: val }));

  const handleLocationSelectP1 = (loc: {
    city: string;
    lat: number;
    lon: number;
  }) => {
    setP1((prev) => ({ ...prev, latitude: loc.lat, longitude: loc.lon }));
  };

  const handleLocationSelectP2 = (loc: {
    city: string;
    lat: number;
    lon: number;
  }) => {
    setP2((prev) => ({ ...prev, latitude: loc.lat, longitude: loc.lon }));
  };

  return (
    <div className="relative flex flex-col min-h-screen w-full bg-background text-foreground selection:bg-primary/20">
      <header className="sticky top-0 z-20 border-b border-border bg-background">
        <div className="flex items-center justify-between h-16 max-w-6xl mx-auto px-6">
          <Link
            href="/"
            className="type-sm text-muted-foreground hover:text-foreground focus-ring"
          >
            Back home
          </Link>
          <h1 className="type-lg font-heading text-foreground">
            Compatibility Check
          </h1>
          <div className="w-12" />
        </div>
      </header>

      <main className="relative z-10 max-w-6xl mx-auto p-6 md:p-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <section className="p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-subtle)]">
            <h2 className="type-sm uppercase tracking-widest text-muted-foreground mb-4">
              First person
            </h2>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Full name"
                aria-label="First person full name"
                className="w-full px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                value={p1.name}
                onChange={(e) => updateP1("name", e.target.value)}
              />
              <div className="grid grid-cols-3 gap-4">
                <input
                  type="number"
                  placeholder="DD"
                  aria-label="First person day of birth"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p1.day}
                  onChange={(e) => updateP1("day", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="MM"
                  aria-label="First person month of birth"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p1.month}
                  onChange={(e) => updateP1("month", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="YYYY"
                  aria-label="First person year of birth"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p1.year}
                  onChange={(e) => updateP1("year", parseInt(e.target.value))}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="number"
                  placeholder="Hour"
                  aria-label="First person birth hour"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p1.hour}
                  onChange={(e) => updateP1("hour", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="Minute"
                  aria-label="First person birth minute"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p1.minute}
                  onChange={(e) => updateP1("minute", parseInt(e.target.value))}
                />
              </div>
              <LocationAutocomplete onLocationSelect={handleLocationSelectP1} />
            </div>
          </section>

          <section className="p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-subtle)]">
            <h2 className="type-sm uppercase tracking-widest text-muted-foreground mb-4">
              Second person
            </h2>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Full name"
                aria-label="Second person full name"
                className="w-full px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                value={p2.name}
                onChange={(e) => updateP2("name", e.target.value)}
              />
              <div className="grid grid-cols-3 gap-4">
                <input
                  type="number"
                  placeholder="DD"
                  aria-label="Second person day of birth"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p2.day}
                  onChange={(e) => updateP2("day", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="MM"
                  aria-label="Second person month of birth"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p2.month}
                  onChange={(e) => updateP2("month", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="YYYY"
                  aria-label="Second person year of birth"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p2.year}
                  onChange={(e) => updateP2("year", parseInt(e.target.value))}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="number"
                  placeholder="Hour"
                  aria-label="Second person birth hour"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p2.hour}
                  onChange={(e) => updateP2("hour", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="Minute"
                  aria-label="Second person birth minute"
                  className="px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] bg-background border border-border focus-ring"
                  value={p2.minute}
                  onChange={(e) => updateP2("minute", parseInt(e.target.value))}
                />
              </div>
              <LocationAutocomplete onLocationSelect={handleLocationSelectP2} />
            </div>
          </section>
        </div>

        <div className="flex flex-col items-center gap-4">
          <button
            onClick={handleMatch}
            disabled={loading}
            className="w-full md:w-auto px-6 py-2 type-md font-semibold text-white rounded-[var(--radius)] bg-primary hover:bg-primary/90 transition-colors disabled:opacity-50"
            aria-busy={loading}
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="animate-spin rounded-[var(--radius)] h-4 w-4 border-2 border-white/70 border-t-transparent"></span>
                Calculating alignment...
              </span>
            ) : (
              "Calculate match"
            )}
          </button>
        </div>

        {result && (
          <div className="mt-8 bg-card border border-border rounded-[var(--radius)] p-4 md:p-6 shadow-[var(--shadow-subtle)]">
            <div className="flex flex-col md:flex-row items-start gap-6 mb-6">
              <div className="shrink-0">
                <div className="w-24 h-24 rounded-[var(--radius)] border border-border flex items-center justify-center bg-background">
                  <div className="text-center">
                    <div className="type-xl font-heading text-primary">
                      {result.analysis?.score}
                    </div>
                    <div className="type-sm text-muted-foreground">
                      / 36 points
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex-1">
                <h3 className="type-lg font-heading mb-4 text-foreground">
                  Alignment report
                </h3>
                <div className="type-md text-muted-foreground space-y-4">
                  {result.ai_verdict
                    .split("\n")
                    .map((line: string, i: number) => {
                      const match = line.match(/^\*\s*\*\*(.*?)\*\*:\s*(.*)/);
                      if (match) {
                        const [_, key, value] = match;
                        return (
                          <div
                            key={i}
                            className="flex flex-col md:flex-row gap-2 md:gap-4 items-start"
                          >
                            <span className="text-foreground font-semibold shrink-0 md:w-32">
                              {key}:
                            </span>
                            <span>{value}</span>
                          </div>
                        );
                      }
                      if (!line.trim()) return <br key={i} />;
                      return <div key={i}>{line}</div>;
                    })}
                </div>
              </div>
            </div>

            {result.analysis?.details && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t border-border pt-4">
                {Object.entries(result.analysis.details).map(
                  ([key, val]: [string, any]) => (
                    <div
                      key={key}
                      className="bg-background border border-border rounded-[var(--radius)] p-4"
                    >
                      <div className="type-sm text-muted-foreground uppercase mb-2 tracking-widest">
                        {key}
                      </div>
                      <div className="type-lg font-heading text-foreground">
                        {val}{" "}
                        <span className="type-sm font-normal text-muted-foreground">
                          pts
                        </span>
                      </div>
                    </div>
                  )
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
