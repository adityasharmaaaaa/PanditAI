"use client";

import { useState } from "react";
import LocationAutocomplete from "@/components/LocationAutocomplete";

export default function Home() {
  const [formData, setFormData] = useState({
    dob: "2005-08-20",
    time: "8:24",
    city: "Delhi",
    lat: 28.6139,
    lon: 77.209,
    ayanamsa: "lahiri",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleLocationSelect = (location: {
    city: string;
    lat: number;
    lon: number;
  }) => {
    setFormData((prev) => ({
      ...prev,
      city: location.city,
      lat: location.lat,
      lon: location.lon,
    }));
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      // Parse date and time from form inputs
      const date = new Date(formData.dob);
      const [hours, minutes] = formData.time.split(":").map(Number);

      // Prepare request payload for backend
      const payload = {
        year: date.getFullYear(),
        month: date.getMonth() + 1, // JavaScript months are 0-indexed
        day: date.getDate(),
        hour: hours,
        minute: minutes,
        timezone: 5.5, // Default to IST (India Standard Time)
        latitude: formData.lat,
        longitude: formData.lon,
        ayanamsa: formData.ayanamsa.toUpperCase(),
      };

      console.log("Sending to backend:", payload);

      // Call backend API
      const response = await fetch("http://localhost:8000/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      console.log("Backend response:", data);

      // Store full prediction data (includes meta.destiny_score, charts, etc.)
      if (data) {
        localStorage.setItem("prediction", JSON.stringify(data));
        localStorage.setItem("birth_details", JSON.stringify(payload));
        window.location.href = "/prediction";
      } else {
        setError("No prediction data received from the server");
      }
    } catch (err: any) {
      setError(err.message || "Failed to generate horoscope");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col relative overflow-hidden">
      {/* Decorative Gold Glows */}
      <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] bg-[#ff8c42]/20 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-[#ffd700]/30 rounded-full blur-[100px] pointer-events-none" />

      <main className="flex-1 flex flex-col lg:flex-row items-center justify-center p-6 lg:p-24 gap-12 z-10">
        {/* Left: Hero Text */}
        <h2 className="text-5xl lg:text-7xl font-extrabold tracking-tight leading-tight">
          Welcome to <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#ff8c42] via-[#ffd700] to-[#ff8c42] animate-pulse">
            PanditAI
          </span>
        </h2>

        {/* New Feature Link */}
        <div className="pt-4">
          <a
            href="/matching"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-colors group"
          >
            <span className="text-rose-200 text-sm font-medium tracking-wider uppercase">
              Try Horoscope Matching
            </span>
          </a>
        </div>

        {/* Right: Form */}
        <div className="flex-1 w-full max-w-md">
          <div className="bg-white/5 backdrop-blur-xl border border-[#ff8c42]/20 rounded-lg shadow-2xl shadow-[#ff8c42]/10 p-8">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold mb-2">Enter Birth Details</h3>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="dob" className="block text-sm font-medium mb-2">
                  Date of Birth
                </label>
                <input
                  type="date"
                  id="dob"
                  required
                  value={formData.dob}
                  onChange={(e) =>
                    setFormData({ ...formData, dob: e.target.value })
                  }
                  className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label
                    htmlFor="time"
                    className="block text-sm font-medium mb-2"
                  >
                    Time
                  </label>
                  <input
                    type="time"
                    id="time"
                    required
                    value={formData.time}
                    onChange={(e) =>
                      setFormData({ ...formData, time: e.target.value })
                    }
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                  />
                </div>
                <div>
                  <label
                    htmlFor="ayanamsa"
                    className="block text-sm font-medium mb-2"
                  >
                    Ayanamsa
                  </label>
                  <select
                    id="ayanamsa"
                    value={formData.ayanamsa}
                    onChange={(e) =>
                      setFormData({ ...formData, ayanamsa: e.target.value })
                    }
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                  >
                    <option value="lahiri">Lahiri</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Birth Location
                </label>
                <LocationAutocomplete onLocationSelect={handleLocationSelect} />
                {formData.lat !== 0 && (
                  <div className="mt-2 text-xs text-gray-400">
                    📍 {formData.lat.toFixed(4)}°, {formData.lon.toFixed(4)}°
                  </div>
                )}
              </div>

              {error && (
                <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading || formData.lat === 0}
                className="w-full bg-gradient-to-r from-[#ff8c42] to-[#ff6b1a] hover:from-[#ff6b1a] hover:to-[#ff8c42] text-white font-bold py-4 text-lg rounded-lg mt-6 transition-all duration-500 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Generating..." : "Generate Horoscope"}
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
