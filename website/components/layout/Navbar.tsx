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
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? "bg-[#050508]/90 backdrop-blur-xl border-b border-[#1a1a2e]"
          : "bg-transparent"
      }`}
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
            AXON<span className="text-[#00f0ff]">.AI</span>
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          {links.map((link) => (
            <Link
              key={link}
              href={`#${link.toLowerCase()}`}
              className="text-[#8899aa] hover:text-white text-sm font-medium tracking-widest uppercase transition-colors duration-200 hover:text-[#00f0ff]"
              style={{ fontFamily: "'Space Mono', monospace" }}
            >
              {link}
            </Link>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-4">
          <Link
            href="#"
            className="text-sm text-[#8899aa] hover:text-white transition-colors font-medium"
            style={{ fontFamily: "'Space Mono', monospace" }}
          >
            Sign in
          </Link>
          <Link
            href="#"
            className="relative group px-5 py-2.5 text-sm font-bold text-black overflow-hidden rounded-lg"
            style={{ fontFamily: "'Space Mono', monospace" }}
          >
            <span className="absolute inset-0 bg-gradient-to-r from-[#00f0ff] to-[#7b2fff] transition-all duration-300 group-hover:opacity-80" />
            <span className="relative">Get Access</span>
          </Link>
        </div>

        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden flex flex-col gap-1.5 p-2"
        >
          <span
            className={`block w-6 h-0.5 bg-white transition-all duration-300 ${menuOpen ? "rotate-45 translate-y-2" : ""}`}
          />
          <span
            className={`block w-6 h-0.5 bg-white transition-all duration-300 ${menuOpen ? "opacity-0" : ""}`}
          />
          <span
            className={`block w-6 h-0.5 bg-white transition-all duration-300 ${menuOpen ? "-rotate-45 -translate-y-2" : ""}`}
          />
        </button>
      </div>

      {menuOpen && (
        <div className="md:hidden bg-[#050508]/95 backdrop-blur-xl border-t border-[#1a1a2e] px-6 py-8 flex flex-col gap-6">
          {links.map((link) => (
            <Link
              key={link}
              href={`#${link.toLowerCase()}`}
              onClick={() => setMenuOpen(false)}
              className="text-[#8899aa] hover:text-[#00f0ff] text-sm font-medium tracking-widest uppercase transition-colors"
              style={{ fontFamily: "'Space Mono', monospace" }}
            >
              {link}
            </Link>
          ))}
          <Link
            href="#"
            className="mt-2 text-center px-5 py-3 text-sm font-bold text-black bg-gradient-to-r from-[#00f0ff] to-[#7b2fff] rounded-lg"
            style={{ fontFamily: "'Space Mono', monospace" }}
          >
            Get Access
          </Link>
        </div>
      )}
    </nav>
  );
}