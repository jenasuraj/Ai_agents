"use client";

import { useState, useEffect } from "react";
import Image from "next/image";

export default function Hero() {
  const [typedText, setTypedText] = useState("");
  const phrases = ["Autonomous Agents.", "Intelligent Pipelines.", "Zero-Limit AI."];
  const [phraseIdx, setPhraseIdx] = useState(0);
  const [charIdx, setCharIdx] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const phrase = phrases[phraseIdx];
    const timeout = setTimeout(() => {
      if (!deleting) {
        setTypedText(phrase.slice(0, charIdx + 1));
        if (charIdx + 1 === phrase.length) {
          setTimeout(() => setDeleting(true), 2000);
        } else {
          setCharIdx((c) => c + 1);
        }
      } else {
        setTypedText(phrase.slice(0, charIdx - 1));
        if (charIdx - 1 === 0) {
          setDeleting(false);
          setPhraseIdx((p) => (p + 1) % phrases.length);
          setCharIdx(0);
        } else {
          setCharIdx((c) => c - 1);
        }
      }
    }, deleting ? 40 : 80);
    return () => clearTimeout(timeout);
  }, [charIdx, deleting, phraseIdx]);

  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 lg:px-10 pt-20 overflow-hidden">
      <div className="absolute rounded-full blur-[120px] opacity-20 pointer-events-none w-[600px] h-[600px] -top-40 -left-40 bg-[#00f0ff]" />
      <div className="absolute rounded-full blur-[120px] opacity-15 pointer-events-none w-[500px] h-[500px] top-1/2 -right-60 bg-[#7b2fff]" />

      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(#00f0ff 1px, transparent 1px), linear-gradient(90deg, #00f0ff 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
        }}
      />

      <div className="relative z-10 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 border border-[#1a1a2e] bg-[#0a0a14] rounded-full px-4 py-2 mb-10">
          <span className="w-2 h-2 rounded-full bg-[#00f0ff] animate-pulse" />
          <span className="text-[#00f0ff] text-xs font-medium tracking-widest uppercase">
            Public Beta — 12M+ tasks processed
          </span>
        </div>

        <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6 tracking-tight">
          Build teams of
          <br />
          <span className="bg-gradient-to-r from-[#00f0ff] via-[#7b2fff] to-[#ff2f7b] bg-clip-text text-transparent">
            {typedText}
          </span>
          <span className="animate-pulse text-[#00f0ff]">|</span>
        </h1>

        <p className="text-[#667788] text-lg max-w-xl mx-auto mb-10 leading-relaxed">
          Deploy, orchestrate, and scale specialized AI agents that work 24/7 — reasoning, executing, and adapting without human intervention.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="#agents"
            className="group relative px-8 py-3.5 rounded-xl font-semibold text-black overflow-hidden text-sm"
          >
            <span className="absolute inset-0 bg-gradient-to-r from-[#00f0ff] to-[#7b2fff] transition-opacity group-hover:opacity-80" />
            <span className="relative flex items-center gap-2">
              Deploy Your First Agent
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </span>
          </a>
          <a
            href="#features"
            className="px-8 py-3.5 rounded-xl font-semibold text-sm border border-[#1a1a2e] text-[#8899aa] hover:border-[#00f0ff] hover:text-[#00f0ff] transition-all duration-200"
          >
            See How It Works
          </a>
        </div>

        <div className="mt-16 relative rounded-2xl overflow-hidden border border-[#1a1a2e] shadow-2xl max-w-3xl mx-auto">
          <div className="flex items-center gap-2 px-4 py-3 bg-[#0a0a14] border-b border-[#1a1a2e]">
            <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
            <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
            <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
            <span className="ml-4 text-[#334455] text-xs">axon — agent-control-center</span>
          </div>
          <div className="relative">
            <Image
              src="https://images.unsplash.com/photo-1639762681057-408e52192e55?w=1200&q=80"
              alt="Dashboard preview"
              width={1200}
              height={600}
              className="w-full object-cover opacity-60"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#050508] via-transparent to-transparent" />
          </div>
        </div>
      </div>
    </section>
  );
}