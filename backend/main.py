from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
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

@app.get("/api/plants")
def get_plants():
    # Mock data for power plants
    plants = [
        {"id": "p1", "name": "Grand Coulee Dam", "fuel_type": "Hydro", "capacity_mw": 6809, "lat": 47.957, "lon": -118.982, "status": "Operational"},
        {"id": "p2", "name": "Palo Verde Generating Station", "fuel_type": "Nuclear", "capacity_mw": 3937, "lat": 33.388, "lon": -112.861, "status": "Operational"},
        {"id": "p3", "name": "Scherer Power Plant", "fuel_type": "Coal", "capacity_mw": 3520, "lat": 33.058, "lon": -83.807, "status": "Maintenance"},
        {"id": "p4", "name": "Alta Wind Energy Center", "fuel_type": "Wind", "capacity_mw": 1548, "lat": 35.016, "lon": -118.316, "status": "Operational"},
        {"id": "p5", "name": "Solar Star", "fuel_type": "Solar", "capacity_mw": 579, "lat": 34.811, "lon": -118.375, "status": "Operational"},
        {"id": "p6", "name": "WA Parish Generating Station", "fuel_type": "Gas", "capacity_mw": 3653, "lat": 29.477, "lon": -95.632, "status": "Operational"},
        {"id": "p7", "name": "Vogtle Electric Generating Plant", "fuel_type": "Nuclear", "capacity_mw": 4536, "lat": 33.142, "lon": -81.761, "status": "Operational"},
        {"id": "p8", "name": "Ocotillo Wind Energy Facility", "fuel_type": "Wind", "capacity_mw": 315, "lat": 32.793, "lon": -116.002, "status": "Outage"},
        {"id": "p9", "name": "Topaz Solar Farm", "fuel_type": "Solar", "capacity_mw": 550, "lat": 35.385, "lon": -120.068, "status": "Operational"},
        {"id": "p10", "name": "Monroe Power Plant", "fuel_type": "Coal", "capacity_mw": 3280, "lat": 41.889, "lon": -83.346, "status": "Operational"}
    ]
    
    # Return as GeoJSON
    features = []
    for p in plants:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p["lon"], p["lat"]]
            },
            "properties": p
        })
        
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/fuel-mix")
def get_fuel_mix():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "mix": [
            {"source": "Natural Gas", "percentage": 39, "category": "Brown"},
            {"source": "Coal", "percentage": 19, "category": "Brown"},
            {"source": "Nuclear", "percentage": 18, "category": "Green"},
            {"source": "Wind", "percentage": 10, "category": "Green"},
            {"source": "Hydro", "percentage": 6, "category": "Green"},
            {"source": "Solar", "percentage": 4, "category": "Green"},
            {"source": "Other", "percentage": 4, "category": "Brown"}
        ],
        "summary": {
            "green_percentage": 38,
            "brown_percentage": 62,
            "carbon_intensity_gCO2_kWh": 385
        }
    }

@app.get("/api/outages")
def get_outages():
    now = datetime.datetime.now()
    return [
        {
            "id": "out-1",
            "time": (now - datetime.timedelta(hours=2)).strftime("%H:%M"),
            "region": "ERCOT (Texas)",
            "event": "Unexpected plant trip (Gas)",
            "impact_mw": 450,
            "status": "Investigating",
            "severity": "High"
        },
        {
            "id": "out-2",
            "time": (now - datetime.timedelta(hours=5)).strftime("%H:%M"),
            "region": "CAISO (California)",
            "event": "Transmission line fault",
            "impact_mw": 120,
            "status": "Resolved",
            "severity": "Medium"
        },
        {
            "id": "out-3",
            "time": (now - datetime.timedelta(hours=12)).strftime("%H:%M"),
            "region": "PJM (Mid-Atlantic)",
            "event": "Scheduled Maintenance (Coal)",
            "impact_mw": 800,
            "status": "Ongoing",
            "severity": "Low"
        },
        {
            "id": "out-4",
            "time": (now - datetime.timedelta(hours=24)).strftime("%H:%M"),
            "region": "NYISO (New York)",
            "event": "Wind curtailment due to congestion",
            "impact_mw": 300,
            "status": "Ongoing",
            "severity": "Medium"
        }
    ]

@app.get("/api/intelligence")
def get_intelligence():
    return {
        "insight_a": "Energy is the Foundation of Economic Growth—an unstable or carbon-heavy grid is a long-term risk to capital.",
        "insight_b": "The Ministry of Power, Grid Operators (ISOs/RTOs), and utility companies manage the physical assets."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
