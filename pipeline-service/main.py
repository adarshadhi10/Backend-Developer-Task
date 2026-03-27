from fastapi import FastAPI, HTTPException
from database import SessionLocal, engine
from models.customer import Customer
from services.ingestion import fetch_all_customers
from sqlalchemy.orm import Session

app = FastAPI()
Customer.metadata.create_all(bind=engine)

@app.post("/api/ingest")
def ingest():
    db: Session = SessionLocal()
    try:
        customers = fetch_all_customers()

        for c in customers:
            existing = db.get(Customer, c["customer_id"])
            if existing:
                for key, value in c.items():
                    setattr(existing, key, value)
            else:
                db.add(Customer(**c))

        db.commit()
        return {"status": "success", "records_processed": len(customers)}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()
    query = db.query(Customer)
    total = query.count()
    data = query.offset((page - 1) * limit).limit(limit).all()
    db.close()

    return {
        "data": [c.__dict__ for c in data],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()
    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Not found")

    db.close()
    return customer.__dict__
