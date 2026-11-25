from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import Employee, Department, User
from app.schemas import EmployeeIn, EmployeeOut, DepartmentIn
from app.security import get_current_user, require_admin

router = APIRouter(tags=["Employees & Departments"])

@router.post("/departments", status_code=201)
def create_department(data: DepartmentIn, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    if db.query(Department).filter(Department.name.ilike(data.name)).first():
        raise HTTPException(409, "Department already exists")
    item = Department(name=data.name.strip())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id, "name": item.name}

@router.get("/departments")
def list_departments(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Department).order_by(Department.name).all()

@router.post("/employees", response_model=EmployeeOut, status_code=201)
def create_employee(data: EmployeeIn, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    if data.status not in {"Active", "Inactive", "On Leave"}:
        raise HTTPException(422, "Status must be Active, Inactive, or On Leave")
    if db.query(Employee).filter(or_(Employee.employee_code == data.employee_code, Employee.email == data.email)).first():
        raise HTTPException(409, "Employee code or email already exists")
    if data.department_id and not db.get(Department, data.department_id):
        raise HTTPException(404, "Department not found")
    item = Employee(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/employees", response_model=list[EmployeeOut])
def list_employees(q: str | None = None, department_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Employee)
    if q:
        query = query.filter(or_(Employee.name.ilike(f"%{q}%"), Employee.employee_code.ilike(f"%{q}%"), Employee.email.ilike(f"%{q}%")))
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    return query.order_by(Employee.id.desc()).all()

@router.get("/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.get(Employee, employee_id)
    if not item: raise HTTPException(404, "Employee not found")
    return item

@router.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeIn, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    item = db.get(Employee, employee_id)
    if not item: raise HTTPException(404, "Employee not found")
    if data.status not in {"Active", "Inactive", "On Leave"}:
        raise HTTPException(422, "Status must be Active, Inactive, or On Leave")
    if data.department_id and not db.get(Department, data.department_id):
        raise HTTPException(404, "Department not found")
    duplicate = db.query(Employee).filter(Employee.id != employee_id, or_(Employee.employee_code == data.employee_code, Employee.email == data.email)).first()
    if duplicate: raise HTTPException(409, "Employee code or email already exists")
    for key, value in data.model_dump().items(): setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    item = db.get(Employee, employee_id)
    if not item: raise HTTPException(404, "Employee not found")
    db.delete(item); db.commit()
    return {"message": "Employee deleted"}
