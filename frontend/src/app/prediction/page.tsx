"use client";

import { useEffect, useState } from "react";

type CategoryKey =
  | "personality"
  | "health"
  | "money"
  | "career"
  | "love"
  | "miscellaneous";

const categories: { key: CategoryKey; title: string; icon: string }[] = [
  { key: "personality", title: "Personality", icon: "✧" },
  { key: "health", title: "Health", icon: "⚖" },
  { key: "money", title: "Wealth", icon: "◈" },
  { key: "career", title: "Purpose", icon: "⌬" },
  { key: "love", title: "Affinity", icon: "❦" },
  { key: "miscellaneous", title: "Ethereal", icon: "✶" },
];

export default function PredictionPage() {
  const [activeCard, setActiveCard] = useState<CategoryKey | null>(null);
  const [data, setData] = useState<Record<string, string>>({});
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const cached = localStorage.getItem("prediction");
    if (cached) setData(JSON.parse(cached));
    setIsLoaded(true);
  }, []);

  return (
    <div className="min-h-screen relative overflow-hidden bg-[#08080a] text-[#f5f5f7] font-sans selection:bg-amber-200/30">
      {/* 🌌 Refined Atmospheric Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_-20%,_#1a1a2e,_transparent_70%)] opacity-40" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom,_#0d0d0d,_transparent_50%)]" />

      {/* 🏛️ Minimalist Header */}
      <header className="absolute top-12 left-0 w-full z-20 flex flex-col items-center">
        <h1 className="text-sm tracking-[0.6em] font-light uppercase text-white/40 mb-2">
          The Oracle of
        </h1>
        <div className="h-px w-12 bg-gradient-to-r from-transparent via-amber-200/40 to-transparent" />
      </header>

      {/* MAIN CONTENT */}
      <main className="relative z-10 flex items-center justify-center min-h-screen px-8 pt-20">
        {!activeCard ? (
          <div
            className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl w-full transition-all duration-1000 ${
              isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
            }`}
          >
            {categories.map((cat) => (
              <button
                key={cat.key}
                onClick={() => setActiveCard(cat.key)}
                className="group relative text-left outline-none"
              >
                <div className="absolute inset-0 bg-amber-200/5 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
                <div className="relative h-56 p-8 rounded-2xl border border-white/5 bg-white/[0.02] backdrop-blur-sm flex flex-col justify-between transition-all duration-500 group-hover:border-amber-200/20 group-hover:-translate-y-1">
                  <span className="text-3xl font-light text-amber-100/40 group-hover:text-amber-100/80 transition-colors duration-500">
                    {cat.icon}
                  </span>
                  <div>
                    <h3 className="text-lg font-serif tracking-widest text-white/80 group-hover:text-white transition-colors duration-500">
                      {cat.title}
                    </h3>
                    <div className="h-px w-0 bg-amber-200/30 mt-2 transition-all duration-700 group-hover:w-full" />
                  </div>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="max-w-2xl w-full animate-reveal">
            <div className="relative p-12 rounded-3xl border border-white/10 bg-white/[0.01] backdrop-blur-3xl shadow-2xl">
              <div className="absolute -top-6 left-1/2 -translate-x-1/2 px-6 py-2 bg-[#08080a] border border-white/10 rounded-full">
                <span className="text-xs tracking-[0.4em] uppercase text-amber-200/60">
                  {categories.find((c) => c.key === activeCard)?.title}
                </span>
              </div>

              <div className="space-y-8">
                <p className="text-xl font-serif leading-relaxed text-white/90 text-center first-letter:text-3xl first-letter:font-light">
                  {data[activeCard] ||
                    "The celestial alignment is currently obscured. Seek clarity within and return when the moon is high."}
                </p>

                <div className="flex justify-center pt-8">
                  <button
                    onClick={() => setActiveCard(null)}
                    className="group flex items-center gap-3 text-xs tracking-[0.3em] uppercase text-white/40 hover:text-amber-200 transition-colors duration-300"
                  >
                    <span className="h-px w-8 bg-white/20 group-hover:bg-amber-200/40 transition-all" />
                    Return to Oracles
                    <span className="h-px w-8 bg-white/20 group-hover:bg-amber-200/40 transition-all" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* 🕯️ Subtle Footer Detail */}
      <footer className="absolute bottom-12 w-full text-center px-4">
        <p className="text-[10px] tracking-[0.5em] uppercase text-white/20 font-light">
          Wisdom is the silent language of the stars
        </p>
      </footer>

      <style jsx>{`
        @keyframes reveal {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.98);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
        .animate-reveal {
          animation: reveal 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
      `}</style>
    </div>
  );
}
