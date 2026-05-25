const ITEMS = [
  "Autonomous Reasoning",
  "Multi-Agent Swarms",
  "Real-Time Learning",
  "Self-Healing Pipelines",
  "Tool-Use Mastery",
  "Edge Deployment",
  "Memory Engine",
  "Zero-Shot Execution",
];

export default function Marquee() {
  return (
    <div className="relative overflow-hidden py-5 border-y border-[#0d0d1a]">
      <div
        className="flex whitespace-nowrap"
        style={{ animation: "marquee 30s linear infinite" }}
      >
        {[...ITEMS, ...ITEMS, ...ITEMS].map((item, i) => (
          <span
            key={i}
            className="inline-flex items-center gap-4 px-8 text-xs font-semibold tracking-widest uppercase text-[#334455]"
          >
            <span className="text-[#00f0ff]">◆</span>
            {item}
          </span>
        ))}
      </div>

      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-33.33%); }
        }
      `}</style>
    </div>
  );
}