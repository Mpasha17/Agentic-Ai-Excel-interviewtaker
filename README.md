# AI Excel Mock Interviewer

An AI-powered mock interview system designed to assess Microsoft Excel proficiency through intelligent questioning and evaluation.

## Project Overview

This project implements an automated Excel skills assessment system that:
- Conducts structured mock interviews with 5 progressively challenging questions
- Uses AI (OpenAI GPT) for intelligent question generation and answer evaluation
- Provides real-time feedback and generates comprehensive performance reports
- Features a clean, responsive web interface for seamless user experience

## Architecture

The project follows a clean separation of concerns with:

### Backend (FastAPI)
- **Location**: `backend/` folder
- **Framework**: FastAPI with Python 3.11
- **Features**:
  - RESTful API endpoints for interview management
  - AI-powered question generation using OpenAI GPT
  - Intelligent answer evaluation and scoring
  - In-memory session management
  - Comprehensive performance report generation
  - CORS enabled for frontend communication

### Frontend (HTML/CSS/JavaScript)
- **Location**: `frontend/` folder
- **Technology**: Vanilla HTML, CSS, and JavaScript
- **Features**:
  - Responsive design for desktop and mobile
  - Progressive interview flow with visual feedback
  - Real-time progress tracking
  - Clean, professional UI with gradient design
  - Error handling and loading states

## API Endpoints

### `POST /interview/start`
Initiates a new mock interview session.
- **Response**: `{interview_id: string, first_question: string}`

### `POST /interview/{interview_id}/answer`
Submits an answer to the current question.
- **Request**: `{answer: string}`
- **Response**: `{next_question: string|null, feedback: string, interview_completed: boolean}`

### `GET /interview/{interview_id}/report`
Retrieves the final performance report.
- **Response**: `{report: string}`

### `GET /`
Health check endpoint.
- **Response**: `{message: string}`

## Setup and Installation

### Prerequisites
- Python 3.11+
- Mistral AI API key 
- Modern web browser

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export MISTRAL_API_KEY="your-mistral-api-key"
   ```

4. Run the FastAPI server:
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start a local web server:
   ```bash
   python -m http.server 3000
   ```
   The frontend will be available at `http://localhost:3000`

## Usage

1. **Start the Backend**: Ensure the FastAPI server is running on port 8000
2. **Open the Frontend**: Access the web interface at `http://localhost:3000`
3. **Begin Interview**: Click "Start Interview" to begin the assessment
4. **Answer Questions**: Provide detailed answers to each Excel-related question
5. **Review Report**: View your comprehensive performance summary at the end

## Testing

### Backend API Testing
Run the included test script:
```bash
cd backend
python test_api.py
```

### Manual Testing
1. Start both backend and frontend servers
2. Navigate through the complete interview flow
3. Verify all features work as expected

## Key Features

### AI-Powered Question Generation
- Dynamic question generation based on conversation history
- Progressive difficulty scaling
- Contextual follow-up questions

### Intelligent Answer Evaluation
- AI-based scoring (1-10 scale)
- Constructive feedback for each response
- Knowledge assessment tracking

### Comprehensive Reporting
- Detailed performance analysis
- Strengths and improvement areas
- Professional hiring recommendations

### User Experience
- Clean, intuitive interface
- Real-time progress tracking
- Responsive design for all devices
- Loading states and error handling

## Technology Choices

### Backend: FastAPI
- **Why**: High performance, automatic API documentation, excellent async support
- **Benefits**: Fast development, built-in validation, modern Python features

### Frontend: Vanilla JavaScript
- **Why**: Simplicity, no build process, universal compatibility
- **Benefits**: Lightweight, fast loading, easy to understand and modify

### AI: OpenAI GPT-3.5-turbo
- **Why**: Excellent natural language understanding and generation
- **Benefits**: Contextual question generation, intelligent answer evaluation

## Project Structure

```
ai_excel_interviewer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── test_api.py         # API test script
│   └── api_design.md       # API documentation
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # CSS styles
│   ├── script.js           # JavaScript functionality
│   └── frontend_outline.md # Frontend documentation
└── README.md               # This file
```

## Future Enhancements

- Database integration for persistent storage
- User authentication and session management
- Advanced analytics and reporting
- Multiple interview templates
- Integration with HR systems
- Mobile app development

## License

This project is a proof-of-concept for the AI Engineer Assignment.

## Support

For questions or issues, please refer to the project documentation or contact the development team.

