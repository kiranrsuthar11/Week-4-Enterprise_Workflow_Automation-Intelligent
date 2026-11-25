from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO, BytesIO
import csv, json
from reportlab.pdfgen import canvas
from app.database import get_db
from app.models import Employee, Department, Workflow, Document, User
from app.security import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

def summary(db: Session):
    employees = db.query(Employee).all()
    departments = db.query(Department).all()
    workflows = db.query(Workflow).all()
    return {
        "total_employees": len(employees),
        "employees_by_status": {s: sum(1 for e in employees if e.status == s) for s in ["Active", "Inactive", "On Leave"]},
        "departments": {d.name: len(d.employees) for d in departments},
        "total_documents": db.query(Document).count(),
        "workflows": {s: sum(1 for w in workflows if w.status == s) for s in ["Pending", "Approved", "Rejected"]},
    }

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return summary(db)

@router.get("/employees.csv")
def employees_csv(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    output = StringIO(); writer = csv.writer(output)
    writer.writerow(["Employee Code", "Name", "Email", "Job Title", "Status", "Department"])
    for e in db.query(Employee).all():
        writer.writerow([e.employee_code, e.name, e.email, e.job_title, e.status, e.department.name if e.department else ""])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=employees.csv"})

@router.get("/summary.json")
def summary_json(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return summary(db)

@router.get("/summary.pdf")
def summary_pdf(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    data = summary(db); buffer = BytesIO(); pdf = canvas.Canvas(buffer)
    y = 800; pdf.setFont("Helvetica-Bold", 16); pdf.drawString(50, y, "Enterprise Workflow - Summary Report")
    pdf.setFont("Helvetica", 11); y -= 35
    for key, value in data.items():
        pdf.drawString(50, y, f"{key}: {json.dumps(value)}"); y -= 22
        if y < 60: pdf.showPage(); y = 800
    pdf.save(); buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=summary.pdf"})
