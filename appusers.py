from sqlalchemy.dialects.postgresql import UUID
import UUID
import marshmallow as ma

from db import db

class AppUsers(db.Model):
  __tablename__ = "appusers"
  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  first_name = db.Column(db.String(), nullable = False)
  last_name = db.Column(db.String(), nullable = False)
  email = db.Column(db.String(), nullable = False)
  password = db.Column(db.String(), nullable = False)
  city = db.Column(db.String(), nullable = False)
  state = db.Column(db.String(), nullable = False)
  role = db.Column(db.String(), nullable = False)
  org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations'))
  active = db.Column(db.Boolean(), default = False)
  
  def __init__(self, name, phone, city, state, active = True):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.city = city
    self.state = state
    self.role = role 
    self.active = active

class AppUsersSchema(ma.Schema):
  class Meta:
    fields = ['org_id', 'name', 'phone', 'city', 'state', 'active']

appuser_schema = AppUsersSchema()
appusers_schema = AppUsersSchema(many=True)
