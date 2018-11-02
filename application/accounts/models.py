from application import db

class Account(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
  onupdate=db.func.current_timestamp())

  name = db.Column(db.String(144), nullable=False)
  username = db.Column(db.String(255), nullable=False, unique=True)  
  password = db.Column(db.String(255), nullable=False)  
  user_role = db.Column(db.String(), nullable=False)

  def __init__(self, name, username, password, user_role):
    self.name = name
    self.username = username
    self.password = password
    self.user_role = user_role