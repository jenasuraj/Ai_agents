export default function CTA() {
  return (
    <section className="py-28 px-6 lg:px-10 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-[#00f0ff]/5 via-[#7b2fff]/5 to-[#ff2f7b]/5" />
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(#00f0ff 1px, transparent 1px), linear-gradient(90deg, #00f0ff 1px, transparent 1px)`,
          backgroundSize: "40px 40px",
        }}
      />

      <div className="max-w-3xl mx-auto text-center relative z-10">
        <div className="inline-flex items-center gap-2 border border-[#1a1a2e] bg-[#0a0a14] rounded-full px-4 py-2 mb-8">
          <span className="w-2 h-2 rounded-full bg-[#27c93f] animate-pulse" />
          <span className="text-[#27c93f] text-xs font-semibold tracking-widest uppercase">
            All systems operational
          </span>
        </div>

        <h2 className="text-4xl md:text-6xl font-bold mb-5 leading-tight">
          Ready to deploy your{" "}
          <span className="bg-gradient-to-r from-[#00f0ff] via-[#7b2fff] to-[#ff2f7b] bg-clip-text text-transparent">
            AI workforce?
          </span>
        </h2>

        <p className="text-[#556677] text-base max-w-lg mx-auto mb-10 leading-relaxed">
          Join 3,000+ teams running agents on AXON. Start free, scale on demand. No credit card required.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="#"
            className="group relative px-9 py-3.5 rounded-xl font-semibold text-black overflow-hidden text-sm w-full sm:w-auto"
          >
            <span className="absolute inset-0 bg-gradient-to-r from-[#00f0ff] to-[#7b2fff] group-hover:opacity-80 transition-opacity" />
            <span className="relative flex items-center justify-center gap-2">
              Start for free
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </span>
          </a>
          <a
            href="#"
            className="px-9 py-3.5 rounded-xl font-semibold text-sm border border-[#1a1a2e] text-[#8899aa] hover:border-[#00f0ff]/40 hover:text-white transition-all duration-200 w-full sm:w-auto text-center"
          >
            Talk to sales
          </a>
        </div>
      </div>
    </section>
  );
}