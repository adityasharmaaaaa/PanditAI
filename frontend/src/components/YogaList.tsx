"use client";

interface Yoga {
  name: string;
  description: string;
  planets?: string[];
  nature?: "Benefic" | "Malefic" | "Mixed";
}

interface YogaListProps {
  yogas?: Yoga[];
}

export default function YogaList({ yogas }: YogaListProps) {
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
        {yogas.map((yoga, idx) => (
          <div
            key={idx}
            className="group relative bg-[#1a1a1e] border border-white/10 rounded-2xl p-6 hover:bg-[#202025] transition-all duration-300 hover:scale-[1.02] hover:border-amber-500/30"
          >
            {/* Glow Effect */}
            <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />

            <div className="relative z-10">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-serif text-amber-100 font-medium tracking-wide">
                  {yoga.name}
                </h3>
                {yoga.nature && (
                  <span
                    className={`px-3 py-1 text-[10px] uppercase tracking-widest rounded-full border ${
                      yoga.nature === "Benefic"
                        ? "bg-green-500/10 border-green-500/30 text-green-300"
                        : yoga.nature === "Malefic"
                        ? "bg-red-500/10 border-red-500/30 text-red-300"
                        : "bg-blue-500/10 border-blue-500/30 text-blue-300"
                    }`}
                  >
                    {yoga.nature}
                  </span>
                )}
              </div>

              <p className="text-sm text-white/70 leading-relaxed mb-6">
                {yoga.description}
              </p>

              {yoga.planets && yoga.planets.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-auto">
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
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
