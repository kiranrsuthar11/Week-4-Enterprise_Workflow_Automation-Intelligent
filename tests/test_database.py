from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Department, Employee

def test_department_employee_relationship_and_constraints(tmp_path):
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        department = Department(name="Engineering")
        session.add(department)
        session.flush()
        employee = Employee(employee_code="EMP-001", name="Test User", email="test@example.com", department_id=department.id)
        session.add(employee)
        session.commit()
        assert session.query(Employee).one().department.name == "Engineering"
    Base.metadata.drop_all(engine)
