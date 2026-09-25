# Dashboard Module (`src/dashboard/`)

The Dashboard module is a distinct presentation layer built with Streamlit.

## Responsibilities

- **Visualization**: Renders KPIs and tables representing the health of the supply chain.
- **Interaction**: Allows users to filter anomalies and provides links to the Swagger documentation.
- **API Consumption**: Communicates strictly with the FastAPI backend over HTTP, never accessing the database directly.
