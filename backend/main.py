from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import datetime

app = FastAPI(title="Energy Infrastructure Watchtower API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnergyDataGenerator:
    """
    Synthetic Data Generator for the Energy Infrastructure Watchtower.
    Generates realistic energy asset data based on North American grid patterns.
    """

    OPERATORS = [
        "NextGrid", "NorthPower", "Vanguard Energy", "TerraWatts",
        "Apex Utility", "Core Power", "BlueHorizon", "Summit Energy"
    ]

    # Regional coordinate ranges — tightened to keep all plants on the
    # North American landmass and away from ocean areas.
    # Format: [lat_min, lat_max, lon_min, lon_max]
    REGIONS = {
        # Arizona, New Mexico, W. Texas, S. Nevada — avoids Gulf of California
        "Southwest": {"coords": [31.5, 37.0, -114.0, -103.0], "fuels": ["Solar", "Gas"]},
        # Great Plains & Upper Midwest — fully continental
        "Midwest":   {"coords": [38.0, 48.0, -104.0, -85.0],  "fuels": ["Wind", "Coal", "Gas"]},
        # Oregon & California inland valleys — avoids the Pacific shelf
        "Pacific":   {"coords": [34.0, 48.0, -122.0, -119.0], "fuels": ["Solar", "Hydro", "Wind"]},
        # Pennsylvania to Maine corridor — avoids open Atlantic
        "Northeast": {"coords": [40.5, 46.0, -79.0, -68.0],   "fuels": ["Nuclear", "Hydro", "Gas"]},
        # Carolinas, Georgia, Tennessee — avoids Gulf coast & Atlantic seaboard
        "Southeast": {"coords": [30.5, 35.5, -89.0, -77.0],   "fuels": ["Nuclear", "Gas", "Solar"]},
    }

    FUEL_STATS = {
        "Nuclear": {"range": (1000, 3500), "status": [95, 3,  2]},   # Very stable
        "Coal":    {"range": (500,  2500), "status": [80, 15, 5]},
        "Gas":     {"range": (200,  1800), "status": [90, 8,  2]},
        "Hydro":   {"range": (100,  2000), "status": [92, 6,  2]},
        "Wind":    {"range": (50,   600),  "status": [85, 10, 5]},
        "Solar":   {"range": (20,   400),  "status": [98, 1,  1]},
    }

    ISO_NAMES = ["ERCOT", "CAISO", "PJM", "NYISO", "SPP", "MISO", "IESO"]

    def __init__(self, plant_count=30):
        self.plants = self._generate_synthetic_plants(plant_count)

    def _generate_synthetic_plants(self, count):
        plants = []
        for i in range(count):
            # Select a random region
            region_name = random.choice(list(self.REGIONS.keys()))
            region = self.REGIONS[region_name]

            # Select fuel based on regional bias
            fuel = random.choice(region["fuels"])
            stats = self.FUEL_STATS[fuel]

            # Generate coordinates within region bounding box
            lat = random.uniform(region["coords"][0], region["coords"][1])
            lon = random.uniform(region["coords"][2], region["coords"][3])

            # Name generation
            operator = random.choice(self.OPERATORS)
            identifier = random.randint(100, 999)
            name = f"{operator} {fuel} Unit {identifier}"

            # Status weighted by fuel reliability profile
            status = random.choices(
                ["Operational", "Maintenance", "Outage"],
                weights=stats["status"]
            )[0]

            plants.append({
                "id": f"ep-{i:03d}",
                "name": name,
                "fuel_type": fuel,
                "capacity_mw": random.randint(stats["range"][0], stats["range"][1]),
                "lat": round(lat, 4),
                "lon": round(lon, 4),
                "status": status,
                "region": region_name,
            })
        return plants

    def get_geojson(self):
        features = []
        for p in self.plants:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [p["lon"], p["lat"]]
                },
                "properties": p
            })
        return {"type": "FeatureCollection", "features": features}

    def get_fuel_mix(self):
        # Weighted fuel mix representing North American baseline
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

    def get_outages(self):
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
                "region": random.choice(self.ISO_NAMES),
                "event": random.choice(events),
                "impact_mw": random.randint(100, 1200),
                "status": random.choice(["Ongoing", "Investigating", "Monitoring"]),
                "severity": severity,
            })
        return sorted(outages, key=lambda x: x["time"], reverse=True)


# ---------------------------------------------------------------------------
# Generator instance
# ---------------------------------------------------------------------------
generator = EnergyDataGenerator(plant_count=30)


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------
@app.get("/api/plants")
def get_plants():
    return generator.get_geojson()


@app.get("/api/fuel-mix")
def get_fuel_mix():
    return generator.get_fuel_mix()


@app.get("/api/outages")
def get_outages():
    return generator.get_outages()


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
