# AI-Powered Menu Intelligence Widget for POS System

A lightweight full-stack application that helps restaurant managers auto-generate item descriptions and upsell suggestions using AI.

## Features

- **Menu Description Generation**: AI-powered generation of attractive menu descriptions (max 30 words)
- **Upsell Suggestions**: Intelligent combo recommendations for menu items
- **Model Toggle**: Switch between GPT-3.5 and GPT-4 simulation modes
- **Input Validation**: Basic security and sanitization
- **Rate Limiting**: API usage protection

## Project Structure

```
Project2/
├── frontend/          # React application
├── backend/           # Python Flask API
├── docs/             # Documentation and prompts
└── README.md         # This file
```

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /generate-item-details` - Generate menu description and upsell suggestion

## Integration Notes

This widget can be integrated into Grafterr's POS item management screen by:
1. Embedding the React component in the item creation/editing form
2. Calling the backend API when users need AI-generated content
3. Adding the generated content to the item database

## Security Features

- Input sanitization and validation
- Rate limiting (simulated)
- CORS configuration
- Error handling
