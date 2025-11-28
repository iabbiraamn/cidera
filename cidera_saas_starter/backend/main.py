from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="CIDERA API", version="0.1.0")

class MicrogridConfig(BaseModel):
    name: str
    description: Optional[str] = None
    raw_config: dict

class ControllerParams(BaseModel):
    gains: dict

class Scenario(BaseModel):
    name: str
    type: str
    params: dict

class SimulationRequest(BaseModel):
    microgrid: MicrogridConfig
    controller: ControllerParams
    scenario: Scenario

class SimulationResult(BaseModel):
    time: List[float]
    freq_hz: List[float]
    v_bus: List[float]
    cost_score: float

class TuningRequest(BaseModel):
    microgrid: MicrogridConfig
    scenario: Scenario
    iterations: int = 20

class TuningResult(BaseModel):
    best_gains: dict
    best_cost: float

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "cidera-api"}

@app.post("/api/simulate", response_model=SimulationResult)
async def simulate(req: SimulationRequest):
    t = [i * 0.1 for i in range(100)]
    freq = [60.0 + 0.1 * (1.0 if i < 20 else -1.0) for i in range(100)]
    vbus = [1.0 for _ in range(100)]
    cost = 12.34
    return SimulationResult(time=t, freq_hz=freq, v_bus=vbus, cost_score=cost)

@app.post("/api/tune", response_model=TuningResult)
async def tune(req: TuningRequest):
    dummy_best = {
        "Kp_freq": 1e-4,
        "Ki_freq": 1e-6,
        "Kp_volt": 5.0,
        "Ki_volt": 0.1,
    }
    return TuningResult(best_gains=dummy_best, best_cost=10.5)
