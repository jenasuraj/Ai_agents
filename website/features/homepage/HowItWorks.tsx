import Image from "next/image";

const STEPS = [
  {
    step: "01",
    title: "Define your objective",
    desc: "Describe what you need in plain language. AXON breaks it into agent-ready subtasks automatically.",
  },
  {
    step: "02",
    title: "Agents collaborate",
    desc: "Specialized agents spin up, share context, and execute in parallel with full coordination.",
  },
  {
    step: "03",
    title: "Review & ship",
    desc: "Get structured outputs, logs, and confidence scores. Approve, refine, or automate entirely.",
  },
];

export default function HowItWorks() {
  return (
    <section className="py-24 px-6 lg:px-10">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-14 items-center">
          <div>
            <span className="text-[#ff2f7b] text-xs font-semibold tracking-widest uppercase mb-3 block">
              ◆ How It Works
            </span>
            <h2 className="text-4xl md:text-5xl font-bold mb-8 leading-tight">
              From prompt to{" "}
              <span className="bg-gradient-to-r from-[#ff2f7b] to-[#ffb800] bg-clip-text text-transparent">
                production in minutes.
              </span>
            </h2>

            <div className="flex flex-col gap-7">
              {STEPS.map((item) => (
                <div key={item.step} className="flex gap-4 group">
                  <div className="flex-shrink-0 w-9 h-9 rounded-lg bg-[#0d0d1a] border border-[#1a1a2e] flex items-center justify-center text-xs font-bold text-[#ff2f7b] group-hover:border-[#ff2f7b] transition-colors">
                    {item.step}
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-1 text-sm">{item.title}</h4>
                    <p className="text-[#556677] text-sm leading-relaxed">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-[#ff2f7b]/10 to-[#7b2fff]/10 rounded-3xl blur-xl" />
            <div className="relative rounded-2xl overflow-hidden border border-[#1a1a2e]">
              <Image
                src="https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800&q=80"
                alt="Agent workflow"
                width={800}
                height={600}
                className="w-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#050508]/80 to-transparent" />
              <div className="absolute bottom-5 left-5 right-5">
                <div className="bg-[#080810]/90 backdrop-blur-sm rounded-xl p-4 border border-[#1a1a2e]">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-2 h-2 rounded-full bg-[#27c93f] animate-pulse" />
                    <span className="text-white text-xs font-semibold">CodeAgent — Running task #5193</span>
                  </div>
                  <div className="text-[#445566] text-xs leading-relaxed font-mono">
                    <span className="text-[#00f0ff]">→</span> Analyzing codebase...<br />
                    <span className="text-[#00f0ff]">→</span> Generating unit tests for 47 functions...<br />
                    <span className="text-[#27c93f]">✓</span> Coverage improved: 61% → 94%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}