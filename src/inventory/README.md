# Inventory Module (`src/inventory/`)

The Inventory bounded context is responsible for tracking the physical reality of the supply chain.

## Domain Concepts

- **Item**: A distinct product or SKU.
- **Warehouse**: A location where items are stored.
- **Movement**: A transaction (Inbound/Outbound) representing a change in stock levels.

*Note: Movements trigger domain events which are asynchronously analyzed by the Anomaly module.*
