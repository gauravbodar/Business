This section outlines a practical 7-day sprint plan for building the initial n8n workflow prototype and a 30-day roadmap for scaling the product into a SaaS-style offering.

### 5.1. 7-Day Sprint Plan to Build the First n8n Workflow Prototype

The initial sprint focuses on establishing the core data ingestion and processing pipeline using publicly available and easily accessible data sources. This will validate the technical feasibility and provide a tangible prototype.

| Day(s) | Task | Deliverables | Notes |
|---|---|---|---|
| **Day 1** | **n8n Environment Setup & Core Trigger** | - n8n instance deployed (local or cloud) <br> - Basic scheduled trigger (daily/weekly) configured | Install n8n, set up basic credentials. Start with a simple cron trigger. |
| **Day 2** | **Initial Scraper Development (Probate/Gazette)** | - Working scraper for one State Government Gazette (e.g., NSW) <br> - Working scraper for one Probate Notice source (e.g., NSW Online Registry) | Focus on extracting raw HTML/text. Prioritize sources with consistent structures. |
| **Day 3** | **Initial Scraper Development (Auction/Sheriff)** | - Working scraper for Victorian Sheriff\'s Auctions <br> - Working scraper for realestate.com.au (basic search for "mortgagee in possession") | Implement basic web scraping for property addresses, dates, and URLs. |
| **Day 4** | **Data Cleaning & Standardization** | - n8n nodes for extracting Address, Notice Type, Date, URL from raw scraped data <br> - Basic standardization of extracted fields | Use Regex and JSON parsing. Focus on cleaning data from Day 2 & 3 sources. |
| **Day 5** | **Storage Integration (Google Sheets/Airtable)** | - Connection to Google Sheets or Airtable established <br> - Workflow successfully writes cleaned data to designated columns | Choose one for MVP. Ensure correct column mapping. |
| **Day 6** | **Basic Alerting & Initial Scoring Logic** | - Slack/Telegram/Email notification for new entries <br> - Placeholder for Urgency Score calculation (e.g., based on notice type) | Implement a simple notification for successful data ingestion. Begin defining scoring rules. |
| **Day 7** | **Prototype Review & Refinement** | - End-to-end workflow demonstration <br> - Documentation of current workflow <br> - Identification of immediate improvements | Test the entire flow. Gather feedback on data quality and workflow stability. |

### 5.2. 30-Day Roadmap to Scale into a SaaS-Style Product

This roadmap outlines the key stages for evolving the prototype into a more robust, feature-rich, and scalable SaaS product, focusing on expanding data sources, enhancing functionality, and preparing for user adoption.

| Week | Focus Area | Key Activities | Deliverables |
|---|---|---|---|
| **Week 1: Data Source Expansion & Refinement** | Expand coverage and improve data quality. | - Integrate AFSA NPII (API if possible, otherwise advanced scraping) <br> - Develop scrapers for 2-3 additional council public notice sites <br> - Refine existing scrapers for robustness and error handling <br> - Implement initial geocoding for addresses (e.g., using Google Maps API) | - Expanded data sources <br> - More accurate address data <br> - Improved data reliability |
| **Week 2: Advanced Data Processing & Scoring** | Enhance data cleaning, enrichment, and lead scoring. | - Implement comprehensive Data Cleaner for all sources <br> - Develop advanced Urgency Scoring module (incorporating location, property type, keywords) <br> - Integrate contact extraction and standardization <br> - Implement basic deduplication logic | - Richer, cleaner data <br> - Intelligent lead scoring <br> - Extracted contact information |
| **Week 3: Productization Layer Development (MVP)** | Build the foundational elements of the user-facing product. | - Develop front-end dashboard (basic UI with list view) <br> - Implement filtering and sorting capabilities (Notice Type, Suburb, Urgency Score) <br> - Integrate Google Maps API for property visualization <br> - Implement user authentication (basic login) | - Functional MVP dashboard <br> - Interactive map view <br> - Secure user access |
| **Week 4: Testing, Compliance & Deployment Preparation** | Ensure stability, address legal aspects, and prepare for launch. | - Comprehensive end-to-end testing of n8n workflows and front-end <br> - Review compliance checklist and implement necessary safeguards (e.g., privacy policy, ToS) <br> - Prepare for deployment (e.g., cloud hosting setup, CI/CD pipeline) <br> - Develop CSV export functionality | - Tested and stable product <br> - Compliance documentation <br> - Deployment-ready infrastructure <br> - Basic export feature |

