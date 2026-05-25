const FEATURES = [
  {
    icon: "⬡",
    title: "Multi-Agent Orchestration",
    desc: "Deploy swarms of specialized agents that collaborate, delegate, and self-coordinate to solve complex multi-step tasks.",
    accent: "#00f0ff",
  },
  {
    icon: "◈",
    title: "Memory & Context Engine",
    desc: "Persistent long-term memory with semantic search. Your agents remember everything across sessions and teams.",
    accent: "#7b2fff",
  },
  {
    icon: "⌖",
    title: "Tool-Use & API Mastery",
    desc: "Native integrations with 200+ tools. Agents browse the web, write code, query databases, and call any REST API.",
    accent: "#ff2f7b",
  },
  {
    icon: "⟁",
    title: "Self-Healing Pipelines",
    desc: "Agents detect failures, retry with alternative strategies, and escalate intelligently. Zero babysitting required.",
    accent: "#ffb800",
  },
  {
    icon: "⊞",
    title: "Audit & Explainability",
    desc: "Every decision is logged. Full chain-of-thought transparency with replay, diff, and approval workflows built in.",
    accent: "#00f0ff",
  },
  {
    icon: "⌬",
    title: "Edge Deployment",
    desc: "Run agents close to your data. On-premise, private cloud, or serverless — with sub-50ms response times globally.",
    accent: "#7b2fff",
  },
];

export default function Features() {
  return (
    <section id="features" className="py-24 px-6 lg:px-10 relative">
      <div
        className="absolute inset-0 opacity-[0.02]"
        style={{
          backgroundImage: `radial-gradient(#00f0ff 1px, transparent 1px)`,
          backgroundSize: "32px 32px",
        }}
      />

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="text-center mb-14">
          <span className="text-[#7b2fff] text-xs font-semibold tracking-widest uppercase mb-3 block">
            ◆ Capabilities
          </span>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Everything you need.{" "}
            <span className="bg-gradient-to-r from-[#7b2fff] to-[#ff2f7b] bg-clip-text text-transparent">
              Nothing you don't.
            </span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {FEATURES.map((f, i) => (
            <div
              key={i}
              className="group p-6 rounded-2xl border border-[#1a1a2e] bg-[#080810] hover:border-[#2a2a3e] transition-all duration-300 relative overflow-hidden"
            >
              <div
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl"
                style={{ background: `radial-gradient(circle at top left, ${f.accent}08, transparent 60%)` }}
              />
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center text-xl mb-4"
                style={{ background: `${f.accent}10`, color: f.accent }}
              >
                {f.icon}
              </div>
              <h3 className="text-white font-semibold text-base mb-2">{f.title}</h3>
              <p className="text-[#556677] text-sm leading-relaxed">{f.desc}</p>
              <div
                className="absolute bottom-0 left-0 right-0 h-px opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                style={{ background: `linear-gradient(90deg, transparent, ${f.accent}, transparent)` }}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}