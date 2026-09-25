# Design

## Context

The backend is built with FastAPI following Clean Architecture and Domain-Driven Design (as per `AGENTS.md`), exposing APIs for supply chain anomalies. The new entry point will be a Streamlit application providing an interactive dark-themed dashboard. Both the API and the new dashboard will be served via Nginx (already configured for the API) in a Docker Compose environment. The project emphasizes clean code, typed contracts, and testing.

## Goals / Non-Goals

**Goals:**

- Provide a responsive, interactive, and visually appealing dark-themed UI using Streamlit.
- Keep the dashboard as a pure presentation layer that fetches data entirely via the FastAPI backend (no direct database connections).
- Seamlessly integrate the Streamlit app into the existing Docker Compose setup.
- Route the root URL (`/`) through Nginx to the Streamlit dashboard.

**Non-Goals:**

- Implementing any domain logic or complex data processing within Streamlit (all logic belongs to the FastAPI backend).
- Building complex multi-page apps beyond the main dashboard and a simple external link to the Swagger UI.

## Decisions

1. **Dashboard Technology:**
   - **Choice:** Streamlit
   - **Rationale:** The user explicitly requested it. It is perfect for data-driven Python applications and integrates easily with the existing ecosystem.
   - **Alternatives:** React, Vue, or native FastAPI HTML templates. Rejected because Streamlit requires less boilerplate and is specified by the user.

2. **Data Integration:**
   - **Choice:** Streamlit will consume the existing `GET /api/v1/anomalies` endpoints via HTTP requests (using `httpx` or `requests`).
   - **Rationale:** Maintains the Clean Architecture boundary defined in `AGENTS.md`. The UI must not talk to the database directly.
   - **Alternatives:** Direct SQLAlchemy access from Streamlit. Rejected as it violates architectural boundaries.

3. **Styling and Theme:**
   - **Choice:** Configure `.streamlit/config.toml` to enforce a dark theme natively, using the project's preferred color palette (if any, otherwise a standard dark preset). Use `st.container(border=True)` and native Streamlit elements rather than custom HTML/CSS, adhering to `@developing-with-streamlit` best practices.
   - **Rationale:** Easiest to maintain, native to the framework, ensures consistent UX.

4. **Performance:**
   - **Choice:** Use `@st.cache_data(ttl="5m")` for fetching anomalies to prevent hammering the API on every UI interaction. Use `@st.fragment` for independent filtering and chart updates if the dashboard becomes complex.
   - **Rationale:** Keeps the app responsive while ensuring data is reasonably fresh.

5. **Deployment:**
   - **Choice:** Add a new `dashboard` service to `compose.yaml` and update `nginx.conf` to proxy `/` to `dashboard:8501`, and `/api` to `api:8000`.
   - **Rationale:** Centralizes access through Nginx and keeps services isolated.

## Risks / Trade-offs

- **Risk:** Caching might show slightly stale data immediately after a new movement is registered via Swagger.
  - **Mitigation:** Provide a "Refresh" button or keep the TTL relatively short (e.g., 1-2 minutes) and document this behavior.
- **Risk:** HTTP calls from Streamlit to the API could fail if the API container isn't ready.
  - **Mitigation:** Use `depends_on` in `compose.yaml` and add basic retry/error handling in the data-fetching layer of the Streamlit app.
