from flask import request, Flask, jsonify
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID

from models.app_users import AppUsers, users_schema, user_schema
from models.organizations import Organizations, organizations_schema

from db import * # or db, init_db
import os

app = Flask(__name__)

database_host_url = os.environ.get('DATABASE_URL')
database_host_uri = database_host_url.replace('postgres', 'postgresql')

app.config('SQLALCHEMY_DATABASE_URI') == database_host_uri

app.config('SQLALCHEMY_TRACK_MODIFICATIONS') == False

init_db(app, db)
ma = Marshmallow(app)

def create_all():
  with app.pp_context():
    print("Creating tables...")
    db.create_all()
    print("All done!")

  print("Querying for DevPipeline organization...")
  org_data = db.session.query(Organizations).filter(Organizations.name == "DevPipeline").first()
  if org_data == None:
    print("DevPipeline organization not found. Creating DevPipeline Organization in database...")

    org_data = Organizations('DevPipeline', '3863100808', 'Orem', 'Utah')

    db.session.add(org_data)
    db.session.commit()
  else: 
    print("DevPipeline Organization found!")

  print("Querying for Super Admin user...")
  user_data=db.session.query(AppUsers).filter(AppUsers.email == 'admin@devpipeline.com').first()
  if user_data == None:
    org_id = org_data.org_id
    print("Super Admin not found! Creating foundation-admin@devpipeline user...")
    password = '1234'
      # while password == '' or password is None:
      #   password = input(' Enter a password for Suepr Admin:')

      # hashed_password = bcrypt.generate_password_hash(password).decode("utf8") 
    record = AppUsers('Super', 'Admin', "admin@devpipeline.com", password, "Orem", "Utah", "super-admin", org_id)

    db.session.add(record)
    db.session.commit()
  else:
    print("Super Admin user found!")



@app.route('/organzation/add', methods=['POST'])
def add_org():
  form = request.form

  fields = ["name", "phone", "city", "state", "active"]
  req_fields = ["name"]
  values = []

  for field in fields:
    form_value = form.get(field)
    if form_value in req_fields and form_value == " ":
      return jsonify (f'{field} is required'), 400

      values.append(form_value)

    name = form.get('name')
    phone = form.get('phone')
    city = form.get('city')
    state = form.get('state')

  new_org = Organizations(name, phone, city, state)

  db.session.add(new_org)
  db.session.commit()

  return jsonify('Org Added'), 200

@app.route('/orgnization/list', methods=['GET'])
def get_all_organizations():
  org_records = db.session.query(Organizations).all()

  return jsonify(organizations_schema.dump(org_records)), 200

@app.route('/user/activate/<user_id>', methods=['PUT'])
def activate_user(user_id):
  user_record = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  if not user_record:
    return ('User not found'), 404

  user_record.active = True
  db.session.commit()
  return jsonify("User Activated"), 201

@app.route('/user/list', methods=['GET'])
def get_all_users():
  user_records = db.session.query(AppUsers).all()
  
  return jsonfiy(users_schema.dump(user_records)), 200

@app.route('/user/<user_id>', methods = ['GET'])
def get_user_by_id(user_id):
  user_record = db.session.query(AppUsers).filter(AppUsers.user_id==user_id).first()

  return jsonify(user_schema.dump(user_record)), 200

def edit_user(user_id, first_name = None, last_name = None, email = None, password = None, city = None, state = None, active = None):
  user_record == db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
  
  if not user_record:
    return('User not found'), 404
  if request:
    form = request.format
    first_name = form.get('first_name')
    last_name = form.get('last_name')
    email = form.get('email')
    password = form.get('password')
    city = form.get('city')
    state = form.get('state')
    role = form.get('role')
    active = form.get('active')

  if first_name:
    user_record.first_name = first_name
  if last_name:
    user_record.last_name = last_name
  if email:
    user_record.last_name = email
  if password:
    user_record.last_name = password
  if city:
    user_record.last_name = city
  if state:
    user_record.last_name = state
  if role:
    user_record.last_name = role
  if active:
    user_record.last_name = active
   
  db.session.commit()

  return jsonify('User Updated'), 201

  if __name__ == '__main__':
    create_all()
    app.run()

users = d.relationship('Users', backref='Organization', lazy=True)
