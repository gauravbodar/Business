## 7. Execution Timeline (Gantt-style)

This section transforms the high-level 7-day sprint and 30-day roadmap into a concrete, operational Gantt-style plan. It details day-by-day tasks for the first two weeks and weekly deliverables for the first 60 days, assigning roles to each task to ensure clear accountability.

**Who does this:** [Founder] (Overall Management), [Dev] (Development), [Ops] (Operations/n8n), [Growth] (Marketing/Sales)

### 7.1. Day-by-Day Tasks (First 2 Weeks)

This detailed breakdown covers the initial setup, core data pipeline development, and early productization efforts.

| Day | Task Category | Specific Task | Role | Estimated Hours |
|---|---|---|---|---|
| **Week 1: Prototype & Core Data Pipeline** | | | | |
| Day 1 | **Environment Setup** | 1.1. Create Replit project, configure `.replit` and `replit.nix` for Python/Node.js. | [Dev] | 4 |
| | | 1.2. Install n8n locally or deploy to cloud (e.g., DigitalOcean droplet). | [Ops] | 4 |
| Day 2 | **n8n Workflow - Triggers & AFSA** | 2.1. Configure n8n scheduled trigger (daily). | [Ops] | 2 |
| | | 2.2. Develop n8n workflow for AFSA NPII (API or initial web scraper). | [Ops] | 6 |
| Day 3 | **n8n Workflow - Real Estate Portals** | 2.3. Develop n8n workflow for realestate.com.au (basic search for "mortgagee in possession"). | [Ops] | 8 |
| Day 4 | **n8n Workflow - Data Cleaning** | 2.4. Implement n8n Data Cleaner nodes for AFSA and realestate.com.au data (address, notice type, date, URL). | [Ops] | 8 |
| Day 5 | **n8n Workflow - Storage & Geocoding** | 2.5. Set up Google Sheets/Airtable as MVP database, map columns. | [Ops] | 4 |
| | | 2.6. Integrate Google Maps Geocoding API into n8n for address enrichment. | [Dev] | 4 |
| Day 6 | **n8n Workflow - Scoring & Alerting** | 2.7. Implement basic Urgency Scoring logic in n8n (Function Node). | [Ops] | 6 |
| | | 2.8. Configure Slack/Email alerts for new high-score leads. | [Ops] | 2 |
| Day 7 | **Frontend MVP - Setup & Display** | 3.1. Set up React frontend in Replit (`frontend/` directory). | [Dev] | 4 |
| | | 3.2. Develop basic dashboard UI to display leads from database (read-only). | [Dev] | 4 |
| **Week 2: Productization & Initial Features** | | | | |
| Day 8 | **Frontend MVP - Filtering & Sorting** | 3.3. Implement client-side filtering (Notice Type, Suburb) and sorting (Urgency Score). | [Dev] | 8 |
| Day 9 | **Frontend MVP - Mapping Integration** | 3.4. Integrate Leaflet.js/React-Leaflet to display property markers on a map. | [Dev] | 8 |
| Day 10 | **Authentication & User Management** | 3.5. Implement backend API endpoints for user registration and login (JWT). | [Dev] | 8 |
| Day 11 | **Subscription Integration (Stripe/PayPal)** | 3.6. Set up Stripe/PayPal products/plans. | [Founder] | 4 |
| | | 3.7. Implement backend webhook for subscription status updates. | [Dev] | 4 |
| Day 12 | **Role-Based Access & Data Limits** | 3.8. Implement role-based access control for premium features. | [Dev] | 6 |
| | | 3.9. Implement daily lead quota enforcement for free users. | [Dev] | 2 |
| Day 13 | **Compliance & Documentation** | 6.1. Draft Privacy Policy and Terms of Service. | [Founder] | 8 |
| Day 14 | **Testing & Refinement** | 7.1. End-to-end testing of core workflows and MVP features. | [Dev], [Ops] | 8 |

### 7.2. Weekly Deliverables (First 60 Days)

This roadmap extends beyond the initial prototype, focusing on scaling, marketing, and operational maturity.

| Week | Focus Area | Key Activities | Deliverables | Role |
|---|---|---|---|---|
| **Week 1-2** | **Core Product Development & MVP Launch** | - Complete Day 1-14 tasks. <br> - Deploy MVP to Replit. <br> - Internal testing and feedback. | - Functional MVP with core data pipeline, authentication, basic mapping, and filtering. <br> - Initial compliance documents. | [Dev], [Ops], [Founder] |
| **Week 3** | **Data Source Expansion & Refinement** | - Develop scrapers for 2-3 additional council public notice sites. <br> - Refine existing scrapers for robustness and error handling. <br> - Implement additional government gazette scrapers (e.g., QLD, SA). | - Expanded data coverage. <br> - Improved data reliability. | [Ops] |
| **Week 4** | **Advanced Data Processing & Scoring** | - Implement comprehensive Data Cleaner for all sources. <br> - Develop advanced Urgency Scoring module (incorporating location, property type, keywords). <br> - Integrate contact extraction and standardization. | - Richer, cleaner data. <br> - Intelligent lead scoring. <br> - Extracted contact information. | [Ops], [Dev] |
| **Week 5** | **Outbound Sales & Marketing Setup** | - Set up Apollo.io account and define ICPs. <br> - Build initial target lists in Apollo.io. <br> - Set up Instantly.ai account and warm up sending domains. | - Targeted lead lists. <br> - Instantly.ai ready for campaigns. | [Growth] |
| **Week 6** | **Outbound Campaign Launch & Optimization** | - Draft initial cold email templates and sequences in Instantly.ai. <br> - Launch first outbound campaigns. <br> - Monitor initial campaign metrics (open, reply rates). | - Active outbound campaigns. <br> - Initial performance data. | [Growth] |
| **Week 7** | **Growth & Customer Operations - PDF Digest** | - Develop n8n workflow for weekly PDF digest generation for premium subscribers. <br> - Implement email delivery for PDF digests. | - Automated weekly PDF digest system. | [Ops], [Dev] |
| **Week 8** | **Growth & Customer Operations - CRM Integration** | - Integrate Instantly.ai with CRM (e.g., HubSpot) via n8n webhooks. <br> - Set up CRM data flow for user signups and subscription status. | - Unified CRM with lead and customer data. | [Ops], [Dev], [Growth] |
| **Week 9** | **Compliance & Risk Refinement** | - Conduct internal audit of data retention policies. <br> - Implement automated data anonymization/deletion workflows in n8n. <br> - Review and update disclaimers based on user feedback/legal advice. | - Robust data retention and compliance. | [Founder], [Ops] |
| **Week 10** | **Performance Monitoring & Scaling** | - Implement advanced monitoring for n8n workflows and app performance. <br> - Optimize database for scalability (e.g., migrate from Google Sheets to PostgreSQL). <br> - Review and optimize cloud infrastructure costs. | - Scalable and performant system. <br> - Cost-optimized infrastructure. | [Dev], [Ops] |
| **Week 11** | **Feature Enhancement & User Feedback** | - Implement 1-2 high-priority feature requests from early users. <br> - Set up a system for collecting and prioritizing user feedback. | - Improved user experience. <br> - Structured feedback loop. | [Dev], [Founder] |
| **Week 12** | **Marketing & Sales Expansion** | - Analyze outbound campaign results and refine strategies. <br> - Explore additional marketing channels (e.g., content marketing, social media). <br> - Develop sales enablement materials. | - Optimized marketing funnels. <br> - Expanded market reach. | [Growth], [Founder] |

This timeline provides a structured path from initial prototype to a fully operational SaaS product, emphasizing iterative development and continuous improvement across all operational areas.
