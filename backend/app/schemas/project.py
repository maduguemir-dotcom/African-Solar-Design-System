from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class Appliance(BaseModel):
    name: str
    power_watts: float
    quantity: int
    hours_per_day: float

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ProjectCreate(ProjectBase):
    daily_consumption_kwh: Optional[float] = None
    peak_load_kw: Optional[float] = None
    appliances: Optional[List[Appliance]] = None
    system_type: str = "hybrid"
    battery_autonomy_days: float = 2.0
    battery_dod: float = 0.5

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    daily_consumption_kwh: Optional[float] = None
    peak_load_kw: Optional[float] = None

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    daily_consumption_kwh: Optional[float] = None
    peak_load_kw: Optional[float] = None
    system_type: str
    battery_autonomy_days: float
    battery_dod: float
    peak_sun_hours: Optional[float] = None
    pv_capacity_kw: Optional[float] = None
    num_pv_panels: Optional[int] = None
    battery_capacity_kwh: Optional[float] = None
    inverter_capacity_kw: Optional[float] = None
    total_system_cost: Optional[float] = None
    monthly_savings: Optional[float] = None
    payback_period_years: Optional[float] = None
    roi_percentage: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
