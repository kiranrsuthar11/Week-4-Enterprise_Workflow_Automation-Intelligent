import logging
from pathlib import Path
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, employees, documents, workflows, reports

Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, filename="logs/application.log",
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PY-W4-004 Enterprise Workflow Automation", version="1.0.0",
              description="Employee and department management, secure document processing, approval workflows, and business reporting. Register the first user to bootstrap the local demo administrator account.")

@app.get("/")
def health():
    return {"status": "ok", "project": "PY-W4-004"}

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(documents.router)
app.include_router(workflows.router)
app.include_router(reports.router)
