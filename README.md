# 📧 Email Response Assistant

An AI-powered email analysis and response system that helps you manage emails efficiently by generating intelligent response routes and variations.

## 🌟 Features

- **AI Email Analysis**: Automatically analyzes emails for urgency (1-5 scale)
- **Smart Response Routes**: Generates 4 custom response strategies per email
- **Multiple Variations**: 3 different response styles for each route
- **Interactive Editor**: Edit responses with AI assistance
- **CSV-Based Storage**: All data stored in CSV files for easy management
- **Clean Web Interface**: Modern Flask-based frontend

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
EMAIL_COUNT=10
```

### 3. Prepare Email Data

Ensure you have an `emails.csv` file with the following format:

```csv
id,sender,subject,body,timestamp
1,john@example.com,Subject Here,Email body content...,2024-06-29 10:00:00
```

A sample `emails.csv` file is provided with 10 sample emails.

### 4. Run the Application

```bash
python run_app.py
```

Or directly:

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 📁 File Structure

```
email-response-assistant/
├── app.py                    # Main Flask application
├── run_app.py               # Startup script with error checking
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── emails.csv              # Input email data
├── email_analysis.csv      # AI analysis results (auto-generated)
├── user_selections.csv     # User choices (auto-generated)
└── templates/
    ├── index.html          # Email list page
    └── email_detail.html   # Email detail with response routes
```

## 🚀 Usage Guide

### 1. Email List View
- View all emails with urgency indicators
- Click "Analyze" to process emails with AI
- Analyzed emails show priority levels (1-5)

### 2. Email Detail View
- Click on any email to view details
- See AI-generated response routes
- Choose from 4 different response strategies

### 3. Response Generation
- **Step 1**: Select a response route
- **Step 2**: Choose from 3 response variations
- **Step 3**: Edit the response in the text editor

### 4. AI Assistant Features
- **Auto-Analysis**: AI determines email urgency and generates response routes
- **Response Editing**: Provide instructions to modify responses
- **Custom Routes**: AI creates contextual route names based on email content

## 📊 Data Storage

### Input CSV Format (`emails.csv`)
```csv
id,sender,subject,body,timestamp
1,john@company.com,Project Update,Email content here...,2024-06-29 10:00:00
```

### AI Analysis CSV (`email_analysis.csv`)
Automatically generated with:
- Email ID and urgency score
- 4 route names and their 3 variations each
- Analysis timestamp

### User Selections CSV (`user_selections.csv`)
Tracks user choices:
- Selected route and variation
- Final edited response
- Selection timestamp

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `EMAIL_COUNT` | Max emails to process | 10 |

### OpenAI Model

The application uses `gpt-3.5-turbo` by default. You can modify this in `app.py` if needed.

## 🔧 Customization

### Adding New Email Sources
Currently uses CSV files. To integrate with email providers:
1. Modify the `load_emails()` function in `app.py`
2. Add email provider API integration
3. Update the email loading logic

### Customizing AI Prompts
Modify the prompts in these functions:
- `generate_ai_analysis()` - For route generation
- `edit_response_with_ai()` - For response editing

### Styling Changes
Update the CSS in the HTML templates:
- `templates/index.html` - Email list styling
- `templates/email_detail.html` - Detail page styling

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in `.env`
   - Verify the key has sufficient credits

2. **CSV File Not Found**
   - Make sure `emails.csv` exists in the project root
   - Check the file format matches the expected structure

3. **Module Import Errors**
   - Run `pip install -r requirements.txt`
   - Ensure you're using Python 3.7+

4. **Port Already in Use**
   - Change the port in `run_app.py` or `app.py`
   - Or stop the process using the port

### Debug Mode
The application runs in debug mode by default. To disable:
```python
app.run(debug=False)
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main email list page |
| `/analyze/<email_id>` | GET | Analyze email with AI |
| `/email/<email_id>` | GET | View email details |
| `/api/edit-response` | POST | Edit response with AI |
| `/api/save-selection` | POST | Save user selection |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to modify and distribute as needed.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the file structure and setup steps
3. Ensure all dependencies are installed correctly

---

**Happy Email Managing! 📧✨**