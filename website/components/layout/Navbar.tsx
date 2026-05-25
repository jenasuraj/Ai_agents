"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const links = ["Agents", "Features", "Showcase", "Pricing", "Docs"];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 `}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-10 flex items-center justify-between h-20">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative w-9 h-9">
            <div className="absolute inset-0 bg-gradient-to-br from-[#00f0ff] to-[#7b2fff] rounded-lg rotate-45 group-hover:rotate-90 transition-transform duration-500" />
            <div className="absolute inset-[3px] bg-[#050508] rounded-md rotate-45" />
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-[#00f0ff] font-black text-sm">Λ</span>
            </div>
          </div>
          <span
            className="text-white font-black text-xl tracking-tight"
            style={{ fontFamily: "'Space Mono', monospace" }}
          >
            Agentic<span className="text-[#00f0ff]">.AI</span>
          </span>
        </Link>

      </div>

   
    </nav>
  );
}