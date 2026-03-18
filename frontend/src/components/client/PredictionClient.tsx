"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  IconBriefcase,
  IconCompass,
  IconCrown,
  IconDashboard,
  IconHeart,
  IconHourglass,
  IconMessage,
  IconSparkles,
  IconWallet,
} from "@/components/icons/PanditIcons";
import ChartViewer from "@/components/client/ChartViewer";
import TimelineViewer from "@/components/client/TimelineViewer";
import YogaList from "@/components/client/YogaList";
import AstrologerChat from "@/components/client/AstrologerChat";

export default function PredictionClient() {
  const [data, setData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("analysis");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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
  }, []);

  const tabs = [
    { id: "analysis", label: "Analysis", icon: IconDashboard },
    { id: "charts", label: "Charts", icon: IconCompass },
    { id: "timeline", label: "Timeline", icon: IconHourglass },
    { id: "yogas", label: "Yogas", icon: IconCrown },
    { id: "chat", label: "Chat", icon: IconMessage },
  ];

  const dominantKey =
    data?.ai_reading?.meta?.dominant_category?.toLowerCase() || "career";

  return (
    <>
      <header className="relative z-20 pt-6 px-6 pb-4 border-b border-border bg-background sticky top-0">
        <div className="max-w-7xl mx-auto flex justify-between items-center mb-4 type-sm uppercase tracking-widest text-muted-foreground">
          <div className="flex gap-4">
            <Link href="/" className="focus-ring transition-colors hover:text-foreground">
              Home
            </Link>
            <Link
              href="/matching"
              className="focus-ring transition-colors hover:text-foreground"
            >
              Matchmaking
            </Link>
          </div>
        </div>

        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-center md:text-left">
            <div className="type-sm tracking-widest uppercase text-muted-foreground">
              PanditAI
            </div>
            <div className="type-lg font-heading text-foreground">
              Vedic Life Architect
            </div>
          </div>

          <div className="group relative flex items-center gap-4 bg-card rounded-[var(--radius)] px-4 py-2 border border-border shadow-[var(--shadow-subtle)]">
            <div className="text-right">
              <div className="type-sm uppercase tracking-widest text-muted-foreground">
                Destiny Score
              </div>
              <div className="type-lg font-semibold text-primary">
                {data?.meta ? data.meta.destiny_score : "--"}/100
              </div>
            </div>
            <div className="h-10 w-10 rounded-[var(--radius)] border border-border flex items-center justify-center text-primary bg-background">
              <IconCrown size={20} />
            </div>

            <div className="absolute top-full mt-2 right-0 w-64 p-4 bg-popover border border-border rounded-[var(--radius)] shadow-[var(--shadow-elev)] opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50 type-sm text-muted-foreground">
              <p>
                <strong className="text-primary block mb-2">
                  Vedic Strength Index
                </strong>
                Aggregated score based on planetary strengths, benefic aspects,
                and Raja Yogas in your birth chart.
              </p>
            </div>
          </div>
        </div>
      </header>

      <nav
        className="max-w-7xl mx-auto px-6 mt-6 flex gap-4 overflow-x-auto pb-2 border-b border-border"
        role="tablist"
        aria-label="Prediction sections"
      >
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={isActive}
              aria-controls={`panel-${tab.id}`}
              id={`tab-${tab.id}`}
              onClick={() => setActiveTab(tab.id)}
              className={`focus-ring relative px-2 py-2 type-sm uppercase tracking-widest transition-colors flex items-center gap-2 ${
                isActive
                  ? "text-primary font-semibold"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Icon size={16} />
              {tab.label}
              {isActive && (
                <div className="absolute bottom-0 left-0 w-full h-px bg-primary" />
              )}
            </button>
          );
        })}
      </nav>

      <main className="relative z-10 flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-7xl mx-auto min-h-[500px]">
          {activeTab === "analysis" && (
            <section
              id="panel-analysis"
              role="tabpanel"
              aria-labelledby="tab-analysis"
              className="space-y-6"
            >
              <div className="text-center space-y-2">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-[var(--radius)] bg-primary/10 border border-primary/20 text-primary type-sm tracking-widest uppercase font-semibold">
                  <span className="w-2 h-2 rounded-[var(--radius)] bg-primary" />
                  Key Focus
                </div>
                {loading ? (
                  <div className="max-w-3xl mx-auto space-y-2">
                    <div className="skeleton h-6 w-full" />
                    <div className="skeleton h-6 w-4/5 mx-auto" />
                  </div>
                ) : (
                  <p className="type-xl text-foreground max-w-4xl mx-auto">
                    {data?.ai_reading?.meta?.insight ? (
                      <span>"{data.ai_reading.meta.insight}"</span>
                    ) : (
                      <span>
                        "Your <span className="text-primary">cosmic energy</span>{" "}
                        is shifting, bringing new opportunities for growth."
                      </span>
                    )}
                  </p>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {(loading
                  ? Array.from({ length: 6 }).map((_, idx) => (
                      <div
                        key={`skeleton-${idx}`}
                        className="rounded-[var(--radius)] border border-border p-4 bg-card shadow-[var(--shadow-subtle)] space-y-4"
                      >
                        <div className="skeleton h-10 w-10" />
                        <div className="space-y-2">
                          <div className="skeleton h-4 w-2/3" />
                    <div className="skeleton h-4 w-1/2" />
                        </div>
                      </div>
                    ))
                  : [
                      {
                        key: "personality",
                        title: "Personality",
                        desc: "Inner Self and Ego",
                        icon: <IconSparkles size={20} />,
                      },
                      {
                        key: "health",
                        title: "Health",
                        desc: "Vitality and Wellness",
                        icon: <IconHeart size={20} />,
                      },
                      {
                        key: "money",
                        title: "Money",
                        desc: "Wealth and Assets",
                        icon: <IconWallet size={20} />,
                      },
                      {
                        key: "career",
                        title: "Career",
                        desc: "Purpose and Status",
                        icon: <IconBriefcase size={20} />,
                      },
                      {
                        key: "love",
                        title: "Love",
                        desc: "Relationships",
                        icon: <IconHeart size={20} />,
                      },
                      {
                        key: "miscellaneous",
                        title: "Miscellaneous",
                        desc: "Travel and Spirituality",
                        icon: <IconSparkles size={20} />,
                      },
                    ].map((cat) => {
                      const isDominant = cat.key === dominantKey;
                      return (
                        <Link
                          key={cat.key}
                          href={`/prediction/${cat.key}`}
                          className={`focus-ring group relative block p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-subtle)] transition-shadow ${
                            isDominant ? "border-primary/30" : ""
                          } hover:shadow-[var(--shadow-elev)]`}
                        >
                          {isDominant && (
                            <div className="absolute top-2 right-2 type-sm uppercase tracking-widest text-primary font-semibold border border-primary/20 px-2 py-2 rounded-[var(--radius)] bg-primary/10">
                              Dominant
                            </div>
                          )}

                          <div className="flex flex-col items-center gap-2 text-center">
                            <div
                              className={`p-2 rounded-[var(--radius)] border border-border text-muted-foreground ${
                                isDominant ? "text-primary bg-primary/10" : ""
                              }`}
                            >
                              {cat.icon}
                            </div>
                            <div className="space-y-2">
                              <h3 className="type-sm uppercase tracking-widest text-foreground font-semibold">
                                {cat.title}
                              </h3>
                              <p className="type-sm text-muted-foreground">
                                {cat.desc}
                              </p>
                            </div>
                          </div>
                        </Link>
                      );
                    }))}
              </div>
            </section>
          )}

          {activeTab === "charts" && (
            <section
              id="panel-charts"
              role="tabpanel"
              aria-labelledby="tab-charts"
            >
              <ChartViewer />
            </section>
          )}

          {activeTab === "timeline" && (
            <section
              id="panel-timeline"
              role="tabpanel"
              aria-labelledby="tab-timeline"
            >
              <TimelineViewer timeline={data?.dasha?.timeline} />
            </section>
          )}

          {activeTab === "yogas" && (
            <section
              id="panel-yogas"
              role="tabpanel"
              aria-labelledby="tab-yogas"
            >
              <YogaList yogas={data?.yogas} />
            </section>
          )}

          {activeTab === "chat" && (
            <section
              id="panel-chat"
              role="tabpanel"
              aria-labelledby="tab-chat"
            >
              <AstrologerChat context={data?.meta?.fact_sheet} />
            </section>
          )}
        </div>
      </main>
    </>
  );
}
