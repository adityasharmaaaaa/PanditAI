"use client";

import { useState } from "react";
import Link from "next/link";
import LocationAutocomplete from "@/components/LocationAutocomplete";

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

export default function MatchingPage() {
  // State for Two People
  const [p1, setP1] = useState<BirthDetails>({
    ...DEFAULT_DETAILS,
    name: "Person 1",
  });
  const [p2, setP2] = useState<BirthDetails>({
    ...DEFAULT_DETAILS,
    name: "Person 2",
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleMatch = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ p1, p2 }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("Matching Failed");
    } finally {
      setLoading(false);
    }
  };

  // Helper to update state
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
    <div className="min-h-screen bg-[#08080a] text-[#f5f5f7] font-sans selection:bg-rose-200/30">
      {/* Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_#1a0505,_transparent_70%)] opacity-60 pointer-events-none" />

      <header className="relative z-10 p-6 flex justify-between items-center max-w-6xl mx-auto">
        <Link href="/" className="text-white/40 hover:text-white transition">
          Home
        </Link>
        <h1 className="text-2xl font-serif text-rose-100 tracking-wide">
          MatchMaking{" "}
        </h1>
        <div className="w-10" />
      </header>

      <main className="relative z-10 max-w-6xl mx-auto p-4 md:p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 relative">
          {/* VS Badge */}
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-rose-500 rounded-full flex items-center justify-center font-bold text-black z-20 shadow-[0_0_20px_rgba(244,63,94,0.5)] md:flex hidden"></div>

          {/* Person 1 Form */}
          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
            <h2 className="text-rose-200/60 uppercase tracking-widest text-sm mb-6">
              Person One
            </h2>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Name"
                className="w-full bg-black/20 border border-white/10 rounded-lg p-3 focus:border-rose-500/50 outline-none"
                value={p1.name}
                onChange={(e) => updateP1("name", e.target.value)}
              />

              <div className="grid grid-cols-3 gap-2">
                <input
                  type="number"
                  placeholder="DD"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p1.day}
                  onChange={(e) => updateP1("day", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="MM"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p1.month}
                  onChange={(e) => updateP1("month", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="YYYY"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p1.year}
                  onChange={(e) => updateP1("year", parseInt(e.target.value))}
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  placeholder="HH"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p1.hour}
                  onChange={(e) => updateP1("hour", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="mm"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p1.minute}
                  onChange={(e) => updateP1("minute", parseInt(e.target.value))}
                />
              </div>

              {/* Location Autocomplete P1 */}
              <div className="relative">
                <LocationAutocomplete
                  onLocationSelect={handleLocationSelectP1}
                />
                <div className="absolute right-3 top-3 text-xs text-white/30 pointer-events-none">
                  {p1.latitude !== 0 ? "📍 Set" : ""}
                </div>
              </div>
            </div>
          </div>

          {/* Person 2 Form */}
          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-sm">
            <h2 className="text-blue-200/60 uppercase tracking-widest text-sm mb-6">
              Person Two
            </h2>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Name"
                className="w-full bg-black/20 border border-white/10 rounded-lg p-3 focus:border-blue-500/50 outline-none"
                value={p2.name}
                onChange={(e) => updateP2("name", e.target.value)}
              />

              <div className="grid grid-cols-3 gap-2">
                <input
                  type="number"
                  placeholder="DD"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p2.day}
                  onChange={(e) => updateP2("day", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="MM"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p2.month}
                  onChange={(e) => updateP2("month", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="YYYY"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p2.year}
                  onChange={(e) => updateP2("year", parseInt(e.target.value))}
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  placeholder="HH"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p2.hour}
                  onChange={(e) => updateP2("hour", parseInt(e.target.value))}
                />
                <input
                  type="number"
                  placeholder="mm"
                  className="bg-black/20 border border-white/10 rounded-lg p-3 outline-none"
                  value={p2.minute}
                  onChange={(e) => updateP2("minute", parseInt(e.target.value))}
                />
              </div>

              {/* Location Autocomplete P2 */}
              <div className="relative">
                <LocationAutocomplete
                  onLocationSelect={handleLocationSelectP2}
                />
                <div className="absolute right-3 top-3 text-xs text-white/30 pointer-events-none">
                  {p2.latitude !== 0 ? "📍 Set" : ""}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Action */}
        <div className="mt-12 text-center">
          <button
            onClick={handleMatch}
            disabled={loading}
            className="bg-gradient-to-r from-rose-500 to-orange-600 text-white px-10 py-4 rounded-full font-serif text-xl tracking-wide hover:scale-105 transition-transform shadow-[0_0_40px_rgba(244,63,94,0.4)] disabled:opacity-50"
          >
            {loading ? "Analyzing Stars..." : "Calculate Compatibility"}
          </button>

          <div className="mt-4">
            <button
              onClick={() => {
                setP1({
                  name: "Rahul",
                  year: 1990,
                  month: 5,
                  day: 25,
                  hour: 14,
                  minute: 30,
                  latitude: 28.61,
                  longitude: 77.2,
                  timezone: 5.5,
                });
                setP2({
                  name: "Priya",
                  year: 1992,
                  month: 9,
                  day: 15,
                  hour: 10,
                  minute: 15,
                  latitude: 19.07,
                  longitude: 72.87,
                  timezone: 5.5,
                });
              }}
              className="text-xs text-white/30 hover:text-white transition underline"
            >
              Use Demo Data
            </button>
          </div>
        </div>

        {/* Results Area */}
        {result && (
          <div className="mt-16 animate-reveal">
            <div className="bg-white/[0.03] border border-white/10 rounded-3xl p-10 max-w-4xl mx-auto backdrop-blur-xl">
              <div className="flex flex-col md:flex-row gap-10 items-center justify-center mb-10">
                {/* Score Circle */}
                <div className="relative w-40 h-40 flex items-center justify-center">
                  <svg className="absolute inset-0 w-full h-full -rotate-90">
                    <circle
                      cx="80"
                      cy="80"
                      r="70"
                      stroke="currentColor"
                      strokeWidth="10"
                      className="text-white/10"
                      fill="transparent"
                    />
                    <circle
                      cx="80"
                      cy="80"
                      r="70"
                      stroke="currentColor"
                      strokeWidth="10"
                      className="text-rose-500"
                      fill="transparent"
                      strokeDasharray={440}
                      strokeDashoffset={
                        440 - (440 * (result.analysis?.score || 0)) / 36
                      }
                    />
                  </svg>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-white">
                      {result.analysis?.score}
                    </div>
                    <div className="text-xs text-white/50 uppercase tracking-widest mt-1">
                      {Math.round(((result.analysis?.score || 0) / 36) * 100)}%
                      Match
                    </div>
                  </div>
                </div>

                {/* Verdict */}
                <div className="flex-1">
                  <h3 className="text-2xl font-serif text-rose-200 mb-4">
                    The Verdict
                  </h3>
                  <p className="text-lg leading-relaxed text-white/80 whitespace-pre-line">
                    {result.ai_verdict}
                  </p>
                </div>
              </div>

              {/* Gunas Breakdown */}
              {result.analysis?.details && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 border-t border-white/10 pt-8">
                  {Object.entries(result.analysis.details).map(
                    ([key, val]: [string, any]) => (
                      <div
                        key={key}
                        className="bg-black/20 rounded-xl p-4 text-center"
                      >
                        <div className="text-xs text-white/40 uppercase mb-1">
                          {key}
                        </div>
                        <div className="font-bold text-rose-100">{val} pts</div>
                      </div>
                    )
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
