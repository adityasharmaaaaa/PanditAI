"use client";

import { useState, useRef, useEffect } from "react";
import { IconSend, IconSparkles, IconUser } from "@/components/icons/PanditIcons";

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
        "Namaste. I have analyzed your chart. Ask me about career, relationships, or your next steps.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const newMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, newMsg]);
    setInput("");
    setLoading(true);

    try {
      const API_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/chat`, {
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
            "The connection is faint right now. Please try again in a moment.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto h-[560px] flex flex-col rounded-[var(--radius)] border border-border bg-card shadow-[var(--shadow-elev)] overflow-hidden">
      <div className="p-4 border-b border-border bg-background flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-[var(--radius)] bg-primary/10 text-primary border border-primary/20">
            <IconSparkles size={16} />
          </div>
          <div>
            <h3 className="type-md font-heading text-foreground">PanditAI</h3>
            <div className="flex items-center gap-2 text-muted-foreground type-sm">
              <span className="inline-block w-2 h-2 rounded-[var(--radius)] bg-[var(--color-success)]" />
              Online
            </div>
          </div>
        </div>
      </div>

      <div
        ref={scrollRef}
        role="log"
        aria-live="polite"
        aria-busy={loading}
        className="flex-1 overflow-y-auto p-4 space-y-4"
      >
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-2 ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {m.role === "assistant" && (
              <div className="w-8 h-8 rounded-[var(--radius)] bg-background flex items-center justify-center border border-border flex-shrink-0">
                <IconSparkles size={14} />
              </div>
            )}

            <div
              className={`max-w-[75%] p-4 rounded-[var(--radius)] border type-sm ${
                m.role === "user"
                  ? "bg-primary text-white border-primary/30"
                  : "bg-background text-foreground border-border"
              }`}
            >
              {m.content}
            </div>

            {m.role === "user" && (
              <div className="w-8 h-8 rounded-[var(--radius)] bg-primary/10 flex items-center justify-center border border-primary/20 flex-shrink-0">
                <IconUser size={14} />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-2 items-center text-muted-foreground type-sm">
            <span className="inline-flex h-6 w-6 items-center justify-center rounded-[var(--radius)] border border-border bg-background">
              <span className="inline-block h-2 w-2 rounded-[var(--radius)] border-2 border-muted-foreground border-t-transparent animate-spin" />
            </span>
            PanditAI is thinking...
          </div>
        )}
      </div>

      <div className="p-4 border-t border-border bg-background">
        <div className="relative flex items-center gap-2">
          <label htmlFor="chat-input" className="sr-only">
            Ask a question
          </label>
          <input
            id="chat-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask a question..."
            className="w-full px-4 py-2 type-md text-foreground placeholder:text-muted-foreground rounded-[var(--radius)] border border-border bg-background focus-ring"
          />
          <button
            type="button"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="focus-ring inline-flex items-center justify-center h-10 w-10 rounded-[var(--radius)] border border-border bg-primary text-white transition-colors disabled:opacity-60"
            aria-label="Send message"
          >
            {loading ? (
              <span className="inline-block h-4 w-4 rounded-[var(--radius)] border-2 border-white/70 border-t-transparent animate-spin" />
            ) : (
              <IconSend size={16} />
            )}
          </button>
        </div>
        <p className="text-center mt-2 type-sm text-muted-foreground">
          AI can make mistakes. Verify important decisions.
        </p>
      </div>
    </div>
  );
}
