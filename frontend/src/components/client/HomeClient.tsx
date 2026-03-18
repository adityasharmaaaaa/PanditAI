"use client";

import { useState } from "react";
import LocationAutocomplete from "@/components/client/LocationAutocomplete";

export default function HomeClient() {
  const [formData, setFormData] = useState({
    dob: "2005-08-20",
    time: "08:24",
    city: "Delhi",
    lat: 28.6139,
    lon: 77.209,
    ayanamsa: "lahiri",
  });

  const [loading, setLoading] = useState(false);
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const date = new Date(formData.dob);
      const [hours, minutes] = formData.time.split(":").map(Number);

      const payload = {
        year: date.getFullYear(),
        month: date.getMonth() + 1,
        day: date.getDate(),
        hour: hours,
        minute: minutes,
        timezone: 5.5,
        latitude: formData.lat,
        longitude: formData.lon,
        ayanamsa: formData.ayanamsa.toUpperCase(),
      };

      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${API_URL}/calculate`, {
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
    <div className="flex-1 w-full max-w-md">
      <div className="relative p-4 rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-elev)]">
        <div className="relative z-10 mb-4 text-center">
          <h3 className="type-lg font-heading text-foreground">
            Enter Birth Details
          </h3>
        </div>

        <form onSubmit={handleSubmit} className="relative z-10 space-y-4">
          <div>
            <label
              htmlFor="dob"
              className="block mb-2 type-sm text-muted-foreground uppercase tracking-widest"
            >
              Date of birth
            </label>
            <input
              type="date"
              id="dob"
              required
              value={formData.dob}
              onChange={(e) =>
                setFormData({ ...formData, dob: e.target.value })
              }
              className="w-full px-4 py-2 rounded-[var(--radius)] bg-background border border-border text-foreground focus-ring"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label
                htmlFor="time"
                className="block mb-2 type-sm text-muted-foreground uppercase tracking-widest"
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
                className="w-full px-4 py-2 rounded-[var(--radius)] bg-background border border-border text-foreground focus-ring"
              />
            </div>
            <div>
              <label
                htmlFor="ayanamsa"
                className="block mb-2 type-sm text-muted-foreground uppercase tracking-widest"
              >
                Ayanamsa
              </label>
              <select
                id="ayanamsa"
                value={formData.ayanamsa}
                onChange={(e) =>
                  setFormData({ ...formData, ayanamsa: e.target.value })
                }
                className="w-full px-4 py-2 rounded-[var(--radius)] bg-background border border-border text-foreground focus-ring"
              >
                <option value="lahiri">Lahiri</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block mb-2 type-sm text-muted-foreground uppercase tracking-widest">
              Birth location
            </label>

            <LocationAutocomplete onLocationSelect={handleLocationSelect} />
            {formData.lat !== 0 && (
              <div className="mt-2 type-sm text-muted-foreground">
                Location: {formData.city} ({formData.lat.toFixed(2)} deg,{" "}
                {formData.lon.toFixed(2)} deg)
              </div>
            )}
          </div>

          {error && (
            <div className="p-2 bg-destructive/10 border border-destructive/20 rounded-[var(--radius)] type-sm text-destructive">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || formData.lat === 0}
            className="w-full py-2 mt-2 type-md font-semibold text-white rounded-[var(--radius)] bg-primary hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            aria-busy={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin rounded-[var(--radius)] h-4 w-4 border-2 border-white/70 border-t-transparent"></span>
                Aligning stars...
              </span>
            ) : (
              "Reveal your destiny"
            )}
          </button>
        </form>
      </div>

      <div className="mt-4 text-center">
        <a
          href="/matching"
          className="focus-ring inline-flex items-center gap-2 px-4 py-2 rounded-[var(--radius)] border border-border text-muted-foreground hover:text-foreground"
        >
          Love compatibility check
        </a>
      </div>
    </div>
  );
}
