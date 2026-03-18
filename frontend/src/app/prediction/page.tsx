import PredictionClient from "@/components/client/PredictionClient";

export const metadata = {
  title: "Your Vedic Prediction | PanditAI",
  description:
    "Explore your personalized Vedic astrology insights powered by AI",
};

export default function PredictionPage() {
  return (
    <div className="min-h-screen relative bg-background text-foreground selection:bg-primary/20 flex flex-col">
      <PredictionClient />
    </div>
  );
}
