from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.pdf_generator import generate_solar_report
from app.services.solar_calculator import SolarCalculator
import os
import tempfile

router = APIRouter()

@router.get("/project/{project_id}/pdf")
async def generate_project_report(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    if not all([project.pv_capacity_kw, project.battery_capacity_kwh, project.inverter_capacity_kw]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project design not calculated yet")
    
    calculator = SolarCalculator()
    design = calculator.complete_system_design(
        daily_consumption_kwh=project.daily_consumption_kwh or 10,
        peak_sun_hours=project.peak_sun_hours or 5.0,
        peak_load_kw=project.peak_load_kw or 2.5,
        system_type=project.system_type,
        autonomy_days=project.battery_autonomy_days,
        dod=project.battery_dod
    )
    
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"solar_design_{project_id}.pdf")
    
    report_path = generate_solar_report(
        output_path=output_path,
        project_name=project.name,
        design_data=design,
        customer_name=project.owner.full_name,
        location=project.location_name
    )
    
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"solar_design_{project.name.replace(' ', '_')}.pdf"
    )
