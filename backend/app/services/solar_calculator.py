from typing import Dict, Optional
from dataclasses import dataclass
import math

class SolarCalculator:
    """Solar PV System Designer for African conditions"""
    
    DEFAULT_PV_WATTAGE = 400
    DEFAULT_BATTERY_VOLTAGE = 48
    DEFAULT_INVERTER_EFFICIENCY = 0.95
    DEFAULT_SYSTEM_LOSS = 0.14
    
    COST_PER_WATT_PV = 0.80
    COST_PER_KWH_BATTERY = 300
    COST_PER_KW_INVERTER = 200
    INSTALLATION_PERCENTAGE = 0.15
    
    def __init__(self):
        self.pv_wattage = self.DEFAULT_PV_WATTAGE
        self.battery_voltage = self.DEFAULT_BATTERY_VOLTAGE
        self.inverter_efficiency = self.DEFAULT_INVERTER_EFFICIENCY
        self.system_loss = self.DEFAULT_SYSTEM_LOSS
    
    def calculate_pv_sizing(self, daily_consumption_kwh: float, peak_sun_hours: float, 
                           system_type: str = "hybrid", pv_panel_wattage: Optional[float] = None) -> Dict:
        if pv_panel_wattage:
            self.pv_wattage = pv_panel_wattage
        
        effective_consumption = daily_consumption_kwh / (1 - self.system_loss)
        
        if system_type == "hybrid":
            effective_consumption *= 1.2
        elif system_type == "grid":
            effective_consumption *= 1.3
        
        pv_capacity_kw = effective_consumption / peak_sun_hours
        num_panels = math.ceil((pv_capacity_kw * 1000) / self.pv_wattage)
        actual_pv_capacity_kw = (num_panels * self.pv_wattage) / 1000
        daily_production = actual_pv_capacity_kw * peak_sun_hours * self.inverter_efficiency
        annual_production = daily_production * 365
        
        return {
            "pv_capacity_kw": round(pv_capacity_kw, 2),
            "actual_pv_capacity_kw": round(actual_pv_capacity_kw, 2),
            "num_pv_panels": num_panels,
            "pv_panel_wattage": self.pv_wattage,
            "daily_production_kwh": round(daily_production, 2),
            "annual_production_kwh": round(annual_production, 2)
        }
    
    def calculate_battery_sizing(self, daily_consumption_kwh: float, autonomy_days: float = 2.0,
                                dod: float = 0.5, battery_voltage: Optional[float] = None) -> Dict:
        if battery_voltage:
            self.battery_voltage = battery_voltage
        
        usable_capacity = daily_consumption_kwh * autonomy_days
        total_capacity_kwh = (usable_capacity / dod) * 1.2
        battery_capacity_ah = (total_capacity_kwh * 1000) / self.battery_voltage
        
        return {
            "battery_capacity_kwh": round(total_capacity_kwh, 2),
            "usable_capacity_kwh": round(usable_capacity, 2),
            "battery_voltage": self.battery_voltage,
            "battery_capacity_ah": round(battery_capacity_ah, 2),
            "autonomy_days": autonomy_days,
            "dod": dod
        }
    
    def calculate_inverter_sizing(self, peak_load_kw: float, pv_capacity_kw: float, 
                                 system_type: str = "hybrid") -> Dict:
        inverter_capacity = peak_load_kw * 1.25
        dc_ac_ratio = pv_capacity_kw / inverter_capacity
        
        if dc_ac_ratio < 1.1:
            inverter_capacity = pv_capacity_kw / 1.15
        
        inverter_capacity = max(inverter_capacity, peak_load_kw)
        
        return {
            "inverter_capacity_kw": round(inverter_capacity, 2),
            "dc_ac_ratio": round(dc_ac_ratio, 2)
        }
    
    def calculate_charge_controller(self, pv_capacity_kw: float, battery_voltage: float,
                                   controller_type: str = "mppt") -> Dict:
        efficiency = 0.95 if controller_type == "mppt" else 0.80
        current = (pv_capacity_kw * 1000) / (battery_voltage * efficiency)
        current *= 1.25
        
        return {
            "charge_controller_current": round(current, 2),
            "controller_type": controller_type.upper(),
            "battery_voltage": battery_voltage
        }
    
    def calculate_financial_analysis(self, pv_capacity_kw: float, battery_capacity_kwh: float,
                                    inverter_capacity_kw: float, daily_consumption_kwh: float,
                                    electricity_tariff: float = 0.15) -> Dict:
        pv_cost = pv_capacity_kw * 1000 * self.COST_PER_WATT_PV
        battery_cost = battery_capacity_kwh * self.COST_PER_KWH_BATTERY
        inverter_cost = inverter_capacity_kw * self.COST_PER_KW_INVERTER
        equipment_cost = pv_cost + battery_cost + inverter_cost
        installation_cost = equipment_cost * self.INSTALLATION_PERCENTAGE
        total_cost = equipment_cost + installation_cost
        
        annual_production = daily_consumption_kwh * 365
        annual_savings = annual_production * electricity_tariff
        monthly_savings = annual_savings / 12
        payback_years = total_cost / annual_savings if annual_savings > 0 else float("inf")
        
        total_savings_25_years = annual_savings * 25
        roi_25_years = ((total_savings_25_years - total_cost) / total_cost) * 100
        co2_avoided_tons = (annual_production * 0.5 / 1000) * 25
        
        return {
            "total_system_cost": round(total_cost, 2),
            "pv_panel_cost": round(pv_cost, 2),
            "battery_cost": round(battery_cost, 2),
            "inverter_cost": round(inverter_cost, 2),
            "installation_cost": round(installation_cost, 2),
            "monthly_savings": round(monthly_savings, 2),
            "annual_savings": round(annual_savings, 2),
            "payback_period_years": round(payback_years, 2) if payback_years != float("inf") else None,
            "roi_25_years_percentage": round(roi_25_years, 2),
            "co2_avoided_25_years_tons": round(co2_avoided_tons, 2)
        }
    
    def complete_system_design(self, daily_consumption_kwh: float, peak_sun_hours: float,
                              peak_load_kw: float, system_type: str = "hybrid",
                              autonomy_days: float = 2.0, dod: float = 0.5,
                              electricity_tariff: float = 0.15) -> Dict:
        pv_results = self.calculate_pv_sizing(daily_consumption_kwh, peak_sun_hours, system_type)
        battery_results = self.calculate_battery_sizing(daily_consumption_kwh, autonomy_days, dod)
        inverter_results = self.calculate_inverter_sizing(peak_load_kw, pv_results["pv_capacity_kw"], system_type)
        controller_results = self.calculate_charge_controller(pv_results["pv_capacity_kw"], self.battery_voltage)
        financial_results = self.calculate_financial_analysis(
            pv_results["pv_capacity_kw"], battery_results["battery_capacity_kwh"],
            inverter_results["inverter_capacity_kw"], daily_consumption_kwh, electricity_tariff
        )
        
        return {
            "pv_system": pv_results,
            "battery_system": battery_results,
            "inverter_system": inverter_results,
            "charge_controller": controller_results,
            "financial_analysis": financial_results,
            "system_type": system_type,
            "daily_consumption_kwh": daily_consumption_kwh,
            "peak_sun_hours": peak_sun_hours
        }

def design_solar_system(daily_kwh: float, sun_hours: float, peak_kw: float, 
                       system_type: str = "hybrid") -> Dict:
    calculator = SolarCalculator()
    return calculator.complete_system_design(
        daily_consumption_kwh=daily_kwh,
        peak_sun_hours=sun_hours,
        peak_load_kw=peak_kw,
        system_type=system_type
    )
