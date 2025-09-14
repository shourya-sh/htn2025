from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime
import json

app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key="AIzaSyByu3noEXHjGjBLNTn451CjYCn_Vf9Uzkw")
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Document templates with only essential fields
DOCUMENT_TEMPLATES = {
    "contract": {
        "name": "Contract Agreement",
        "description": "Create a legally binding contract between parties",
        "icon": "📄",
        "essential_fields": [
            {"name": "party1_name", "label": "First Party Name", "type": "text", "required": True},
            {"name": "party2_name", "label": "Second Party Name", "type": "text", "required": True},
            {"name": "contract_type", "label": "Contract Type", "type": "select", "options": ["Service Agreement", "Employment Contract", "Partnership Agreement", "Sales Contract", "Other"], "required": True},
            {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
            {"name": "end_date", "label": "End Date", "type": "date", "required": False},
            {"name": "compensation", "label": "Compensation Details", "type": "textarea", "required": True}
        ],
        "additional_prompts": [
            "What are the specific terms and conditions of this contract?",
            "Are there any termination clauses or conditions?",
            "What governing law should apply to this contract?",
            "Are there any confidentiality or non-compete provisions needed?",
            "What are the payment terms and schedules?",
            "Are there any warranties or guarantees to include?"
        ]
    },
    "lease_agreement": {
        "name": "Lease Agreement",
        "description": "Create a residential or commercial lease agreement",
        "icon": "🏠",
        "essential_fields": [
            {"name": "landlord_name", "label": "Landlord Name", "type": "text", "required": True},
            {"name": "tenant_name", "label": "Tenant Name", "type": "text", "required": True},
            {"name": "property_address", "label": "Property Address", "type": "textarea", "required": True},
            {"name": "lease_type", "label": "Lease Type", "type": "select", "options": ["Residential", "Commercial"], "required": True},
            {"name": "start_date", "label": "Lease Start Date", "type": "date", "required": True},
            {"name": "end_date", "label": "Lease End Date", "type": "date", "required": True},
            {"name": "monthly_rent", "label": "Monthly Rent Amount", "type": "number", "required": True},
            {"name": "security_deposit", "label": "Security Deposit", "type": "number", "required": True}
        ],
        "additional_prompts": [
            "What utilities are included in the rent?",
            "Are pets allowed? If yes, any restrictions?",
            "What are the rules regarding subletting?",
            "Are there any parking arrangements?",
            "What are the maintenance responsibilities?",
            "Are there any noise restrictions or quiet hours?",
            "What are the late payment penalties?",
            "Are there any restrictions on modifications to the property?"
        ]
    },
    "nda": {
        "name": "Non-Disclosure Agreement",
        "description": "Create a confidentiality agreement to protect sensitive information",
        "icon": "🤐",
        "essential_fields": [
            {"name": "disclosing_party", "label": "Disclosing Party", "type": "text", "required": True},
            {"name": "receiving_party", "label": "Receiving Party", "type": "text", "required": True},
            {"name": "confidential_info", "label": "Description of Confidential Information", "type": "textarea", "required": True},
            {"name": "purpose", "label": "Purpose of Disclosure", "type": "textarea", "required": True},
            {"name": "duration", "label": "Confidentiality Duration (years)", "type": "number", "required": True},
            {"name": "effective_date", "label": "Effective Date", "type": "date", "required": True}
        ],
        "additional_prompts": [
            "What are the permitted uses of the confidential information?",
            "Are there any exceptions to confidentiality (e.g., court orders)?",
            "What are the consequences of breach?",
            "Are there any return/destruction requirements?",
            "What governing law should apply?",
            "Are there any non-solicitation provisions needed?"
        ]
    },
    "invoice": {
        "name": "Invoice",
        "description": "Create a professional invoice for goods or services",
        "icon": "💰",
        "essential_fields": [
            {"name": "seller_name", "label": "Seller/Company Name", "type": "text", "required": True},
            {"name": "seller_address", "label": "Seller Address", "type": "textarea", "required": True},
            {"name": "buyer_name", "label": "Buyer/Client Name", "type": "text", "required": True},
            {"name": "buyer_address", "label": "Buyer Address", "type": "textarea", "required": True},
            {"name": "invoice_number", "label": "Invoice Number", "type": "text", "required": True},
            {"name": "invoice_date", "label": "Invoice Date", "type": "date", "required": True},
            {"name": "due_date", "label": "Due Date", "type": "date", "required": True},
            {"name": "items", "label": "Items/Services Description", "type": "textarea", "required": True},
            {"name": "total_amount", "label": "Total Amount", "type": "number", "required": True}
        ],
        "additional_prompts": [
            "What are the payment terms and methods accepted?",
            "Are there any late payment fees?",
            "What is the tax rate to apply?",
            "Are there any discounts or special terms?",
            "What is the currency for this invoice?",
            "Are there any specific payment instructions?"
        ]
    },
    "merger_agreement": {
        "name": "Merger & Acquisition Agreement",
        "description": "Create a comprehensive merger or acquisition agreement",
        "icon": "🏢",
        "essential_fields": [
            {"name": "acquiring_company", "label": "Acquiring Company", "type": "text", "required": True},
            {"name": "target_company", "label": "Target Company", "type": "text", "required": True},
            {"name": "transaction_type", "label": "Transaction Type", "type": "select", "options": ["Merger", "Acquisition", "Asset Purchase", "Stock Purchase"], "required": True},
            {"name": "purchase_price", "label": "Purchase Price", "type": "text", "required": True},
            {"name": "closing_date", "label": "Closing Date", "type": "date", "required": True},
            {"name": "key_assets", "label": "Key Assets/Properties", "type": "textarea", "required": True}
        ],
        "additional_prompts": [
            "What is the due diligence period?",
            "What are the closing conditions?",
            "Are there any earn-out provisions?",
            "What are the representations and warranties?",
            "Are there any non-compete provisions?",
            "What are the indemnification terms?",
            "Are there any regulatory approvals needed?",
            "What are the termination provisions?"
        ]
    },
    "employment_contract": {
        "name": "Employment Contract",
        "description": "Create a comprehensive employment agreement",
        "icon": "👔",
        "essential_fields": [
            {"name": "employer_name", "label": "Employer Name", "type": "text", "required": True},
            {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
            {"name": "job_title", "label": "Job Title", "type": "text", "required": True},
            {"name": "start_date", "label": "Employment Start Date", "type": "date", "required": True},
            {"name": "employment_type", "label": "Employment Type", "type": "select", "options": ["Full-time", "Part-time", "Contract", "Temporary"], "required": True},
            {"name": "salary", "label": "Annual Salary", "type": "number", "required": True},
            {"name": "work_schedule", "label": "Work Schedule", "type": "textarea", "required": True}
        ],
        "additional_prompts": [
            "What benefits package is included?",
            "What is the probationary period?",
            "What are the termination notice requirements?",
            "Are there any non-compete or confidentiality clauses?",
            "What are the vacation and sick leave policies?",
            "Are there any performance review requirements?",
            "What are the intellectual property rights?",
            "Are there any relocation or travel requirements?"
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', documents=DOCUMENT_TEMPLATES)

@app.route('/document/<doc_type>')
def document_form(doc_type):
    if doc_type not in DOCUMENT_TEMPLATES:
        return "Document type not found", 404
    return render_template('document_form.html', doc_type=doc_type, template=DOCUMENT_TEMPLATES[doc_type])

@app.route('/prompt/<doc_type>', methods=['POST'])
def get_additional_info(doc_type):
    if doc_type not in DOCUMENT_TEMPLATES:
        return jsonify({"error": "Document type not found"}), 404
    
    data = request.get_json()
    template = DOCUMENT_TEMPLATES[doc_type]
    
    # Build context from essential fields
    context = f"Document Type: {template['name']}\n\nEssential Information:\n"
    for field in template['essential_fields']:
        field_name = field['name']
        if field_name in data and data[field_name]:
            context += f"{field['label']}: {data[field_name]}\n"
    
    # Generate prompt for additional information
    prompt = f"""Based on the following {template['name']} information:

{context}

Please ask the user for additional important information that would be needed for a complete and professional {template['name']}. 

Consider these areas that might need clarification:
{chr(10).join(f"- {prompt}" for prompt in template['additional_prompts'])}

Ask 2-3 specific questions to gather the most important missing information. Be conversational and helpful. Format your response as a friendly message asking for the additional details."""

    try:
        response = model.generate_content(prompt)
        return jsonify({
            "success": True,
            "prompt": response.text,
            "context": context
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate/<doc_type>', methods=['POST'])
def generate_document(doc_type):
    if doc_type not in DOCUMENT_TEMPLATES:
        return jsonify({"error": "Document type not found"}), 404
    
    data = request.get_json()
    template = DOCUMENT_TEMPLATES[doc_type]
    
    # Build the prompt for the AI
    prompt = f"Generate a professional {template['name']} with the following information:\n\n"
    
    # Add essential fields
    for field in template['essential_fields']:
        field_name = field['name']
        if field_name in data and data[field_name]:
            prompt += f"{field['label']}: {data[field_name]}\n"
    
    # Add additional information if provided
    if 'additional_info' in data and data['additional_info']:
        prompt += f"\nAdditional Information Provided:\n{data['additional_info']}\n"
    
    prompt += f"\nPlease generate a complete, professional {template['name']} that includes all necessary legal clauses, terms, and conditions. Format it properly with clear sections and professional language. Include standard legal provisions that would be appropriate for this type of document."
    
    try:
        response = model.generate_content(prompt)
        return jsonify({
            "success": True,
            "document": response.text,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
