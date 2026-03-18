"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { IconArrowLeft } from "@/components/icons/PanditIcons";

type CategoryKey =
  | "personality"
  | "health"
  | "money"
  | "career"
  | "love"
  | "miscellaneous";

const categoryMeta: Record<CategoryKey, { title: string; image: string }> = {
  personality: { title: "Personality", image: "/personality-bg.webp" },
  health: { title: "Health", image: "/health.webp" },
  money: { title: "Money", image: "/money.webp" },
  career: { title: "Career", image: "/career.webp" },
  love: { title: "Love", image: "/love.webp" },
  miscellaneous: { title: "Miscellaneous", image: "/misc.webp" },
};

export default function AnalysisCategoryPage() {
  const params = useParams();
  const router = useRouter();
  const category = params.category as CategoryKey;
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!categoryMeta[category]) {
      router.push("/prediction");
      return;
    }

    const cached = localStorage.getItem("prediction");
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        setData(parsed);
      } catch (e) {
        console.error("Failed to parse prediction data", e);
      }
    }
    setLoading(false);
  }, [category, router]);

  const meta = categoryMeta[category];
  if (!meta) {
    return null;
  }
  const content =
    data?.ai_reading && typeof data.ai_reading === "object"
      ? data.ai_reading[category]
      : "No detailed analysis available for this section.";

  return (
    <div className="min-h-screen relative overflow-hidden bg-background text-foreground selection:bg-primary/20 flex flex-col">
      <header className="relative z-20 pt-6 px-6 pb-4 border-b border-border bg-background">
        <div className="absolute inset-0 pointer-events-none">
          <img
            src={meta.image}
            alt=""
            className="h-full w-full object-cover opacity-10"
          />
        </div>

        <div className="max-w-4xl mx-auto flex items-center gap-2 relative z-10">
          <Link
            href="/prediction"
            className="focus-ring inline-flex items-center justify-center h-10 w-10 rounded-[var(--radius)] border border-border text-muted-foreground hover:text-foreground"
            aria-label="Back to prediction overview"
          >
            <IconArrowLeft size={16} />
          </Link>
          <div className="flex-1">
            <h1 className="type-lg font-heading text-foreground">
              {meta.title} Analysis
            </h1>
            <p className="type-sm text-muted-foreground">
              Detailed guidance for this area of life.
            </p>
          </div>
        </div>
      </header>

      <main className="relative z-10 flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-card border border-border rounded-[var(--radius)] p-4 md:p-6 shadow-[var(--shadow-subtle)]">
            {loading ? (
              <div className="space-y-4">
                <div className="skeleton h-6 w-2/3" />
                <div className="skeleton h-4 w-full" />
                <div className="skeleton h-4 w-5/6" />
                <div className="skeleton h-4 w-4/6" />
              </div>
            ) : (
              <p className="type-md text-foreground whitespace-pre-line">
                {content}
              </p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
