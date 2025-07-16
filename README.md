# 📄 Flask PDF Converter & Merger

A powerful Flask web application that converts Word documents and RTF files to PDF, merges them into a single document, and creates professional bookmarks with an interactive table of contents.

![Flask PDF Converter](https://img.shields.io/badge/Flask-PDF%20Converter-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📝 **Multi-format Support**: Convert Word (.doc, .docx) and RTF documents to PDF
- 🔗 **Smart Merging**: Combine all converted PDFs into a single, organized document
- 📑 **Interactive TOC**: Generate a table of contents with clickable hyperlinks to each document
- 🔖 **Navigation Bookmarks**: Add professional bookmarks for easy document navigation
- 🎨 **Modern UI**: Clean, responsive web interface with drag-and-drop functionality
- ⚡ **Batch Processing**: Handle multiple documents simultaneously
- 🛡️ **Secure**: File validation and secure upload handling

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- LibreOffice (for document conversion)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rchennamaneni800/flask-pdf-converter.git
   cd flask-pdf-converter
   ```

2. **Install LibreOffice**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install libreoffice
   
   # macOS
   brew install --cask libreoffice
   
   # Windows
   # Download from https://www.libreoffice.org/download/download/
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

### Using Docker

```bash
# Build the Docker image
docker build -t flask-pdf-converter .

# Run the container
docker run -p 5000:5000 flask-pdf-converter
```

## 📖 How to Use

1. **Upload Documents**: Click "Choose Word/RTF Documents" and select your files
2. **Process**: Click "Convert & Merge to PDF" to start the conversion
3. **Download**: Get your merged PDF with bookmarks and TOC

## 🏗️ How It Works

1. **Upload**: Users upload Word (.doc, .docx) or RTF files through the web interface
2. **Convert**: LibreOffice converts each document to PDF format in headless mode
3. **Merge**: All PDFs are merged into a single document using PyPDF2
4. **TOC**: A table of contents is generated with hyperlinks to each document using ReportLab
5. **Bookmarks**: Navigation bookmarks are added for each original document
6. **Download**: The final merged PDF is provided for download

## 📁 Project Structure

```
flask-pdf-converter/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Web interface template
├── uploads/               # Temporary storage for uploaded files
├── converted/             # Temporary storage for converted PDFs
├── output/                # Final merged PDF output
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── test_functionality.py # Test script
└── README.md             # This file
```

## 🧪 Testing

Run the test script to verify functionality:

```bash
python test_functionality.py
```

This will:
- Create sample RTF documents
- Test conversion to PDF
- Test merging with bookmarks and TOC
- Verify output file creation

## 🚀 Deployment

### Local Development

```bash
# Set environment variables
export FLASK_ENV=development
export SECRET_KEY=your-secret-key

# Run the application
python app.py
```

### Production Deployment

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   export PORT=5000
   ```

2. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Docker Deployment

```bash
# Build and run with Docker
docker build -t flask-pdf-converter .
docker run -p 5000:5000 -e SECRET_KEY=your-secret-key flask-pdf-converter
```

## 🔧 Configuration

The application can be configured using environment variables:

- `SECRET_KEY`: Flask secret key for session security
- `PORT`: Port to run the application on (default: 5000)
- `FLASK_ENV`: Environment mode (development/production)
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 50MB)

## 📋 Requirements

- **Python**: 3.7 or higher
- **LibreOffice**: For document conversion
- **Flask**: Web framework
- **PyPDF2**: PDF manipulation
- **ReportLab**: PDF generation
- **Werkzeug**: WSGI utilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **LibreOffice not found**: Ensure LibreOffice is installed and available in PATH
2. **Permission errors**: Check file permissions for upload/converted/output directories
3. **Large file uploads**: Adjust `MAX_CONTENT_LENGTH` if needed
4. **Conversion failures**: Verify document format and integrity

### Error Messages

- "No files selected": Select at least one document before converting
- "Failed to convert": Document may be corrupted or unsupported format
- "Error merging PDFs": Check individual PDF files for corruption

## 🎯 Future Enhancements

- Support for additional document formats (DOCX, ODT)
- Custom bookmark naming
- Password protection for output PDFs
- Batch processing API
- Cloud storage integration
- Advanced TOC formatting options

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing [GitHub Issues](https://github.com/rchennamaneni800/flask-pdf-converter/issues)
3. Create a new issue with detailed information

---

**Created by**: RCH (@rchennamaneni800)  
**Link to Devin run**: https://app.devin.ai/sessions/2e6fb90fb6094ac698d42f37225ee114
