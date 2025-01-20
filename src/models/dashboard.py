from utils.db import db

class Dashboard(db.Model):

    _tablename_ = 'dashboard'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    name = db.Column(db.String(100), nullable=False)
    predeterminado = db.Column(db.Boolean, default=True)  
    description = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('dashboard', lazy=True))

    def _init_(self, user_id, name, predeterminado, description):
        self.user_id = user_id
        self.name = name
        self.predeterminado = predeterminado
        self.description = description