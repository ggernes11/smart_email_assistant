import os
import csv
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuration
EMAIL_COUNT = int(os.getenv('EMAIL_COUNT', 10))
INPUT_CSV = 'emails.csv'
ANALYSIS_CSV = 'email_analysis.csv'
SELECTIONS_CSV = 'user_selections.csv'

# Simple fix: Replace your load_emails() function with this:

def load_emails():
    """Load emails from CSV file"""
    try:
        df = pd.read_csv(INPUT_CSV)
        df['body'] = df['body'].fillna('')
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return df.head(EMAIL_COUNT).to_dict('records')
    except FileNotFoundError:
        return []

def load_analysis():
    """Load AI analysis results from CSV"""
    print(f"Loading analysis results from {ANALYSIS_CSV}")
    try:
        df = pd.read_csv(ANALYSIS_CSV)
        return df.to_dict('records')
    except FileNotFoundError:
        return []

def save_analysis(email_id, urgency, routes_data):
    """Save AI analysis to CSV"""
    print(f"Saving analysis for email ID {email_id} to {ANALYSIS_CSV}")
    analysis_data = {
        'email_id': email_id,
        'urgency': urgency,
        'timestamp': datetime.now().isoformat()
    }
    
    # Add route data
    for i, route in enumerate(routes_data, 1):
        analysis_data[f'route{i}_name'] = route['name']
        for j, variation in enumerate(route['variations'], 1):
            analysis_data[f'route{i}_var{j}'] = variation
    
    # Check if file exists
    file_exists = os.path.isfile(ANALYSIS_CSV)
    
    with open(ANALYSIS_CSV, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['email_id', 'urgency', 'timestamp'] + \
                    [f'route{i}_name' for i in range(1, 5)] + \
                    [f'route{i}_var{j}' for i in range(1, 5) for j in range(1, 4)]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(analysis_data)

def save_selection(email_id, route_name, variation, final_response):
    """Save user selection to CSV"""
    print(f"Saving user selection for email ID {email_id} to {SELECTIONS_CSV}")
    selection_data = {
        'email_id': email_id,
        'route_name': route_name,
        'selected_variation': variation,
        'final_response': final_response,
        'timestamp': datetime.now().isoformat()
    }
    
    file_exists = os.path.isfile(SELECTIONS_CSV)
    
    with open(SELECTIONS_CSV, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['email_id', 'route_name', 'selected_variation', 'final_response', 'timestamp']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(selection_data)

def generate_ai_analysis(email_data):
    """Generate AI analysis for an email"""
    print(f"Generating AI analysis for email: {email_data['subject']}")
    prompt = f"""
    Analyze this email and provide:
    1. Urgency score (1-5, where 1 is lowest priority, 5 is highest)
    2. Four different response routes with custom names based on the email content
    3. Three variations for each route

    Email Details:
    From: {email_data['sender']}
    Subject: {email_data['subject']}
    Body: {email_data['body']}

    Please respond in JSON format:
    {{
        "urgency": <number 1-5>,
        "routes": [
            {{
                "name": "<custom route name>",
                "variations": ["<variation 1>", "<variation 2>", "<variation 3>"]
            }},
            ... (4 routes total)
        ]
    }}
    """
    
    try:
        # Call OpenAI API to generate analysis
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.05
        )
        # print("Response code: ", response.status_code)
        response  = response.choices[0].message.content.strip()
        # get all text between the first and last curly braces
        response = response[response.find('{'):response.rfind('}')+1]
        print("Response text: ", response)
        result = json.loads(response)
        return result
    except Exception as e:
        print(f"Error generating AI analysis: {e}")
        return None

def edit_response_with_ai(current_response, instructions):
    """Edit response using AI based on user instructions"""
    prompt = f"""
    Please edit the following response based on the user's instructions:

    Current Response:
    {current_response}

    User Instructions:
    {instructions}

    Please provide only the edited response, no explanations.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.05
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error editing response: {e}")
        return current_response

@app.route('/')
def index():
    """Main page showing email list"""
    emails = load_emails()
    analysis = load_analysis()
    
    # Merge email data with analysis
    analysis_dict = {a['email_id']: a for a in analysis}
    
    for email in emails:
        email_analysis = analysis_dict.get(email['id'])
        if email_analysis:
            email['urgency'] = email_analysis['urgency']
            email['analyzed'] = True
        else:
            email['urgency'] = None
            email['analyzed'] = False

    return render_template('index.html', emails=emails)

@app.route('/analyze/<int:email_id>')
def analyze_email(email_id):
    """Analyze an email with AI"""
    emails = load_emails()
    email = next((e for e in emails if e['id'] == email_id), None)
    
    if not email:
        return jsonify({'error': 'Email not found'}), 404
    
    # Check if already analyzed
    analysis = load_analysis()
    existing = next((a for a in analysis if a['email_id'] == email_id), None)
    
    if existing:
        return jsonify({'message': 'Email already analyzed'})
    
    # Generate AI analysis
    ai_result = generate_ai_analysis(email)
    
    if ai_result:
        save_analysis(email_id, ai_result['urgency'], ai_result['routes'])
        return jsonify({'message': 'Analysis complete'})
    else:
        return jsonify({'error': 'Failed to analyze email'}), 500

# Add this debugging code to your view_email function:

@app.route('/email/<int:email_id>')
def view_email(email_id):
    """View email details with routes"""
    import os
    
    # Debug template path
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    print(f"DEBUG: Flask app instance folder: {app.instance_path}")
    print(f"DEBUG: Flask app root path: {app.root_path}")
    
    # Check if templates folder exists
    templates_path = os.path.join(app.root_path, 'templates')
    print(f"DEBUG: Templates path: {templates_path}")
    print(f"DEBUG: Templates folder exists: {os.path.exists(templates_path)}")
    
    if os.path.exists(templates_path):
        files = os.listdir(templates_path)
        print(f"DEBUG: Files in templates folder: {files}")
    
    # Check specific template file
    template_file = os.path.join(templates_path, 'email_detail.html')
    print(f"DEBUG: email_detail.html path: {template_file}")
    print(f"DEBUG: email_detail.html exists: {os.path.exists(template_file)}")
    
    emails = load_emails()
    email = next((e for e in emails if e['id'] == email_id), None)
    
    if not email:
        return "Email not found", 404
    
    # Get analysis data
    analysis = load_analysis()
    email_analysis = next((a for a in analysis if a['email_id'] == email_id), None)
    
    if not email_analysis:
        return redirect(url_for('analyze_email', email_id=email_id))
    
    # Format routes data
    routes = []
    for i in range(1, 5):
        route_name = email_analysis.get(f'route{i}_name')
        if route_name:
            variations = []
            for j in range(1, 4):
                var = email_analysis.get(f'route{i}_var{j}')
                if var:
                    variations.append(var)
            
            routes.append({
                'name': route_name,
                'variations': variations
            })
    
    print(f"DEBUG: About to render template with {len(routes)} routes")
    
    return render_template('email_detail.html', email=email, routes=routes, urgency=email_analysis['urgency'])

@app.route('/api/edit-response', methods=['POST'])
def api_edit_response():
    """API endpoint to edit response with AI"""
    data = request.json
    current_response = data.get('response', '')
    instructions = data.get('instructions', '')
    
    if not instructions:
        return jsonify({'error': 'Instructions required'}), 400
    
    edited_response = edit_response_with_ai(current_response, instructions)
    return jsonify({'edited_response': edited_response})

@app.route('/api/save-selection', methods=['POST'])
def api_save_selection():
    """API endpoint to save user selection"""
    data = request.json
    email_id = data.get('email_id')
    route_name = data.get('route_name')
    variation = data.get('variation')
    final_response = data.get('final_response')
    
    save_selection(email_id, route_name, variation, final_response)
    return jsonify({'message': 'Selection saved'})

if __name__ == '__main__':
    app.run(debug=True)