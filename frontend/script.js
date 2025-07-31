class ExcelInterviewer {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.interviewId = null;
        this.currentQuestionNumber = 1;
        this.totalQuestions = 5;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Start interview button
        document.getElementById('start-interview-btn').addEventListener('click', () => {
            this.startInterview();
        });

        // Submit answer button
        document.getElementById('submit-answer-btn').addEventListener('click', () => {
            this.submitAnswer();
        });

        // New interview button
        document.getElementById('new-interview-btn').addEventListener('click', () => {
            this.resetToHome();
        });

        // Enter key in textarea
        document.getElementById('answer-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.submitAnswer();
            }
        });
    }

    showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show target page
        document.getElementById(pageId).classList.add('active');
    }

    showLoading(show = true) {
        document.getElementById('loading').style.display = show ? 'flex' : 'none';
    }

    updateProgress() {
        const progressPercent = (this.currentQuestionNumber / this.totalQuestions) * 100;
        document.getElementById('progress-fill').style.width = `${progressPercent}%`;
        document.getElementById('question-counter').textContent = 
            `Question ${this.currentQuestionNumber} of ${this.totalQuestions}`;
    }

    async startInterview() {
        try {
            this.showLoading(true);
            
            const response = await fetch(`${this.baseURL}/interview/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.interviewId = data.interview_id;
            this.currentQuestionNumber = 1;
            
            // Display first question
            document.getElementById('current-question').textContent = data.first_question;
            document.getElementById('answer-input').value = '';
            document.getElementById('feedback-section').style.display = 'none';
            
            this.updateProgress();
            this.showPage('interview-page');
            
        } catch (error) {
            console.error('Error starting interview:', error);
            alert('Failed to start interview. Please make sure the backend server is running on http://localhost:8000');
        } finally {
            this.showLoading(false);
        }
    }

    async submitAnswer() {
        const answerInput = document.getElementById('answer-input');
        const answer = answerInput.value.trim();
        
        if (!answer) {
            alert('Please provide an answer before submitting.');
            return;
        }

        if (!this.interviewId) {
            alert('No active interview session.');
            return;
        }

        try {
            this.showLoading(true);
            document.getElementById('submit-answer-btn').disabled = true;
            
            const response = await fetch(`${this.baseURL}/interview/${this.interviewId}/answer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ answer: answer })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Show feedback
            if (data.feedback) {
                document.getElementById('feedback-text').textContent = data.feedback;
                document.getElementById('feedback-section').style.display = 'block';
            }
            
            if (data.interview_completed) {
                // Interview is complete, show report after a delay
                setTimeout(() => {
                    this.showReport();
                }, 2000);
            } else {
                // Continue with next question
                setTimeout(() => {
                    this.currentQuestionNumber++;
                    document.getElementById('current-question').textContent = data.next_question;
                    answerInput.value = '';
                    document.getElementById('feedback-section').style.display = 'none';
                    document.getElementById('submit-answer-btn').disabled = false;
                    this.updateProgress();
                }, 2000);
            }
            
        } catch (error) {
            console.error('Error submitting answer:', error);
            alert('Failed to submit answer. Please try again.');
            document.getElementById('submit-answer-btn').disabled = false;
        } finally {
            this.showLoading(false);
        }
    }

    async showReport() {
        try {
            this.showLoading(true);
            
            const response = await fetch(`${this.baseURL}/interview/${this.interviewId}/report`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Display the report
            document.getElementById('report-content').textContent = data.report;
            this.showPage('report-page');
            
        } catch (error) {
            console.error('Error fetching report:', error);
            document.getElementById('report-content').textContent = 
                'Failed to generate report. Please try again later.';
            this.showPage('report-page');
        } finally {
            this.showLoading(false);
        }
    }

    resetToHome() {
        this.interviewId = null;
        this.currentQuestionNumber = 1;
        document.getElementById('submit-answer-btn').disabled = false;
        this.showPage('home-page');
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ExcelInterviewer();
});

