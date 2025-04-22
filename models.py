import datetime
from app import db

class Document(db.Model):
    """Model for storing uploaded document data and analysis results"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(255))
    summary = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # One-to-many relationship with clauses
    clauses = db.relationship('Clause', backref='document', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Document {self.filename}>'

    def to_dict(self):
        """Convert document to dictionary format for API responses"""
        return {
            'id': self.id,
            'filename': self.filename,
            'document_type': self.document_type,
            'summary': self.summary,
            'upload_date': self.upload_date.isoformat(),
            'clauses': {clause.clause_type: {
                'original_text': clause.original_text,
                'explanation': clause.explanation
            } for clause in self.clauses}
        }

class Clause(db.Model):
    """Model for storing individual clause analysis"""
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    clause_type = db.Column(db.String(50), nullable=False)  # termination, confidentiality, etc.
    original_text = db.Column(db.Text)
    explanation = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Clause {self.clause_type}>'