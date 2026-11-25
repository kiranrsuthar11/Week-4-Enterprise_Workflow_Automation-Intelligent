from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Workflow, WorkflowActivity, User, Document
from workflow_engine.transitions import can_transition
from workflow_engine.notifications import notify_pending
from workflow_engine.workflow_tracker import is_overdue
from app.schemas import WorkflowIn, WorkflowDecision
from app.security import get_current_user, require_admin

router = APIRouter(prefix="/workflows", tags=["Workflow"])

@router.post("", status_code=201)
def create_workflow(data: WorkflowIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if data.document_id and not db.get(Document, data.document_id):
        raise HTTPException(404, "Document not found")
    item = Workflow(title=data.title, description=data.description, document_id=data.document_id, created_by=user.id)
    db.add(item); db.flush()
    db.add(WorkflowActivity(workflow_id=item.id, actor=user.username, action="Submitted", note="Workflow created"))
    db.flush()
    notify_pending(item.id, item.title)
    db.commit(); db.refresh(item)
    return item

@router.get("")
def list_workflows(status: str | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Workflow)
    if status: query = query.filter(Workflow.status == status)
    return query.order_by(Workflow.id.desc()).all()

@router.post("/{workflow_id}/decision")
def decide_workflow(workflow_id: int, data: WorkflowDecision, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    item = db.get(Workflow, workflow_id)
    if not item: raise HTTPException(404, "Workflow not found")
    decision = data.decision.strip().lower()
    if decision not in {"approve", "reject"}: raise HTTPException(422, "Decision must be approve or reject")
    target = "Approved" if decision == "approve" else "Rejected"
    if not can_transition(item.status, target): raise HTTPException(409, "Only pending workflows can be decided")
    item.status = target
    db.add(WorkflowActivity(workflow_id=item.id, actor=user.username, action=item.status, note=data.note))
    db.commit(); db.refresh(item)
    return {"id": item.id, "status": item.status}

@router.get("/overdue")
def overdue_workflows(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(Workflow).filter(Workflow.status == "Pending").order_by(Workflow.created_at).all()
    return [{"id": item.id, "title": item.title, "created_at": item.created_at, "overdue": True}
            for item in items if is_overdue(item.created_at)]

@router.get("/{workflow_id}/history")
def workflow_history(workflow_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not db.get(Workflow, workflow_id): raise HTTPException(404, "Workflow not found")
    return db.query(WorkflowActivity).filter(WorkflowActivity.workflow_id == workflow_id).order_by(WorkflowActivity.id).all()
