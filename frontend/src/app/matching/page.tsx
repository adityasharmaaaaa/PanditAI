import { Metadata } from "next";
import MatchingClient from "@/components/client/MatchingClient";

export const metadata: Metadata = {
  title: "Love Compatibility | PanditAI",
  description:
    "Check astrological compatibility between two individuals using Vedic methodology.",
};

export default function MatchingPage() {
  return <MatchingClient />;
}
