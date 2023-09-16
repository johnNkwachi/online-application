from uuid import uuid4
import uuid
from fastapi import FastAPI, HTTPException
import random
import os
import json
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder
from fastapi import File, UploadFile, Form
from datetime import date

app = FastAPI()

class Contact_Form(BaseModel):
   first_name: str
   last_name: str
   email: EmailStr
   phone_number: str
   message: str
   user_id: Optional[str] = uuid4().hex

class Application_Form(BaseModel):
    first_name: str
    last_name: str
    Email: EmailStr
    phone_number: str
    gender_selection: Literal["male", "female", "unknown"]
    marital_status: Literal["married", "single"]
    street_address: str 
    state: str
    city: str
    Zip_code: int
    date_of_birth: date
    social_code_number: int
    qualification: Literal["bachelor degree", "master degree", "phd degree"]
    cv_upload: UploadFile
    Guarantors_name: str
    Guarantors_address: str
    Guarantors_phone_number: str
    Guarantors_email: str
    Select_fulltime_part_time: Literal["fulltime", "part time"]
    Select_when_to_start: Literal["NOW", "LATER"]
    Select_duration_to_work: Literal["6", "1year"]
    Select_ID_type: Literal["PVC", "Voters card", "NIN", "International passport"]
    Front_ID_upload: UploadFile
    Back_ID_upload: UploadFile
    Selfie_upload: UploadFile
    user_id: str
    user_id: str = Field(..., description="User ID of the applicant (contact form user)")
    

USER_FILE = "user.json"
CONTACT_DATABASE =[]

if os.path.exists(USER_FILE):
   with open(USER_FILE, 'r') as f:
      CONTACT_DATABASE = json.load(f)

APPLICATION_FILE = "application.json"
APPLICATION_DATABASE =[]

if os.path.exists(APPLICATION_FILE):
   with open(APPLICATION_FILE, 'r') as f:
      APPLICATION_DATABASE = json.load(f)

@app.get("/")
def home():
    return {"Welcome To My Application"}

@app.get("/contact-form")
def contact_form():
    return {"Contact": CONTACT_DATABASE}

@app.get("/contact-by-index/{index}")
def contact_by_index(index: int):
     if index < 0 or index >= len(CONTACT_DATABASE):
        raise HTTPException(404, f"Index {index} is out of range {len(CONTACT_DATABASE)}")
     else: 
      return {"contact": [CONTACT_DATABASE[index]]}


# create a new user 
@app.post("/add-new-user")
def add_new_user(user: Contact_Form):
   user.user_id = uuid4().hex
   json_user = jsonable_encoder(user)
   CONTACT_DATABASE.append(json_user)
   with open(USER_FILE, 'w') as f:
      json.dump(CONTACT_DATABASE, f)
   return {"message": f"{user} was added successfully", "user_id": user.user_id}


@app.get("/get-contact-from")
def get_contact_from(user_id: str):
   for contact in CONTACT_DATABASE:
      if contact["user_id"] == user_id:
         return contact
   raise HTTPException(404, f" user not found: {user_id}")  


# create a new new application
@app.post("/create-new-application")
def create_new_application(application: Application_Form, user_id: str):
   application.user_id = user_id
   json_user = jsonable_encoder(application)
   APPLICATION_DATABASE.append(json_user)
   with open(APPLICATION_FILE, 'w') as f:
      json.dump(APPLICATION_DATABASE, f)
   return {"message": f"{application} was added successfully", "user_id": application.user_id}

@app.get("/get-forms/{user_id}")
def get_forms(user_id: str):
   contact_form = None
   application_form = None

    # Search for the contact form with the specified user_id
   for contact in CONTACT_DATABASE:
        if contact["user_id"] == user_id:
            contact_form = contact
            break

    # Search for the application form with the specified user_id
   for application in APPLICATION_DATABASE:
        if application["user_id"] == user_id:
            application_form = application
            break

   if not contact_form and not application_form:
        raise HTTPException(404, f"User with user_id {user_id} not found.")

   return {"contact_form": contact_form, "application_form": application_form}
    

