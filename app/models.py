from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    documents = db.relationship('Document', backref='author', lazy='dynamic')

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload_date = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    status = db.Column(db.String(64))
    content = db.Column(db.Text)
    analysis_results = db.relationship('AnalysisResult', backref='document', lazy='dynamic')
    sorting_results = db.relationship('SortingResult', backref='document', lazy='dynamic')

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    analysis_date = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    data = db.Column(db.Text)

class SortingResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    sort_date = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    sorted_data = db.Column(db.Text)
