"use client";

import { useState, useEffect, useRef } from "react";

interface LocationSuggestion {
  display_name: string;
  lat: string;
  lon: string;
  type: string;
}

interface LocationAutocompleteProps {
  onLocationSelect: (location: {
    city: string;
    lat: number;
    lon: number;
  }) => void;
}

export default function LocationAutocomplete({
  onLocationSelect,
}: LocationAutocompleteProps) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<LocationSuggestion[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        wrapperRef.current &&
        !wrapperRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    if (query.length < 3) {
      setSuggestions([]);
      setIsOpen(false);
      return;
    }

    const timeoutId = setTimeout(async () => {
      setIsLoading(true);
      try {
        const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
          query
        )}&format=json&limit=5&addressdetails=1`;
        const response = await fetch(url, {
          headers: {
            "User-Agent": "PanditAI/1.0",
          },
        });
        const data = await response.json();
        setSuggestions(data);
        setIsOpen(data.length > 0);
      } catch (error) {
        console.error("Geocoding error:", error);
        setSuggestions([]);
      } finally {
        setIsLoading(false);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [query]);

  const handleSelect = (suggestion: LocationSuggestion) => {
    setQuery(suggestion.display_name);
    setIsOpen(false);
    onLocationSelect({
      city: suggestion.display_name,
      lat: parseFloat(suggestion.lat),
      lon: parseFloat(suggestion.lon),
    });
  };

  return (
    <div ref={wrapperRef} className="relative w-full">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Start typing city name..."
        aria-label="Location search"
        className="w-full px-4 py-2 rounded-[var(--radius)] bg-background border border-border text-foreground placeholder:text-muted-foreground focus-ring"
      />

      {isLoading && (
        <div className="absolute right-2 top-2">
          <div className="w-4 h-4 border-2 border-primary/50 border-t-transparent rounded-[var(--radius)] animate-spin"></div>
        </div>
      )}

      {isOpen && suggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-2 max-h-60 overflow-y-auto rounded-[var(--radius)] bg-card border border-border shadow-[var(--shadow-elev)]">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleSelect(suggestion)}
              className="w-full px-4 py-2 text-left hover:bg-background border-b border-border last:border-b-0 transition-colors"
            >
              <div className="type-sm text-foreground">
                {suggestion.display_name}
              </div>
              <div className="type-sm text-muted-foreground mt-2">
                {suggestion.type} - {parseFloat(suggestion.lat).toFixed(4)},{" "}
                {parseFloat(suggestion.lon).toFixed(4)}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
