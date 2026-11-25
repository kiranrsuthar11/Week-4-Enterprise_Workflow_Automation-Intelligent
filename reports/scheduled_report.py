"""Generate a point-in-time report; schedule this module with Windows Task Scheduler/cron."""
from datetime import datetime
import csv
import json
from pathlib import Path

from app.database import SessionLocal
from app.models import Department, Document, Employee, Workflow
from reports.report_generator import generate_text_pdf


def generate_scheduled_reports() -> dict[str, str]:
    output_dir = Path("reports/generated")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with SessionLocal() as db:
        employees = db.query(Employee).all()
        departments = db.query(Department).all()
        documents = db.query(Document).count()
        workflows = db.query(Workflow).all()
        summary = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "total_employees": len(employees),
            "departments": {d.name: len(d.employees) for d in departments},
            "total_documents": documents,
            "workflows": {status: sum(w.status == status for w in workflows) for status in ("Pending", "Approved", "Rejected")},
        }
        csv_path = output_dir / f"employees_{timestamp}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["employee_code", "name", "email", "job_title", "status", "department"])
            for employee in employees:
                writer.writerow([employee.employee_code, employee.name, employee.email, employee.job_title,
                                 employee.status, employee.department.name if employee.department else ""])
        json_path = output_dir / f"summary_{timestamp}.json"
        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        pdf_path = output_dir / f"summary_{timestamp}.pdf"
        generate_text_pdf(["PY-W4-004 Scheduled Summary", *json.dumps(summary, indent=2).splitlines()], str(pdf_path))
    return {"csv": str(csv_path), "json": str(json_path), "pdf": str(pdf_path)}


if __name__ == "__main__":
    for kind, path in generate_scheduled_reports().items():
        print(f"{kind.upper()} report: {path}")
