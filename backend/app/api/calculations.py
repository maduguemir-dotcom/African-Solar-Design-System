from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.solar_calculator import SolarCalculator, design_solar_system

router = APIRouter()

@router.post("/design")
async def calculate_solar_design(
    daily_consumption_kwh: float,
    peak_sun_hours: float,
    peak_load_kw: float,
    system_type: str = "hybrid",
    autonomy_days: float = 2.0,
    dod: float = 0.5,
    electricity_tariff: float = 0.15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    calculator = SolarCalculator()
    design = calculator.complete_system_design(
        daily_consumption_kwh=daily_consumption_kwh,
        peak_sun_hours=peak_sun_hours,
        peak_load_kw=peak_load_kw,
        system_type=system_type,
        autonomy_days=autonomy_days,
        dod=dod,
        electricity_tariff=electricity_tariff
    )
    return design

@router.post("/quick-design")
async def quick_design(
    daily_kwh: float,
    sun_hours: float,
    peak_kw: float,
    system_type: str = "hybrid",
    current_user: User = Depends(get_current_user)
):
    design = design_solar_system(
        daily_kwh=daily_kwh,
        sun_hours=sun_hours,
        peak_kw=peak_kw,
        system_type=system_type
    )
    return design

@router.post("/project/{project_id}/calculate")
async def calculate_project_design(
    project_id: int,
    peak_sun_hours: Optional[float] = None,
    electricity_tariff: float = 0.15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    if not project.daily_consumption_kwh:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project missing daily consumption data")
    
    sun_hours = peak_sun_hours if peak_sun_hours else 5.0
    peak_load = project.peak_load_kw if project.peak_load_kw else project.daily_consumption_kwh / 4
    
    calculator = SolarCalculator()
    design = calculator.complete_system_design(
        daily_consumption_kwh=project.daily_consumption_kwh,
        peak_sun_hours=sun_hours,
        peak_load_kw=peak_load,
        system_type=project.system_type,
        autonomy_days=project.battery_autonomy_days,
        dod=project.battery_dod,
        electricity_tariff=electricity_tariff
    )
    
    project.peak_sun_hours = sun_hours
    project.pv_capacity_kw = design["pv_system"]["pv_capacity_kw"]
    project.num_pv_panels = design["pv_system"]["num_pv_panels"]
    project.battery_capacity_kwh = design["battery_system"]["battery_capacity_kwh"]
    project.inverter_capacity_kw = design["inverter_system"]["inverter_capacity_kw"]
    project.charge_controller_rating = design["charge_controller"]["charge_controller_current"]
    
    financials = design["financial_analysis"]
    project.total_system_cost = financials["total_system_cost"]
    project.pv_panel_cost = financials["pv_panel_cost"]
    project.battery_cost = financials["battery_cost"]
    project.inverter_cost = financials["inverter_cost"]
    project.installation_cost = financials["installation_cost"]
    project.monthly_savings = financials["monthly_savings"]
    project.payback_period_years = financials["payback_period_years"]
    project.roi_percentage = financials["roi_25_years_percentage"]
    
    db.commit()
    db.refresh(project)
    
    return {"project": project, "design": design}

@router.get("/locations/{country}")
async def get_solar_resource_by_location(
    country: str,
    current_user: User = Depends(get_current_user)
):
    solar_data = {
        "nigeria": {"lagos": 5.2, "kano": 5.8, "abuja": 5.5},
        "kenya": {"nairobi": 5.5, "mombasa": 5.8},
        "uganda": {"kampala": 5.4, "entebbe": 5.3, "gulu": 5.6},
        "ghana": {"accra": 5.3, "kumasi": 5.1, "tamale": 5.7},
        "tanzania": {"dar_es_salaam": 5.6, "dodoma": 5.9},
        "south_africa": {"johannesburg": 5.5, "cape_town": 5.4, "durban": 5.2},
    }
    
    country_lower = country.lower().replace(" ", "_")
    
    if country_lower in solar_data:
        cities = solar_data[country_lower]
        avg_sun_hours = sum(cities.values()) / len(cities)
        return {
            "country": country,
            "cities": cities,
            "average_peak_sun_hours": round(avg_sun_hours, 2),
            "note": "Peak sun hours are annual averages."
        }
    else:
        return {
            "country": country,
            "average_peak_sun_hours": 5.5,
            "note": "Default value for African region."
        }
