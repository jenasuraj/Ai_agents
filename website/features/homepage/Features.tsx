const FEATURES = [
  {
    icon: "🧠",
    title: "Agentic RAG",
    desc: "Retrieval-Augmented Generation with autonomous agents that fetch, reason, and synthesize knowledge from multiple sources.",
    accent: "#00f0ff",
  },
  {
    icon: "🤖",
    title: "Deep Agent",
    desc: "Advanced multi-step reasoning agents capable of planning, decision-making, and executing complex workflows end-to-end.",
    accent: "#7b2fff",
  },
  {
    icon: "🐙",
    title: "GitHub Agent",
    desc: "Automates repo management, code analysis, PR reviews, and issue tracking directly from your GitHub workflows.",
    accent: "#ff2f7b",
  },
  {
    icon: "📝",
    title: "Notion Agent",
    desc: "Seamlessly reads, writes, and organizes Notion pages, enabling automated documentation and knowledge management.",
    accent: "#ffb800",
  },
  {
    icon: "🎙️",
    title: "Podcast Agent",
    desc: "Generates, summarizes, and transforms content into podcast-style audio workflows using AI narration pipelines.",
    accent: "#00f0ff",
  },
  {
    icon: "🕸️",
    title: "Web Scraper Agent",
    desc: "Intelligently extracts, structures, and processes data from websites with autonomous scraping and parsing logic.",
    accent: "#7b2fff",
  },
  {
    icon: "📈",
    title: "Stock Intelligence Agent",
    desc: "Analyzes market trends, fetches real-time stock data, and provides actionable insights using AI-driven models.",
    accent: "#ff2f7b",
  },
  {
    icon: "✈️",
    title: "Travel Agent",
    desc: "Plans trips, compares routes, fetches pricing, and builds personalized itineraries with real-time data integration.",
    accent: "#ffb800",
  },
];

export default function Features() {
  return (
    <section id="agents" className="py-24 px-6 lg:px-10 relative">
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