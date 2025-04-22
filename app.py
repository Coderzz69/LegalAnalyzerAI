import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils import analyze_legal_document

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create database base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    logger.info(f"Database URL configured: {DATABASE_URL}")
else:
    logger.warning("DATABASE_URL not found, using SQLite in-memory database")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Maximum content length for file uploads (10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Initialize database with app
db.init_app(app)

# Create database tables within application context
with app.app_context():
    import models  # Import models after db is defined
    db.create_all()
    logger.info("Database tables created")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'document' not in request.files:
        flash('No document uploaded', 'danger')
        return redirect(url_for('index'))
    
    document_file = request.files['document']
    
    if document_file.filename == '':
        flash('No document selected', 'danger')
        return redirect(url_for('index'))
    
    try:
        # Read the document content
        document_text = document_file.read().decode('utf-8')
        
        if not document_text.strip():
            flash('The document is empty', 'danger')
            return redirect(url_for('index'))
        
        # Analyze the document
        analysis_result = analyze_legal_document(document_text)
        
        # Store the result in the session
        session['analysis_result'] = analysis_result
        
        # Save to database
        from models import Document, Clause
        
        # Create a new document record
        new_document = Document(
            filename=document_file.filename,
            document_type=analysis_result.get('document_type', 'Unknown'),
            summary=analysis_result.get('summary', '')
        )
        
        # Create clauses for the document
        clauses_data = analysis_result.get('clauses', {})
        for clause_type, clause_data in clauses_data.items():
            new_clause = Clause(
                clause_type=clause_type,
                original_text=clause_data.get('original_text', ''),
                explanation=clause_data.get('explanation', '')
            )
            new_document.clauses.append(new_clause)
        
        # Add and commit to the database
        db.session.add(new_document)
        db.session.commit()
        
        # Store document ID in session
        session['document_id'] = new_document.id
        
        return redirect(url_for('result'))
    
    except UnicodeDecodeError:
        flash('Unsupported document format. Please upload a text document.', 'danger')
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        flash(f'An error occurred while analyzing the document: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/result')
def result():
    # If we have an analysis result in the session, use that
    analysis_result = session.get('analysis_result')
    
    # If we have a document ID, get it from the database
    document_id = session.get('document_id')
    
    if not analysis_result and not document_id:
        flash('No analysis data found. Please upload a document.', 'warning')
        return redirect(url_for('index'))
    
    # If we have a document ID but no analysis result in the session, fetch from DB
    if document_id and not analysis_result:
        from models import Document
        document = Document.query.get(document_id)
        if document:
            analysis_result = document.to_dict()
            session['analysis_result'] = analysis_result
        else:
            flash('Document not found in database. Please upload again.', 'warning')
            return redirect(url_for('index'))
    
    return render_template('result.html', analysis=analysis_result)

@app.route('/history')
def history():
    """Display a list of previously analyzed documents"""
    from models import Document
    documents = Document.query.order_by(Document.upload_date.desc()).all()
    return render_template('history.html', documents=documents)

@app.route('/document/<int:document_id>')
def view_document(document_id):
    """View a previously analyzed document"""
    from models import Document
    document = Document.query.get_or_404(document_id)
    analysis_result = document.to_dict()
    session['analysis_result'] = analysis_result
    session['document_id'] = document_id
    return redirect(url_for('result'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
