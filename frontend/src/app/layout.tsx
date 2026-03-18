import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: "PanditAI",
    template: "%s | PanditAI",
  },
  description:
    "Personalized Vedic astrology insights with clear, actionable guidance.",
  openGraph: {
    title: "PanditAI",
    description:
      "Personalized Vedic astrology insights with clear, actionable guidance.",
    type: "website",
    images: [
      {
        url: "/og-image.svg",
        width: 1200,
        height: 630,
        alt: "PanditAI",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "PanditAI",
    description:
      "Personalized Vedic astrology insights with clear, actionable guidance.",
    images: ["/og-image.svg"],
  },
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`}>{children}</body>
    </html>
  );
}
