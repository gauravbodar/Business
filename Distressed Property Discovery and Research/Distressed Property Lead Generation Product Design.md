
The 4-Stage Execution Roadmap

[ STAGE 1: Lean Build ] ---> [ STAGE 2: Deal Sourcing ] ---> [ STAGE 3: Whitelabel CAR ] ---> [ STAGE 4: Scale to $1M ]
  (Claude + MCP MVP)          (Data Pipeline & Proof)          (Legal & Trust Activation)      (Wholesale Syndication)

🛠️ Stage 1: Lean Build & Validation (Month 1)

• Objective: Build a functional interactive frontend prototype showcasing a live mock data-sourcing feed.
• Tech Stack: Claude Pro, Claude Code, local MCP servers, and free-tier hosting (Vercel/GitHub Pages).
• Key Result: A working, low-hype investor dashboard showing unlisted property insights to validate demand.

📈 Stage 2: Distressed Deal Sourcing & Proof (Months 2–3)

• Objective: Establish automated data pipelines to ingest real-world distressed property leads.
• Mechanism: Program text-mining scripts via Claude to monitor supreme court probate registries and scrape public portals for distressed keywords ("Mortgagee in possession", "Deceased estate").
• Key Result: A verified database of 50+ off-market opportunities with high equity margins.

⚖️ Stage 3: Corporate Structure & White-Label Activation (Months 4–5)

• Objective: Activate legal compliance framework without the 12-month delay of a direct AFSL application.
• Mechanism: Partner with an established wholesale trustee service provider to appoint your entity as a Corporate Authorised Representative (CAR).
• Key Result: Legal clearance to operate an Unlisted Wholesale Unit Trust and accept Section 708 sophisticated investor capital.

🚀 Stage 4: Wholesale Syndication & Scale (Months 6+)

• Objective: Scale platform revenue to a $1M+ run rate by pooling capital for high-margin deals.
• Mechanism: Deploy your investor acquisition funnel targeting private angel syndicates, boutique accounting firms, and direct LinkedIn outbound.
• Key Result: Fund your first 3 distressed assets, collecting a 1–2% acquisition fee and a 10–20% performance fee on realized equity gains.

Key Financial & Operational Metrics

• Phase 1 Development Cost: ~$31.00/month (Claude Pro Subscription).
• Target Minimum Investment: $50,000 – $100,000 per investor, per deal.
• Investor Gate: Mandatory upload of a valid accountant-signed Section 708 Sophisticated Investor Certificate.

THE CLAUDE PROMPT TO BUILD PHASE 1

Copy and paste the exact prompt below into Claude to initiate the software engineering phase for your Stage 1 prototype.
text
Act as a Lead Full-Stack Software Engineer and Data Engineer specialized in Australian fintech and proptech platforms. 

We are building a lean Phase 1 MVP for an AI-powered property intelligence platform targeting wholesale and sophisticated investors under Section 708 of the Corporations Act. The core feature of this prototype is a highly clinical, data-dense investor dashboard that showcases "Unlisted Distressed Property Insights" (e.g., Deceased Estates, Bankruptcies, and Mortgagee-in-Possession listings).

Please generate a single-file, production-ready interactive frontend layout using React, Tailwind CSS, and Lucide React icons. Deliver this as a fully functional component that can be easily previewed or deployed.

The dashboard must include the following structural elements:
1. A clean, premium, institutional-grade theme (dark or high-contrast clean slate) that avoids consumer marketing fluff and speaks directly to private equity investors.
2. A high-level analytics ribbon showing key aggregate data (e.g., "Active Off-Market Deals Found", "Average Projected Equity Margin", "Total Pooled Capital Target").
3. A main interactive data table displaying a list of realistic mock distressed properties across Australia (including columns for: Asset Type, Distressed Indicator, Estimated Market Value, Target Purchase Price, and Projected ROI/Equity Margin).
4. A robust interactive filter sidebar allowing users to filter listings by State (NSW, ACT, VIC, QLD, WA), Category (Probate, Bankruptcy, Mortgagee in Possession), and Minimum Equity Margin.
5. A "Section 708 Verification Lock" overlay or gate placeholder mechanism: when an investor clicks a property row to view the "Exact Title Deed and Address Details," a sleek modal should appear requiring them to verify their wholesale status or upload a mock Section 708 Accountant's Certificate to unlock premium wholesale data.

Design everything cleanly using modular React code with inline mock data arrays representing the scraped real estate data pipe. Focus heavily on a "Smart Brevity" style layouts—highly scannable, dense text grids, and functional UI elements.
Use code with caution.
