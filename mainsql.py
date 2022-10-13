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

app.config('SQLALCHEMY_DATABASE_URI') = database_host_uri

app.config('SQLALCHEMY_TRACK_MODIFICATIONS') = False

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



@app.route('/organzation/add', methods=(['POST'])
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

@app.route('/orgnization/list'), methods=(['GET'])
def get_all_organizations():
  org_records = db.session.query(Organizations).all()

  return jsonify(organizations_schema.dump(org_records)), 200
...
124 @app.route('/user/activate/<user_id>'), methods=(['PUT'])
125 def activate_user(user_id):
126   user_record = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
127   if not user_record:
128     return ('User not found'), 404
129
130   user_record.active = True
131   db.session.commit()
132
133   return jsonify("User Activated"), 201
134
135 @app.route('/user/list', methods=(['GET'])
136 def get_all_users():
137   user_records = db.session.query(AppUsers).all()
138   
139   return jsonfiy(users_schema.dump(user_records)), 200
140
141 @app.route('/user/<user_id>', methods = (['GET']))
142 def get_user_by_id(user_id):
143   user_record = db.session.query(AppUsers).filter(AppUsers.user_id==user_id).first()
144
145   return jsonify(user_schema.dump(user_record)), 200
...
165 def edit_user(user_id, first_name = None, last_name = None, email = None, password = None, city = None, state = None, active = None)
166   if user_record = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
167   
168   if not user_record:
169     return('User not found'), 404
170   if request:
171     form = request.format
172     first_name = form.get('first_name')
173     last_name = form.get('last_name')
174     email = form.get('email')
175     password = form.get('password')
176     city = form.get('city')
177     state = form.get('state')
178     role = form.get('role')
179     active = form.get('active')
180
181   if first_name:
182     user_record.first_name = first_name
183   if last_name:
184     user_record.last_name = last_name
185   if email:
186     user_record.last_name = email
187   if password:
188     user_record.last_name = password
189   if city:
190     user_record.last_name = city
191   if state:
192     user_record.last_name = state
193   if role:
194     user_record.last_name = role
195   if active:
196     user_record.last_name = active
197   
198   db.session.commit()
199
200   return jsonify('User Updated'), 201
201
202   if __name__ = '__main__':
203     create_all()
204     app.run()



users = d.relationship('Users', backref='Organization', lazy=True)
