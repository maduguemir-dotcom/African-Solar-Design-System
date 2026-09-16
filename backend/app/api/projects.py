from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse

router = APIRouter()

@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(
        Project.owner_id == current_user.id,
        Project.is_active == True
    ).offset(skip).limit(limit).all()
    
    total = db.query(Project).filter(
        Project.owner_id == current_user.id,
        Project.is_active == True
    ).count()
    
    return {"projects": projects, "total": total}

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.projects_created >= current_user.max_projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project limit reached. Upgrade your plan for more projects."
        )
    
    appliances_dict = None
    if project_data.appliances:
        appliances_dict = [appliance.dict() for appliance in project_data.appliances]
    
    new_project = Project(
        owner_id=current_user.id,
        name=project_data.name,
        description=project_data.description,
        location_name=project_data.location_name,
        latitude=project_data.latitude,
        longitude=project_data.longitude,
        daily_consumption_kwh=project_data.daily_consumption_kwh,
        peak_load_kw=project_data.daily_consumption_kwh / 4 if project_data.daily_consumption_kwh else None,
        appliances=appliances_dict,
        system_type=project_data.system_type,
        battery_autonomy_days=project_data.battery_autonomy_days,
        battery_dod=project_data.battery_dod
    )
    
    db.add(new_project)
    current_user.projects_created += 1
    db.commit()
    db.refresh(new_project)
    
    return new_project

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id,
        Project.is_active == True
    ).first()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
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
    
    project.is_active = False
    db.commit()
    
    return None
