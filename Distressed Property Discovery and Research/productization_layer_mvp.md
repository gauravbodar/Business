## 3. Productization Layer (MVP Features)

This section outlines the essential features for a Minimum Viable Product (MVP) of the distressed property discovery tool, focusing on a user-friendly interface and core functionalities.

### 3.1. Front-End Requirements for MVP

The front-end will provide a dashboard for users to view, filter, and manage distressed property leads. The design should prioritize clarity, ease of use, and quick access to critical information.

*   **Dashboard View:**
    *   A central display area showing a list of discovered properties.
    *   Each property entry should display key information at a glance: Address, Notice Type, Date Published, Urgency Score.
    *   Clicking on a property entry should open a detailed view with all extracted information (Source, URL, Contact Details, Price, Property Type, etc.).
*   **Filtering and Sorting:**
    *   **Notice Type Filter:** Allow users to filter properties by categories such as 'Probate', 'Insolvency', 'Foreclosure', 'Unpaid Rates', 'Auction', 'Distressed Listing (General)'.
    *   **Location Filters:** Filters for 'State', 'Suburb', and 'Postcode'.
    *   **Urgency Score Filter/Sort:** Enable sorting properties by their calculated urgency score (highest to lowest) and filtering by a score range.
    *   **Date Filters:** Filter by 'Date Published' or 'Auction Date' (e.g., last 7 days, next 30 days).
    *   **Keyword Search:** A general search bar to find properties based on keywords in their description or address.
*   **Status Management:**
    *   Ability for users to update the `Status` of a property (e.g., 'New', 'Active', 'Contacted', 'Under Offer', 'Archived').
    *   Option to add `Next Action` notes for each property.
*   **Responsive Design:** The interface must be accessible and functional across various devices (desktop, tablet, mobile).

### 3.2. Mapping API Integration

Visualizing properties on a map is crucial for geographical analysis and user experience.

*   **Integration:** Google Maps API (or similar, e.g., OpenStreetMap with Leaflet.js).
*   **Functionality:**
    *   Display property locations as markers on an interactive map within the dashboard.
    *   Clicking a map marker should reveal basic property information and a link to the detailed property view.
    *   Ability to filter properties on the map based on the applied dashboard filters.
    *   Heatmap overlay to visualize clusters of distressed properties in certain areas.

### 3.3. Export Options

Providing flexible export options allows users to integrate the data into their existing workflows or for offline analysis.

*   **CSV Export:**
    *   Export all filtered property data into a CSV file, suitable for spreadsheet analysis.
    *   Columns should match the database schema.
*   **vCard Export for Contacts:**
    *   For properties with extracted contact details, provide an option to export these as vCard files.
    *   This allows easy import into CRM systems or contact managers.
*   **PDF Weekly Digest:**
    *   Generate a professional, formatted PDF report summarizing new and high-priority leads for the week.
    *   Include property details, urgency scores, and potentially small map snippets for each property.
    *   This can be automated and emailed to users as a subscription feature.

### 3.4. User Authentication and Management

*   **Basic User Accounts:** Secure login and registration for users.
*   **Role-Based Access (Future):** Differentiate between free and premium users, or team members with different permissions.

This MVP focuses on delivering core value by providing actionable leads through an intuitive interface, with clear pathways for future enhancements.
