# LegalDocGen - Professional Legal Document Generator

A modern, cozy web application for generating professional legal documents using AI. Built with Flask and Google's Generative AI.

## Features

- **Streamlined Forms**: Only essential fields required for each document type
- **Interactive AI Prompts**: ChatGPT-style conversation to gather additional details
- **Multiple Document Types**: Generate contracts, lease agreements, NDAs, invoices, merger agreements, and employment contracts
- **Modern UI**: Beautiful, responsive design with a cozy feel
- **AI-Powered**: Uses Google's Generative AI for professional document generation
- **Download Support**: Generated documents can be downloaded as text files
- **Step-by-Step Process**: Clear progression from essential info to final document

## Document Types Available

1. **Contract Agreement** 📄 - Legally binding contracts between parties
2. **Lease Agreement** 🏠 - Residential and commercial lease agreements
3. **Non-Disclosure Agreement** 🤐 - Confidentiality agreements
4. **Invoice** 💰 - Professional invoices for goods or services
5. **Merger & Acquisition Agreement** 🏢 - Comprehensive merger/acquisition documents
6. **Employment Contract** 👔 - Employment agreements

## How It Works

### Step 1: Essential Information
- Fill in only the most critical fields for your document type
- Clean, focused forms with just the basics needed

### Step 2: AI-Guided Additional Details
- AI analyzes your information and asks relevant follow-up questions
- ChatGPT-style conversation to gather missing important details
- Option to skip additional details if not needed

### Step 3: Document Generation
- AI generates a complete, professional legal document
- Includes all necessary legal clauses and standard provisions
- Proper formatting and structure

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Google Generative AI API key

### Installation

1. **Clone or download the project**
   ```bash
   # If you have the files, just navigate to the project directory
   cd docGen
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Get a Google Generative AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace the API key in `app.py` line 8:
   ```python
   genai.configure(api_key="YOUR_API_KEY_HERE")
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - You'll see the main page with all available document types

## Usage

1. **Select a Document Type**
   - Browse through the available document types on the main page
   - Click on any document card to proceed

2. **Fill Essential Information**
   - Complete the streamlined form with only the most important details
   - Required fields are marked with an asterisk (*)

3. **Provide Additional Details (Optional)**
   - AI will ask specific questions about missing important information
   - Answer the prompts to make your document more complete
   - Or skip this step if you prefer to proceed with basic information

4. **Generate Document**
   - Click "Generate Document" to create your professional legal document
   - The AI will include standard legal provisions and clauses

5. **Download Document**
   - Click "Download as TXT" to save the document to your computer

## Features in Detail

### Streamlined Essential Fields
- Each document type has only the most critical fields
- No overwhelming forms with unnecessary fields
- Focus on what's truly needed to get started

### Interactive AI Prompts
- AI analyzes your information and asks relevant questions
- ChatGPT-style conversation for additional details
- Helps ensure nothing important is missed
- Option to skip if additional details aren't needed

### Professional Document Generation
- AI generates complete, professional legal documents
- Includes standard legal clauses and provisions
- Proper formatting and structure
- Comprehensive coverage even with minimal input

### Modern, Cozy Design
- Beautiful gradient backgrounds
- Smooth animations and transitions
- Step-by-step progress indicators
- Responsive design for all devices
- Intuitive user interface

### Error Handling
- Form validation for required fields
- API error handling with user-friendly messages
- Loading states and progress indicators

## Technical Details

### Backend
- **Framework**: Flask (Python)
- **AI Integration**: Google Generative AI (Gemini 1.5 Flash)
- **Architecture**: RESTful API with JSON responses
- **Interactive Prompts**: Dynamic question generation based on document type

### Frontend
- **Styling**: Pure CSS with modern design principles
- **Fonts**: Inter font family for clean typography
- **Responsive**: Mobile-first design approach
- **JavaScript**: Vanilla JS for form handling and API calls
- **Step Indicators**: Visual progress tracking

### Document Templates
- Structured template system for different document types
- Essential fields only for streamlined experience
- AI-powered additional information gathering
- Easy to extend with new document types

## Adding New Document Types

To add a new document type:

1. Add a new entry to the `DOCUMENT_TEMPLATES` dictionary in `app.py`
2. Define the document's name, description, icon, essential fields, and additional prompts
3. The form and interactive prompts will be automatically generated

Example:
```python
"new_document": {
    "name": "New Document Type",
    "description": "Description of the document",
    "icon": "📋",
    "essential_fields": [
        {"name": "field1", "label": "Field Label", "type": "text", "required": True},
        # ... more essential fields
    ],
    "additional_prompts": [
        "What additional information is needed?",
        "Are there any special requirements?",
        # ... more prompts
    ]
}
```

## Security Notes

- API keys should be stored securely in production
- Consider implementing rate limiting for API calls
- Add input validation and sanitization for production use

## License

This project is for educational and personal use. Please ensure compliance with Google's AI usage policies and local legal requirements.

## Support

For issues or questions:
1. Check that your API key is valid and has sufficient quota
2. Ensure all required fields are filled in the forms
3. Verify your internet connection for API calls

---

**LegalDocGen** - Making legal document generation simple and professional! 🚀 