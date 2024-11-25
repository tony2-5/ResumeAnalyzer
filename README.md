# Project: Resume Analyzer
Our project aims to allow users to upload their resume and receive feedback and job recommendations based on the resume's content. Using natural language processing, our application is able to suggest content changes to resumes, such as wording, structure, and missing skills. Using machine learning, our application is able to offer job recommendations based on keywords and skills.
## Goals:
#### 1.  **User Registration and Authentication**
-   **Functionality**:
    -   Allow users to sign up with an email and password.
    -   Implement login and logout functionalities using a secure authentication method.
    -   Maintain session management to keep users logged in.
#### 2.  **Resume and Job Description Input**
-   **Functionality**:
    -   Users can upload a resume as a PDF or paste in text directly.
    -   Users can upload or paste in a job description.
    -   No persistent storage of files—data should be temporarily held in memory for processing.
    -   Validate inputs (e.g., file size/type and character limits for pasted text).

#### 3.  **AI-Powered Resume Analysis and Job Matching**
-   **Functionality**:
    -   Utilize an NLP model to analyze resume content against job descriptions.
    -   Assess whether the resume aligns with the job requirements and assign a "fit score."
    -   Provide feedback on how to improve the resume for better alignment with the job description.
#### 4.  **Real-Time Feedback and Suggestions**

-   **Functionality**:
    -   Once users provide their resume and job description, display real-time feedback on a dashboard.
    -   Allow users to download a report with suggestions if needed.
## Tech Stack
 -   **Communication Protocol**:
	    -   **REST**
-   **Backend**:
    -   Python: **FastAPI**.
-   **Frontend**:
    -   Javascript: **React.js**.
-  	**NLP API**:
	 -   **OpenAI**.
## Team: 
1. Anthony Dvorsky
	* Email: ajd99@njit.edu
2. Matthew Choi
	 * Email: mjc@njit.edu
3. Ryan Kulfan 
	* Email: rpk36@njit.edu
4. Shengfu Deng
	* Email: sd972@njit.edu
5. Dev Patel
	* Email: dmp36@njit.edu
## Project Setup
### Backend Setup
1. Setup python virtual environment using `python -m venv venv` from the main directory
2. Activate virtual environment with `source venv/bin/activate` (using mac may differ for other operating systems)
3. Install python backend dependencies using `pip install -r ./requirements.txt` from the main directory
4. Go to backend folder with `cd ./backend`
5. Create a file inside of the backend directory called `.env`
6. Within the .env file define a variable `JWT_KEY` and set it equal to the output of running `openssl rand -hex 32` in the terminal.
7. Run the backend using `fastapi dev main.py`
### Frontend Setup
1. Return to the main directory
2. From the main directory go to the frontend/src folder with `cd ./frontend/src`
3. Run `npm install` to install dependencies
4. Run the frontend using `npm start`