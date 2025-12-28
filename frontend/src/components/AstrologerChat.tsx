"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatProps {
  context?: string;
}

export default function AstrologerChat({ context }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Namaste. I have analyzed your chart. Ask me anything about your career, relationships, destiny and how to make it better.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, newMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: newMsg.content,
          context: context || "No context available.",
        }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I am having trouble connecting to the cosmos right now. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[600px] flex flex-col rounded-3xl border border-white/10 bg-white/[0.02] backdrop-blur-md overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-white/5 bg-white/5 flex items-center gap-3">
        <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse" />
        <span className="font-serif text-amber-100 tracking-wide">
          PanditAI Interaction Mode
        </span>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-amber-600/20 text-white rounded-br-none border border-amber-500/30"
                  : "bg-white/10 text-white/90 rounded-bl-none border border-white/10"
              }`}
            >
              <span className="font-bold block mb-1 text-xs opacity-50 uppercase tracking-wider">
                {m.role === "user" ? "You" : "PanditAI"}
              </span>
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white/5 p-4 rounded-2xl rounded-bl-none text-white/50 text-sm animate-pulse">
              Consulting the stars...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-white/5 bg-white/[0.02]">
        <div className="flex gap-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask about your Dasha, compatibility, or career..."
            className="flex-1 bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-amber-200/50 transition-colors"
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="px-6 py-3 bg-amber-600/20 hover:bg-amber-600/40 text-amber-200 rounded-xl border border-amber-500/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send ➢
          </button>
        </div>
      </div>
    </div>
  );
}
