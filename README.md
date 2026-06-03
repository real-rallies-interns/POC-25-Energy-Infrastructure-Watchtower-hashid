# Real Rails: Energy Infrastructure Watchtower (PoC #25)

A professional decoupled geospatial monitoring dashboard focusing on real-time telemetry extraction, grid health analysis, and high-throughput asset visualization across North American power networks.

---

## ⚡ Core Technical Features

### 1. Advanced Synthetic Data Matrix (`main.py`)
* **Reviewer Feedback Alignment:** Completely eliminates static hardcoding of coordinates and metadata. Replaced by a native python engine called `EnergyDataGenerator`.
* **Bounded Bounding-Boxes:** Telemetry bounds are strictly hard-fenced into specific geographic regions (Southwest, Midwest, Pacific, Northeast, Southeast) to keep all simulated energy cells inside the continental North American landmass and completely away from ocean zones.
* **Proportional Reliability Weighting:** Asset states (`Operational`, `Maintenance`, `Outage`) and electrical generation limits (MW) are computed using real-world baseline algorithms per fuel profile (e.g., Higher base loads for Nuclear, variable thresholds for Wind/Solar).

### 2. Standards-Compliant GeoJSON Data Stream
* The backend delivers spatial coordinates directly mapped into an industry-standard GeoJSON `FeatureCollection` via the `/api/plants` route. 
* This structures points seamlessly into `geometry.coordinates` and injects localized attributes into `properties`, avoiding data integration errors during render cycles.

### 3. Comprehensive Grid Dash Layer (`page.tsx`)
* **70% Main Spatial Stage:** Embeds a dark-themed Leaflet geospatial vector layer rendering custom responsive map pins with live status-ping waves for active terminal outages.
* **30% Intelligence Workspace:** Handles downstream data transformations capturing real-time aggregate carbon intensity analytics (gCO₂/kWh) and regional ISO event logs (ERCOT, CAISO, PJM, etc.).

---

## 🛠️ API & Schema Blueprint

The FastAPI tier runs natively on port `8001` and serves the following micro-routes:
* `GET /api/plants` -> Dispatches the randomized 30-node geographic asset layout inside a flat GeoJSON schema.
* `GET /api/fuel-mix` -> Normalizes dynamic baselines mapping Green vs. Brown grid dependencies.
* `GET /api/outages` -> Generates automated runtime anomaly tickets tracking active transmission failures, line deratings, and emergency drops.
* `GET /api/intelligence` -> Delivers high-level geopolitical insights regarding grid sovereignty.

---

## 💻 Tech Stack Setup
* **IDE & OS Context:** Managed and executed within the Antigravity Specialized IDE on a Windows host environment.
* **Server Infrastructure:** Uvicorn Async Workers, FastAPI Framework, Pydantic, Native Random Seed Matrices.
* **UI Interface Pipeline:** Next.js Framework, TypeScript, React Leaflet Vector Layer, TailwindCSS, Lucide Icons.