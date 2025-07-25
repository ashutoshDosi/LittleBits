"""
routers.py
Defines FastAPI routers for user authentication and core features.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas, models, auth
from .database import get_db
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user 

# --- Personalized Memory (Interactions) ---
@router.post("/interactions", response_model=schemas.InteractionOut)
def log_interaction(
    interaction: schemas.InteractionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    new_interaction = models.Interaction(
        user_id=current_user.id,
        message=interaction.message,
        response=interaction.response,
        timestamp=datetime.utcnow(),
    )
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return new_interaction

@router.get("/interactions", response_model=List[schemas.InteractionOut])
def get_interactions(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Interaction).filter(models.Interaction.user_id == current_user.id).order_by(models.Interaction.timestamp.desc()).all()

# --- Cycle/Phase Management ---
@router.post("/cycles", response_model=schemas.CycleOut)
def log_cycle(
    cycle: schemas.CycleCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    new_cycle = models.Cycle(
        user_id=current_user.id,
        start_date=cycle.start_date,
        symptoms=cycle.symptoms,
        moods=cycle.moods,
    )
    db.add(new_cycle)
    db.commit()
    db.refresh(new_cycle)
    return new_cycle

@router.get("/cycles", response_model=List[schemas.CycleOut])
def get_cycles(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Cycle).filter(models.Cycle.user_id == current_user.id).order_by(models.Cycle.start_date.desc()).all()

@router.get("/phase")
def get_current_phase(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    # Simple phase calculation based on last cycle start date
    last_cycle = db.query(models.Cycle).filter(models.Cycle.user_id == current_user.id).order_by(models.Cycle.start_date.desc()).first()
    if not last_cycle:
        return {"phase": None, "message": "No cycle data found."}
    days_since = (datetime.utcnow() - last_cycle.start_date).days
    # Example: Menstrual (0-4), Follicular (5-13), Ovulatory (14-16), Luteal (17-28)
    if days_since <= 4:
        phase = "menstrual"
    elif days_since <= 13:
        phase = "follicular"
    elif days_since <= 16:
        phase = "ovulatory"
    elif days_since <= 28:
        phase = "luteal"
    else:
        phase = "unknown"
    return {"phase": phase, "days_since": days_since}

# --- Reminders (Stub) ---
@router.post("/reminders", response_model=schemas.ReminderOut)
def create_reminder(
    reminder: schemas.ReminderCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    new_reminder = models.Reminder(
        user_id=current_user.id,
        type=reminder.type,
        time=reminder.time,
        method=reminder.method,
        active=True,
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return new_reminder

@router.get("/reminders", response_model=List[schemas.ReminderOut])
def get_reminders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Reminder).filter(models.Reminder.user_id == current_user.id).all()

# --- Partner/Supporter Features ---
@router.post("/invite-partner", response_model=schemas.PartnerOut)
def invite_partner(
    invite: schemas.PartnerInvite,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    partner_user = auth.get_user_by_email(db, invite.partner_email)
    if not partner_user:
        raise HTTPException(status_code=404, detail="Partner email not found.")
    new_partner = models.Partner(
        user_id=current_user.id,
        partner_user_id=partner_user.id,
        consent_type=invite.consent_type,
        status="pending",
    )
    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)
    return new_partner

@router.get("/partners", response_model=List[schemas.PartnerOut])
def get_partners(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    # Show partners where user is the owner
    return db.query(models.Partner).filter(models.Partner.user_id == current_user.id).all()

@router.post("/partners/{partner_id}/consent")
def update_partner_consent(
    partner_id: int,
    consent_type: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id, models.Partner.user_id == current_user.id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner relationship not found.")
    partner.consent_type = consent_type
    db.commit()
    return {"message": "Consent updated."}

@router.get("/shared-info")
def get_shared_info(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    # Show info shared with the current user as a partner
    partner_links = db.query(models.Partner).filter(models.Partner.partner_user_id == current_user.id, models.Partner.status == "accepted").all()
    shared = []
    for link in partner_links:
        owner = db.query(models.User).filter(models.User.id == link.user_id).first()
        if link.consent_type == "cycle":
            cycles = db.query(models.Cycle).filter(models.Cycle.user_id == owner.id).all()
            shared.append({"owner": owner.email, "cycles": [c.start_date.isoformat() for c in cycles]})
        # Add more types as needed
    return shared 