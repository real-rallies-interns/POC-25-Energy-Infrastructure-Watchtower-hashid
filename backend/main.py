from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import datetime
from pathlib import Path

app = FastAPI(title="Energy Infrastructure Watchtower API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# GeoJSON data source — resolved relative to this file so the server can be
# launched from any working directory.
# ---------------------------------------------------------------------------
DATA_FILE = Path(__file__).parent / "data.json"


def _load_data() -> dict:
    """Read and return the full data.json document."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_geojson() -> dict:
    """Return only the GeoJSON FeatureCollection portion of data.json."""
    data = _load_data()
    return {"type": data["type"], "features": data["features"]}


# ---------------------------------------------------------------------------
# Standalone helpers for fuel-mix and outage data (still synthetic/live)
# ---------------------------------------------------------------------------
_ISO_NAMES = ["ERCOT", "CAISO", "PJM", "NYISO", "SPP", "MISO", "IESO"]


def _build_fuel_mix() -> dict:
    """Weighted fuel mix built from baselines stored in data.json."""
    baselines = _load_data()["fuel_mix_baselines"]

    mix = []
    total = 0
    for entry in baselines:
        val = max(1, entry["base_percentage"] + random.randint(-2, 2))
        mix.append({"source": entry["source"], "percentage": val, "category": entry["category"]})
        total += val

    # Normalize to 100 %
    for item in mix:
        item["percentage"] = round((item["percentage"] / total) * 100)

    green = sum(i["percentage"] for i in mix if i["category"] == "Green")
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "mix": mix,
        "summary": {
            "green_percentage": green,
            "brown_percentage": 100 - green,
            "carbon_intensity_gCO2_kWh": random.randint(360, 410),
        },
    }


def _build_outages() -> list:
    """Generate a random set of live outage events using event types from data.json."""
    events = _load_data()["outage_event_types"]
    outages = []
    for i in range(random.randint(5, 10)):
        severity = random.choices(["High", "Medium", "Low"], weights=[15, 35, 50])[0]
        outages.append({
            "id": f"evt-{i}",
            "time": (
                datetime.datetime.now()
                - datetime.timedelta(minutes=random.randint(5, 1200))
            ).strftime("%H:%M"),
            "region": random.choice(_ISO_NAMES),
            "event": random.choice(events),
            "impact_mw": random.randint(100, 1200),
            "status": random.choice(["Ongoing", "Investigating", "Monitoring"]),
            "severity": severity,
        })
    return sorted(outages, key=lambda x: x["time"], reverse=True)


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------
@app.get("/api/plants")
def get_plants():
    """Return the static GeoJSON FeatureCollection loaded from data.json."""
    return _load_geojson()


@app.get("/api/fuel-mix")
def get_fuel_mix():
    return _build_fuel_mix()


@app.get("/api/outages")
def get_outages():
    return _build_outages()


@app.get("/api/intelligence")
def get_intelligence():
    """Return intelligence insights loaded from data.json."""
    return _load_data()["intelligence"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
