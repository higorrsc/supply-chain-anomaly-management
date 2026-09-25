# Nginx Reverse Proxy (`nginx/`)

This directory contains the Nginx configuration files used to route traffic within the Docker ecosystem.

## Role

Nginx serves as the single entry point for the application, exposing port `80` to the host machine. It securely routes internal traffic without exposing the backend or database ports directly.

- `/api/*`, `/docs`, `/openapi.json` -> Proxied to the `api` container (FastAPI)
- `/` -> Proxied to the `dashboard` container (Streamlit, including WebSocket upgrades)
