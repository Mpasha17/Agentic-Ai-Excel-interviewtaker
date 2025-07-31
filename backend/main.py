from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from mistralai.client import MistralClient
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional

app = FastAPI(title="AI Excel Mock Interviewer", version="1.0.0")

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mistral AI client setup
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "mistral-large-latest"
client = MistralClient(api_key=API_KEY)

# In-memory storage for interview sessions
interview_sessions: Dict[str, dict] = {}

# Pydantic models
class AnswerRequest(BaseModel):
    answer: str

class InterviewStartResponse(BaseModel):
    interview_id: str
    first_question: str

class AnswerResponse(BaseModel):
    next_question: Optional[str]
    feedback: Optional[str]
    interview_completed: bool

class ReportResponse(BaseModel):
    report: str

# Excel interview questions pool
EXCEL_QUESTIONS = [
    "Can you explain the difference between VLOOKUP and HLOOKUP functions in Excel?",
    "How would you use pivot tables to analyze sales data by region and product category?",
    "What is the purpose of the INDEX and MATCH functions, and how do they work together?",
    "Describe how you would use conditional formatting to highlight cells based on specific criteria.",
    "How would you create a dynamic chart that updates automatically when new data is added?",
    "Explain the difference between absolute and relative cell references with examples.",
    "How would you use the SUMIFS function to calculate totals based on multiple criteria?",
    "What are some best practices for organizing and structuring large Excel workbooks?"
]

def generate_question_with_ai(conversation_history: List[dict], question_number: int) -> str:
    """Generate a contextual Excel interview question using AI"""
    if question_number == 1:
        return EXCEL_QUESTIONS[0]  # Start with a basic question
    
    # Use AI to generate follow-up questions based on conversation history
    prompt = f"""You are an Excel expert conducting a technical interview. Based on the conversation history below, generate the next appropriate Excel-related question. The question should:
1. Be progressively more challenging
2. Test different Excel skills (formulas, data analysis, visualization, etc.)
3. Be relevant to a professional Excel user
4. Be clear and specific

Conversation history:
{conversation_history}

Generate only the next question, no additional text:"""

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback to predefined questions if AI fails
        return EXCEL_QUESTIONS[min(question_number - 1, len(EXCEL_QUESTIONS) - 1)]

def evaluate_answer_with_ai(question: str, answer: str) -> dict:
    """Evaluate the candidate's answer using AI"""
    prompt = f"""You are an Excel expert evaluating a candidate's answer in a technical interview. 

Question: {question}
Answer: {answer}

Evaluate the answer and provide:
1. A score from 1-10 (10 being excellent)
2. Brief feedback (2-3 sentences)
3. Whether the answer demonstrates good Excel knowledge (true/false)

Respond in this exact format:
Score: [number]
Feedback: [feedback text]
Knowledge: [true/false]"""

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        lines = content.split('\n')
        
        score = 5  # default
        feedback = "Answer received."
        knowledge = True
        
        for line in lines:
            if line.startswith("Score:"):
                try:
                    score = int(line.split(":")[1].strip())
                except:
                    pass
            elif line.startswith("Feedback:"):
                feedback = line.split(":", 1)[1].strip()
            elif line.startswith("Knowledge:"):
                knowledge = line.split(":")[1].strip().lower() == "true"
        
        return {"score": score, "feedback": feedback, "knowledge": knowledge}
    except Exception as e:
        return {"score": 5, "feedback": "Answer received and noted.", "knowledge": True}

def generate_final_report(interview_data: dict) -> str:
    """Generate a comprehensive final report using AI"""
    conversation_history = interview_data.get("conversation_history", [])
    evaluations = interview_data.get("evaluations", [])
    
    prompt = f"""Generate a comprehensive Excel interview performance report based on the following data:

Conversation History:
{conversation_history}

Evaluations:
{evaluations}

Create a professional report that includes:
1. Overall performance summary
2. Strengths demonstrated
3. Areas for improvement
4. Specific recommendations
5. Overall recommendation (Hire/Don't Hire/Further Assessment)

Make it detailed but concise, suitable for HR and hiring managers."""

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Report generation failed. Please review the interview manually."

@app.post("/interview/start", response_model=InterviewStartResponse)
async def start_interview():
    """Start a new Excel mock interview"""
    interview_id = str(uuid.uuid4())
    first_question = generate_question_with_ai([], 1)
    
    interview_sessions[interview_id] = {
        "interview_id": interview_id,
        "current_question": first_question,
        "conversation_history": [{"type": "question", "content": first_question}],
        "evaluations": [],
        "question_number": 1,
        "is_completed": False
    }
    
    return InterviewStartResponse(
        interview_id=interview_id,
        first_question=first_question
    )

@app.post("/interview/{interview_id}/answer", response_model=AnswerResponse)
async def submit_answer(interview_id: str, answer_request: AnswerRequest):
    """Submit an answer to the current question"""
    if interview_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    session = interview_sessions[interview_id]
    if session["is_completed"]:
        raise HTTPException(status_code=400, detail="Interview already completed")
    
    current_question = session["current_question"]
    answer = answer_request.answer
    
    # Add answer to conversation history
    session["conversation_history"].append({"type": "answer", "content": answer})
    
    # Evaluate the answer
    evaluation = evaluate_answer_with_ai(current_question, answer)
    session["evaluations"].append({
        "question": current_question,
        "answer": answer,
        "evaluation": evaluation
    })
    
    # Determine if interview should continue (max 5 questions)
    if session["question_number"] >= 5:
        session["is_completed"] = True
        return AnswerResponse(
            next_question=None,
            feedback=evaluation["feedback"],
            interview_completed=True
        )
    
    # Generate next question
    session["question_number"] += 1
    next_question = generate_question_with_ai(session["conversation_history"], session["question_number"])
    session["current_question"] = next_question
    session["conversation_history"].append({"type": "question", "content": next_question})
    
    return AnswerResponse(
        next_question=next_question,
        feedback=evaluation["feedback"],
        interview_completed=False
    )

@app.get("/interview/{interview_id}/report", response_model=ReportResponse)
async def get_report(interview_id: str):
    """Get the final performance report for a completed interview"""
    if interview_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    session = interview_sessions[interview_id]
    if not session["is_completed"]:
        raise HTTPException(status_code=400, detail="Interview not yet completed")
    
    report = generate_final_report(session)
    return ReportResponse(report=report)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Excel Mock Interviewer API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

