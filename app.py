from flask import Flask, request, render_template, send_file, flash, redirect, url_for, jsonify
import os
import tempfile
import zipfile
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess
import io
import time
import threading
import shutil

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
OUTPUT_FOLDER = 'output'
DOWNLOADS_FOLDER = 'downloads'

for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER, OUTPUT_FOLDER, DOWNLOADS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

conversion_progress = {"current": 0, "total": 0, "status": "idle", "estimated_time": 0, "current_file": ""}

ALLOWED_EXTENSIONS = {'doc', 'docx', 'rtf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_pdf(input_file, output_file):
    """Convert Word/RTF documents to PDF using LibreOffice"""
    try:
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_file),
            input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            generated_pdf = os.path.join(os.path.dirname(output_file), f"{base_name}.pdf")
            
            if os.path.exists(generated_pdf) and generated_pdf != output_file:
                os.rename(generated_pdf, output_file)
            
            return True
        else:
            print(f"LibreOffice conversion failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error converting {input_file}: {str(e)}")
        return False

def create_toc_pdf(pdf_files, output_path):
    """Create a Table of Contents PDF with hyperlinks"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("Table of Contents", title_style))
    story.append(Spacer(1, 20))
    
    toc_style = ParagraphStyle(
        'TOCEntry',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        leftIndent=20
    )
    
    current_page = 2  # Start from page 2 (after TOC)
    
    for i, pdf_file in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_file)
        name_without_ext = os.path.splitext(filename)[0]
        
        link_text = f"{i}. {name_without_ext} ........................ Page {current_page}"
        story.append(Paragraph(link_text, toc_style))
        
        try:
            with open(pdf_file, 'rb') as f:
                reader = PdfReader(f)
                current_page += len(reader.pages)
        except:
            current_page += 1  # Assume 1 page if can't read
    
    doc.build(story)
    return output_path

def merge_pdfs_with_bookmarks(pdf_files, output_path, include_toc=True):
    """Merge PDFs and add bookmarks for each document"""
    writer = PdfWriter()
    
    if include_toc:
        toc_path = os.path.join(os.path.dirname(output_path), 'toc_temp.pdf')
        create_toc_pdf(pdf_files, toc_path)
        
        with open(toc_path, 'rb') as toc_file:
            toc_reader = PdfReader(toc_file)
            for page in toc_reader.pages:
                writer.add_page(page)
        
        writer.add_outline_item("Table of Contents", 0)
        current_page = len(toc_reader.pages)
        
        os.remove(toc_path)
    else:
        current_page = 0
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        name_without_ext = os.path.splitext(filename)[0]
        
        try:
            with open(pdf_file, 'rb') as f:
                reader = PdfReader(f)
                
                writer.add_outline_item(name_without_ext, current_page)
                
                for page in reader.pages:
                    writer.add_page(page)
                
                current_page += len(reader.pages)
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            continue
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    return output_path

@app.route('/progress')
def get_progress():
    return jsonify(conversion_progress)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    global conversion_progress
    
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    
    if not files or all(file.filename == '' for file in files):
        flash('No files selected')
        return redirect(url_for('index'))
    
    output_folder_name = request.form.get('output_folder', 'output')
    if output_folder_name == 'output':
        selected_folder = OUTPUT_FOLDER
    elif output_folder_name == 'downloads':
        selected_folder = DOWNLOADS_FOLDER
    else:
        selected_folder = UPLOAD_FOLDER
    
    for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER, OUTPUT_FOLDER, DOWNLOADS_FOLDER]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    conversion_progress = {"current": 0, "total": len(files), "status": "converting", "estimated_time": 0, "current_file": ""}
    start_time = time.time()
    
    uploaded_files = []
    converted_pdfs = []
    
    for i, file in enumerate(files):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            uploaded_files.append(file_path)
            
            conversion_progress["current_file"] = filename
            
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
            
            if convert_to_pdf(file_path, pdf_path):
                converted_pdfs.append(pdf_path)
            else:
                flash(f'Failed to convert {filename}')
            
            conversion_progress["current"] = i + 1
            elapsed = time.time() - start_time
            if i > 0:
                avg_time_per_file = elapsed / (i + 1)
                remaining_files = len(files) - (i + 1)
                conversion_progress["estimated_time"] = remaining_files * avg_time_per_file
    
    if not converted_pdfs:
        conversion_progress["status"] = "idle"
        flash('No files were successfully converted to PDF')
        return redirect(url_for('index'))
    
    conversion_progress["status"] = "merging"
    conversion_progress["current_file"] = "merged_document.pdf"
    converted_pdfs.sort()
    
    for pdf_path in converted_pdfs:
        pdf_filename = os.path.basename(pdf_path)
        output_pdf_path = os.path.join(selected_folder, pdf_filename)
        if os.path.abspath(pdf_path) != os.path.abspath(output_pdf_path):
            shutil.copy2(pdf_path, output_pdf_path)
    
    output_filename = 'merged_document.pdf'
    output_path = os.path.join(selected_folder, output_filename)
    
    try:
        merge_pdfs_with_bookmarks(converted_pdfs, output_path, include_toc=True)
        conversion_progress["status"] = "idle"
        flash(f'Successfully processed {len(converted_pdfs)} documents!')
        return send_file(output_path, as_attachment=True, download_name=output_filename)
    except Exception as e:
        conversion_progress["status"] = "idle"
        flash(f'Error merging PDFs: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
