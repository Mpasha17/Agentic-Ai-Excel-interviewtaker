
# Frontend Outline

## Components:

### 1. `InterviewPage`
- Displays the current question.
- Provides an input field for the candidate's answer.
- Handles submission of answers.
- Displays loading indicators during API calls.

### 2. `ReportPage`
- Displays the final performance summary report.
- Presents detailed feedback for each question.

### 3. `HomePage` (Optional)
- A simple landing page to start the interview.

## Interactions:

- **Start Interview:** User clicks a 


button to start the interview, triggering a call to `/interview/start`.
- **Submit Answer:** User types an answer and submits it, triggering a call to `/interview/{interview_id}/answer`.
- **Display Next Question/Feedback:** The frontend updates based on the backend response, either displaying the next question or indicating interview completion.
- **View Report:** Once the interview is completed, the frontend navigates to the `ReportPage` and fetches the report from `/interview/{interview_id}/report`.

