import Image from "next/image";

const TESTIMONIALS = [
  {
    quote: "Axon replaced an entire QA team. Our agents now catch edge cases we never even thought of.",
    author: "Priya Menon",
    role: "CTO, Streamline Labs",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&q=80",
  },
  {
    quote: "We shipped a feature in 3 days that would have taken 3 weeks. The CodeAgent is genuinely insane.",
    author: "Marcus Chen",
    role: "Eng Lead, Vortex Systems",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&q=80",
  },
  {
    quote: "The ResearchAgent synthesizes 500-page reports overnight. Our analysts now focus on decisions, not digging.",
    author: "Aisha Okafor",
    role: "Head of Strategy, NeoCorp",
    avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&q=80",
  },
];

export default function Testimonials() {
  return (
    <section className="py-24 px-6 lg:px-10">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-14">
          <span className="text-[#ffb800] text-xs font-semibold tracking-widest uppercase mb-3 block">
            ◆ Testimonials
          </span>
          <h2 className="text-4xl md:text-5xl font-bold">
            Teams that moved faster{" "}
            <span className="bg-gradient-to-r from-[#ffb800] to-[#ff2f7b] bg-clip-text text-transparent">
              with AXON.
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {TESTIMONIALS.map((t, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border border-[#1a1a2e] bg-[#080810] hover:border-[#2a2a3e] transition-colors duration-300"
            >
              <p className="text-[#889aaa] text-sm leading-relaxed mb-6">"{t.quote}"</p>
              <div className="flex items-center gap-3">
                <Image
                  src={t.avatar}
                  alt={t.author}
                  width={36}
                  height={36}
                  className="rounded-full object-cover border border-[#1a1a2e]"
                />
                <div>
                  <div className="text-white text-sm font-semibold">{t.author}</div>
                  <div className="text-[#445566] text-xs">{t.role}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}