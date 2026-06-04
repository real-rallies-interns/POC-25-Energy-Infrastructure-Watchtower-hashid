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


def _load_geojson() -> dict:
    """Read and return the GeoJSON FeatureCollection from data.json."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Standalone helpers for fuel-mix and outage data (still synthetic/live)
# ---------------------------------------------------------------------------
_ISO_NAMES = ["ERCOT", "CAISO", "PJM", "NYISO", "SPP", "MISO", "IESO"]


def _build_fuel_mix() -> dict:
    """Weighted fuel mix representing a North American baseline."""
    sources = [
        ("Natural Gas", 39, "Brown"),
        ("Nuclear",     19, "Green"),
        ("Coal",        18, "Brown"),
        ("Wind",        11, "Green"),
        ("Hydro",        6, "Green"),
        ("Solar",        4, "Green"),
        ("Other",        3, "Brown"),
    ]

    mix = []
    total = 0
    for source, base, category in sources:
        val = max(1, base + random.randint(-2, 2))
        mix.append({"source": source, "percentage": val, "category": category})
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
    """Generate a random set of live outage events."""
    events = [
        "Thermal trip", "Grid frequency drop", "Substation maintenance",
        "Transmission line derating", "Inverter failure", "Turbine vibration alert",
    ]
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
    return {
        "insight_a": (
            "Energy is the Foundation of Economic Growth—an unstable or "
            "carbon-heavy grid is a long-term risk to capital."
        ),
        "insight_b": (
            "The Ministry of Power, Grid Operators (ISOs/RTOs), and utility "
            "companies manage the physical assets."
        ),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
