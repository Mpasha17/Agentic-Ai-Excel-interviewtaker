
# Backend API Design

## Endpoints:

### 1. `POST /interview/start`
- **Description:** Initiates a new mock Excel interview.
- **Request Body:** None
- **Response:**
  ```json
  {
    "interview_id": "string",
    "first_question": "string"
  }
  ```

### 2. `POST /interview/{interview_id}/answer`
- **Description:** Submits a candidate's answer to the current question.
- **Request Body:**
  ```json
  {
    "answer": "string"
  }
  ```
- **Response:**
  ```json
  {
    "next_question": "string" | null,
    "feedback": "string" | null,
    "interview_completed": "boolean"
  }
  ```

### 3. `GET /interview/{interview_id}/report`
- **Description:** Retrieves the final performance summary report for a completed interview.
- **Request Body:** None
- **Response:**
  ```json
  {
    "report": "string"
  }
  ```

## Data Models:

### InterviewState
- `interview_id`: Unique identifier for the interview.
- `current_question`: The question currently asked.
- `conversation_history`: List of past questions and answers.
- `evaluation_results`: Stores evaluation of each answer.
- `is_completed`: Boolean indicating if the interview is finished.

### FeedbackReport
- `interview_id`: Unique identifier for the interview.
- `summary`: Overall performance summary.
- `detailed_feedback`: Specific feedback points for each question/answer.


