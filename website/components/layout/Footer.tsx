import Link from "next/link";

export default function Footer() {
  const year = new Date().getFullYear();

  const cols = [
    {
      title: "Product",
      links: ["Agents", "Workflows", "Integrations", "Changelog", "Roadmap"],
    },
    {
      title: "Developers",
      links: ["Docs", "API Reference", "SDKs", "Examples", "Status"],
    },
    {
      title: "Company",
      links: ["About", "Blog", "Careers", "Press Kit", "Contact"],
    },
  ];

  return (
    <footer className="bg-[#020205] border-t border-[#0d0d1a] pt-20 pb-10 px-6 lg:px-10">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12 mb-16">
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-6">
              <div className="relative w-9 h-9">
                <div className="absolute inset-0 bg-gradient-to-br from-[#00f0ff] to-[#7b2fff] rounded-lg rotate-45" />
                <div className="absolute inset-[3px] bg-[#020205] rounded-md rotate-45" />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-[#00f0ff] font-black text-sm">Λ</span>
                </div>
              </div>
              <span
                className="text-white font-black text-xl"
                style={{ fontFamily: "'Space Mono', monospace" }}
              >
                AXON<span className="text-[#00f0ff]">.AI</span>
              </span>
            </div>
            <p
              className="text-[#445566] text-sm leading-relaxed max-w-xs mb-8"
              style={{ fontFamily: "'Space Mono', monospace" }}
            >
              Autonomous AI agents that think, learn, and act. Built for teams
              who demand more than automation.
            </p>
            <div className="flex gap-4">
              {["𝕏", "⬡", "◎", "⌂"].map((icon, i) => (
                <Link
                  key={i}
                  href="#"
                  className="w-9 h-9 border border-[#1a1a2e] rounded-lg flex items-center justify-center text-[#445566] hover:border-[#00f0ff] hover:text-[#00f0ff] transition-all duration-200 text-sm"
                >
                  {icon}
                </Link>
              ))}
            </div>
          </div>

          {cols.map((col) => (
            <div key={col.title}>
              <h4
                className="text-white font-bold text-xs tracking-widest uppercase mb-5"
                style={{ fontFamily: "'Space Mono', monospace" }}
              >
                {col.title}
              </h4>
              <ul className="flex flex-col gap-3">
                {col.links.map((link) => (
                  <li key={link}>
                    <Link
                      href="#"
                      className="text-[#445566] hover:text-[#00f0ff] text-sm transition-colors duration-200"
                      style={{ fontFamily: "'Space Mono', monospace" }}
                    >
                      {link}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-[#0d0d1a] pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p
            className="text-[#334455] text-xs"
            style={{ fontFamily: "'Space Mono', monospace" }}
          >
            © {year} Axon AI, Inc. All rights reserved.
          </p>
          <div className="flex gap-6">
            {["Privacy Policy", "Terms of Service", "Cookie Policy"].map(
              (item) => (
                <Link
                  key={item}
                  href="#"
                  className="text-[#334455] hover:text-[#00f0ff] text-xs transition-colors"
                  style={{ fontFamily: "'Space Mono', monospace" }}
                >
                  {item}
                </Link>
              )
            )}
          </div>
        </div>
      </div>
    </footer>
  );
}