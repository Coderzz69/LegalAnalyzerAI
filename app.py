import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.middleware.proxy_fix import ProxyFix
from utils import analyze_legal_document

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Maximum content length for file uploads (10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

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
    analysis_result = session.get('analysis_result')
    if not analysis_result:
        flash('No analysis data found. Please upload a document.', 'warning')
        return redirect(url_for('index'))
    
    return render_template('result.html', analysis=analysis_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
