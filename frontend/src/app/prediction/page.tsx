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
  { key: "personality", title: "Personality", icon: "♈" },
  { key: "health", title: "Health", icon: "♋" },
  { key: "money", title: "Money", icon: "♉" },
  { key: "career", title: "Career", icon: "♑" },
  { key: "love", title: "Love", icon: "♓" },
  { key: "miscellaneous", title: "Miscellaneous", icon: "✶" },
];

export default function PredictionPage() {
  const [activeCard, setActiveCard] = useState<CategoryKey | null>(null);
  const [data, setData] = useState<Record<string, string>>({});
  const [showQuote, setShowQuote] = useState(false);

  useEffect(() => {
    const cached = localStorage.getItem("prediction");
    if (cached) setData(JSON.parse(cached));

    // Trigger quote after thunder animation
    const timer = setTimeout(() => setShowQuote(true), 2200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="min-h-screen relative overflow-hidden bg-[#05030d] text-white">
      {/* 🌌 Cosmic background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_#2b1d5a,_transparent_60%)] opacity-70" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom,_#0f766e,_transparent_55%)] opacity-50" />

      {/* 🪔 PanditAI Header */}
      <div className="absolute top-6 left-1/2 -translate-x-1/2 z-20">
        <h1 className="text-2xl tracking-[0.35em] font-serif text-white/80">
          PanditAI
        </h1>
      </div>

      {/* MAIN CONTENT */}
      <div className="relative z-10 flex items-center justify-center min-h-screen px-6">
        {!activeCard ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10 max-w-6xl w-full">
            {categories.map((cat) => (
              <div
                key={cat.key}
                onClick={() => setActiveCard(cat.key)}
                className="group cursor-pointer"
              >
                <div
                  className="h-64 rounded-3xl backdrop-blur-xl
                  bg-white/10 border border-white/20
                  shadow-[0_0_30px_rgba(168,85,247,0.25)]
                  flex flex-col items-center justify-center
                  transition-all duration-500
                  group-hover:scale-105 group-hover:shadow-[0_0_45px_rgba(168,85,247,0.45)]"
                >
                  <div className="text-5xl mb-4 opacity-80">
                    {cat.icon}
                  </div>
                  <div className="text-xl tracking-widest font-serif">
                    {cat.title}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="max-w-3xl w-full animate-fadeInScale">
            <div
              className="rounded-[2.5rem] p-10
              backdrop-blur-2xl
              bg-gradient-to-br from-white/15 to-white/5
              border border-white/20
              shadow-[0_0_60px_rgba(168,85,247,0.4)]"
            >
              <h2 className="text-4xl font-serif text-center mb-6 tracking-wider">
                {categories.find(c => c.key === activeCard)?.title}
              </h2>

              <p className="text-lg leading-relaxed text-center opacity-90 whitespace-pre-line">
                {data[activeCard] || "The cosmos remains silent for now ."}
              </p>

              <div className="mt-10 flex justify-center">
                <button
                  onClick={() => setActiveCard(null)}
                  className="px-8 py-3 rounded-full
                    bg-white/10 border border-white/30
                    hover:bg-white hover:text-black
                    transition-all duration-300"
                >
                  ← Return to Oracles
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ⚡ Thunder Sweep */}
      <div className="absolute bottom-16 left-0 w-full h-[2px] overflow-hidden">
        <div className="thunder-line" />
      </div>

      {/* 📜 Quote */}
      {showQuote && (
        <div className="absolute bottom-6 w-full text-center px-4 animate-fadeIn">
          <p className="text-sm tracking-wide text-white/70 font-serif">
            Time is an unstoppable force. PanditAI helps you navigate its currents rather than fight them.
          </p>
        </div>
      )}

      {/* ✨ Animations */}
      <style jsx>{`
        .thunder-line {
          width: 120%;
          height: 2px;
          background: linear-gradient(
            90deg,
            transparent,
            #ffffff,
            #a855f7,
            #ffffff,
            transparent
          );
          animation: thunder 2s ease-in-out forwards;
        }

        @keyframes thunder {
          from {
            transform: translateX(-100%);
            opacity: 0;
          }
          to {
            transform: translateX(0%);
            opacity: 1;
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.85);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out forwards;
        }

        .animate-fadeInScale {
          animation: fadeInScale 0.6s ease-out;
        }
      `}</style>
    </div>
  );
}
