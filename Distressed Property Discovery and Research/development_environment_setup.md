## 1. Development Environment & Stack Setup

This section provides a step-by-step guide for setting up the development environment and defining the technology stack for the Distressed Property Discovery SaaS. The focus is on leveraging Replit for rapid development and deployment, with clear integration points for the backend and database.

### 1.1. Replit Project Setup (Frontend + Backend)

**Goal:** Establish a monorepo structure within Replit to host both the frontend (user interface) and backend (API services, authentication).

**Who does this:** [Dev], [Founder]

**Steps:**
1.  **Create a New Replit Project:**
    *   Go to [Replit](https://replit.com/) and log in or sign up.
    *   Click the `+ Create Repl` button.
    *   Choose a template that supports both frontend and backend development. A `Node.js` or `Python` template with web server capabilities is ideal. For a React frontend and Python/Flask backend, select a `Python` template and manually add Node.js for frontend build, or vice-versa. Alternatively, start with a `Blank` Repl and configure it.
    *   Name your Repl (e.g., `distressed-property-app`) and set it to `Private`.
2.  **Monorepo Structure:** Organize your project into logical directories.
    *   `./frontend/`: Contains all React application code.
    *   `./backend/`: Contains all Flask/FastAPI application code.
    *   `./scripts/`: Utility scripts (e.g., database migrations, setup).
    *   `./.replit`: Replit configuration file.
    *   `./replit.nix`: Nix configuration for dependencies.

**Sample `.replit` configuration (for a Python backend with a React frontend):**

```toml
run = "python3.11 backend/app.py"

[languages]

[languages.python]
pythonVersion = "3.11"

[entrypoint]
command = ["python3.11", "backend/app.py"]

[packager]
language = "python3"

[packager.features]
packageSearch = true

[nix]
pkgs = ["nodejs-18_x", "python311", "python311Packages.pip"]

[deployment]
# Configure deployment settings here (e.g., always-on, custom domain)
# For MVP, manual deployment or Replit's always-on feature can be used.
```

### 1.2. Recommended Frameworks, Libraries, and Authentication

**Goal:** Select robust and efficient technologies for rapid development.

**Who does this:** [Dev]

*   **Frontend:**
    *   **Framework:** [React](https://react.dev/) (with Vite or Create React App for bootstrapping).
    *   **Styling:** [Tailwind CSS](https://tailwindcss.com/) for utility-first styling and rapid UI development.
    *   **Mapping:** [Leaflet.js](https://leafletjs.com/) with [React-Leaflet](https://react-leaflet.js.org/) for interactive maps, integrating with OpenStreetMap or Google Maps API.
*   **Backend:**
    *   **Framework:** [Flask](https://flask.palletsprojects.com/) (Python) for its simplicity and flexibility, or [FastAPI](https://fastapi.tiangolo.com/) for high performance and automatic API documentation.
    *   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) for database interaction (if using PostgreSQL).
    *   **Serialization:** [Marshmallow](https://marshmallow.readthedocs.io/) (for Flask) or Pydantic (for FastAPI) for data validation and serialization.
*   **Authentication (Basic Membership/Subscription Service):**
    *   **Method:** [JWT (JSON Web Tokens)](https://jwt.io/) for stateless authentication.
    *   **Implementation:** Use libraries like `Flask-JWT-Extended` (Flask) or implement manually with `PyJWT` (Python) for token generation and validation.
    *   **Flow:** User signs up/logs in -> Backend issues JWT -> Frontend stores JWT (e.g., in `localStorage` or `httpOnly` cookies) -> Frontend sends JWT with each authenticated request.

### 1.3. Integration Plan with Database

**Goal:** Define the database strategy, starting with a simple MVP solution and planning for scalability.

**Who does this:** [Dev], [Ops]

*   **MVP Database (Google Sheets/Airtable):**
    *   **Integration:** Use n8n to directly write cleaned data to Google Sheets or Airtable. These platforms offer APIs that n8n can easily connect to.
    *   **Access:** Frontend can read data via a backend API layer that queries Google Sheets/Airtable APIs (or n8n can expose an API endpoint for the frontend).
    *   **Pros:** Quick setup, no database administration overhead.
    *   **Cons:** Limited scalability, query performance issues with large datasets, less robust for complex relations.
*   **Scalable Database (PostgreSQL):**
    *   **Deployment:** Host PostgreSQL on a cloud provider (e.g., [Render](https://render.com/), [Supabase](https://supabase.com/), [ElephantSQL](https://www.elephantsql.com/)). Replit can connect to external databases.
    *   **Integration:** n8n will connect to PostgreSQL using its native PostgreSQL node. The backend application (Flask/FastAPI) will use SQLAlchemy to interact with the database.
    *   **Migration:** Plan for a migration path from Google Sheets/Airtable to PostgreSQL as the product scales.

### 1.4. Git/Branch Workflow and CI/CD Strategy for Replit

**Goal:** Establish a streamlined development and deployment process.

**Who does this:** [Dev], [Founder]

*   **Git Workflow:**
    *   **Repository:** Host code on [GitHub](https://github.com/) and link it to your Replit project.
    *   **Branching Strategy:** Use a `main` branch for production-ready code and feature branches for new development. Merge feature branches into `main` via pull requests.
    *   **Replit Integration:** Replit integrates directly with GitHub, allowing you to pull from and push to your repository.
*   **CI/CD Strategy (Replit Deployments):**
    *   **Replit Deployments:** Utilize Replit's built-in deployment features for continuous deployment.
    *   **Automatic Deployments:** Configure Replit to automatically deploy changes from the `main` branch upon successful pushes.
    *   **Environment Variables:** Manage sensitive information (API keys, database credentials) using Replit's Secrets feature (environment variables).
    *   **Build Steps:** Define build commands in `.replit` or `replit.nix` to install frontend dependencies, build the React app, and then run the backend server.

**Sample `replit.nix` for Node.js and Python:**

```nix
{ pkgs }:
{
  deps = [
    pkgs.nodejs-18_x
    pkgs.python311
    pkgs.python311Packages.pip
  ];
}
```

**Sample `package.json` (in `./frontend/`) for React build:**

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "tailwindcss": "^3.3.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

**Backend `app.py` (in `./backend/`) example:**

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(message='Hello from the backend!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

This setup provides a solid foundation for developing and deploying the SaaS application efficiently within the Replit ecosystem.
