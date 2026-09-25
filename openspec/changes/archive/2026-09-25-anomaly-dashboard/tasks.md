# Tasks

## 1. Setup and Dependencies

- [x] 1.1 Add `streamlit`, `pandas`, `altair`, and HTTP client (`httpx` or `requests`) to project dependencies (`pyproject.toml` / `uv`) and verify package installation succeeds.
- [x] 1.2 Create `src/dashboard/app.py` as the entry point for Streamlit and verify the file is present.

## 2. Infrastructure Configuration

- [x] 2.1 Update `compose.yaml` to configure the `dashboard` service (or `api` service if combined, though standard is a new service) to run `uv run streamlit run src/dashboard/app.py`. Verify `docker compose config` is valid.
- [x] 2.2 Update `nginx/nginx.conf` to proxy `/api` traffic to the FastAPI backend and `/` to the new Streamlit dashboard service. Verify `nginx -t` or similar config validation.

## 3. UI Implementation: Theme & Layout

- [x] 3.1 Create `.streamlit/config.toml` to configure the dark theme explicitly. Verify by checking if the configuration is applied when running Streamlit locally.
- [x] 3.2 Implement the main layout in `src/dashboard/app.py` with `st.set_page_config`, a header, and a direct link to the Swagger UI (`/api/docs`). Verify the page renders and the link is visible.

## 4. UI Implementation: Data Fetching and Metrics

- [x] 4.1 Implement a cached data fetching function (`@st.cache_data(ttl="5m")`) in `app.py` that calls the FastAPI backend's `GET /api/v1/anomalies` endpoint. Verify by successfully fetching data or handling errors properly if the API is down.
- [x] 4.2 Create the KPI overview section using `st.container(horizontal=True)` and `st.metric` cards. Verify metrics render correctly using the fetched data.

## 5. UI Implementation: Filtering and Visualization

- [x] 5.1 Add sidebar filters (e.g., date range, severity level) to dynamically filter the fetched anomalies dataframe. Verify the dataframe updates when filters change.
- [x] 5.2 Add visualizations (e.g., bar chart of anomalies by severity or line chart over time) using native Streamlit chart components. Verify charts render correctly.
- [x] 5.3 Display the filtered anomalies in a data table (`st.dataframe` or `st.data_editor(disabled=True)`). Verify the table correctly reflects the active filters.

## 6. Testing and Validation

- [x] 6.1 Start the entire stack with `docker compose up` and verify that accessing `http://localhost/` loads the dark-themed dashboard.
- [x] 6.2 Verify that clicking the Swagger link navigates correctly to the FastAPI documentation.
- [x] 6.3 Register a new anomaly via Swagger and verify it appears in the dashboard (after the cache TTL or a manual refresh).
