from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    daily_consumption_kwh = Column(Float, nullable=True)
    peak_load_kw = Column(Float, nullable=True)
    appliances = Column(JSON, nullable=True)
    system_type = Column(String, default="hybrid")
    battery_autonomy_days = Column(Float, default=2.0)
    battery_dod = Column(Float, default=0.5)
    peak_sun_hours = Column(Float, nullable=True)
    solar_irradiance = Column(Float, nullable=True)
    pv_capacity_kw = Column(Float, nullable=True)
    num_pv_panels = Column(Integer, nullable=True)
    pv_panel_wattage = Column(Float, default=400)
    battery_capacity_kwh = Column(Float, nullable=True)
    battery_voltage = Column(Float, default=48.0)
    inverter_capacity_kw = Column(Float, nullable=True)
    charge_controller_rating = Column(Float, nullable=True)
    total_system_cost = Column(Float, nullable=True)
    pv_panel_cost = Column(Float, nullable=True)
    battery_cost = Column(Float, nullable=True)
    inverter_cost = Column(Float, nullable=True)
    installation_cost = Column(Float, nullable=True)
    electricity_tariff = Column(Float, nullable=True)
    monthly_savings = Column(Float, nullable=True)
    payback_period_years = Column(Float, nullable=True)
    roi_percentage = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    is_template = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="projects")
