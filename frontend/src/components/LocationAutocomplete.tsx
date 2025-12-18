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

  // Close dropdown when clicking outside
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

  // Fetch suggestions from Nominatim
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
    }, 500); // Debounce: wait 500ms after user stops typing

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
        className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
      />

      {isLoading && (
        <div className="absolute right-3 top-3">
          <div className="w-5 h-5 border-2 border-[#ff8c42] border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}

      {isOpen && suggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-gray-800 border border-white/20 rounded-lg shadow-2xl max-h-60 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSelect(suggestion)}
              className="w-full px-4 py-3 text-left hover:bg-[#ff8c42]/20 border-b border-white/10 last:border-b-0 transition-colors"
            >
              <div className="font-medium text-white">
                {suggestion.display_name}
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {suggestion.type} • {parseFloat(suggestion.lat).toFixed(4)},{" "}
                {parseFloat(suggestion.lon).toFixed(4)}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
