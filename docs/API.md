# Resume Analyzer API Documentation

## Authentication Endpoints
### **POST** `api/register`

#### Description
This endpoint registers a new user. If the provided email is already registered, the request will return an error.

#### Status Code
- **201 Created**: User successfully registered.
- **400 Bad Request**: Email is already registered.

**Request Body Example:**
```
{
    "email": "johndoe@example.com",
    "username": "johndoe",
    "password": "securepassword123"
}
```
**Response Example:**
```
{
    "message": "User registered."
}
```
### **POST** `api/login`

#### Description
This endpoint authenticates a user and returns a JSON Web Token (JWT) for subsequent requests.

#### Status Code
- **200 OK**: Authentication successful, JWT token returned.
- **400 Bad Request**: Invalid email or password.

**Request Body Example:**
```
{
    "email": "johndoe@example.com",
    "password": "securepassword123"
}
```
**Response Example:**
```
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "bearer"
}
```
### **GET** `api/users/me`

#### Description
This endpoint retrieves the current logged-in user's information based on the provided JWT token.

#### Status Code
- **200 OK**: User information retrieved successfully.
- **404 Not Found**: User not found.

**Request Headers Example:**
Authorization: Bearer `<your-jwt-token>`

**Response Example:**
```
{
    "email": "johndoe@example.com",
    "username": "johndoe"
}
```
### **DELETE** `api/delete_user`

#### Description
This endpoint deletes a user by their email address.

#### Status Code
- **200 OK**: User deleted successfully.
- **404 Not Found**: User not found.

**Request Body Example:**
```
{
    "email": johndoe@example.com
}
```
**Response Example:**
```
{ 
    "message": "User with email johndoe@example.com deleted successfully." 
}
```
## Analysis Endpoints

### **POST** `api/resume-upload`

#### Description
This endpoint allows users to upload a resume (PDF file) to the backend's temporary storage. It validates the file type and size, then extracts text from the PDF for future processing.

#### Status Code
- **200 OK**: Resume uploaded successfully.
- **400 Bad Request**: Invalid file type or file size exceeds the limit.

**Request Headers Example:** Session-Token: `<your-session-token>`

**Request Example:**
A PDF file (`resumeFile`) is required as part of the form-data.

**Response Example:**
```
{ 
    "message": "Resume uploaded successfully.", 
    "token": "<session-token>" 
}
```

### **POST** `api/job-description`

#### Description
This endpoint allows users to upload a resume (PDF file) to the backend's temporary storage. It validates the file type and size, then extracts text from the PDF for future processing.

#### Status Code
- **200 OK**: Resume uploaded successfully.
- **400 Bad Request**: Invalid file type or file size exceeds the limit.

**Request Headers Example:** Session-Token: `<your-session-token>`

**Request Example:**
```
{
    "job_description": "We are looking for a software engineer with expertise in Python and AI."
}
```

**Response Example:**
```
{ 
    "job_description": "We are looking for a software engineer with expertise in Python and AI.",
    "token": "<session-token>" 
}
```

### **GET** `api/resume-data`

#### Description
This endpoint retrieves the resume data from temporary storage based on the provided session token. It checks if the session exists and returns the associated data.

#### Status Code
- **200 OK**: Session data retrieved successfully.
- **404 Not Found**: Session not found.

**Request Headers Example:** Session-Token: `<your-session-token>`

**Response Example:**
```
{
  "message": "Session data retrieved successfully.",
  "data": {
    "resume_text": "Extracted text from the uploaded resume",
    "job_description": "Job description text"
  }
}
```

### **POST** `api/analyze`

#### Description
This endpoint analyzes the resume and job description to generate a fit score, skills matched, and feedback for improvement. It requires both the resume text and job description to be available in temporary storage. The analysis is performed using an external API (Hugging Face).

#### Status Code
- **200 OK**: Analysis completed successfully.
- **400 Bad Request**: Missing or invalid resume text or job description.
- **404 Not Found**: Session not found.
  
**Request Headers Example:** Authorization: `<your-session-token>`

**Request Example (Optional):**
- Also optional to pass session token in request body.
```
{
    sessionToken: <your-session-token>
}
```
**Response Example:**
```
{
    "fitScore": 85,
    "jobDescriptionSkills": {
        "preferred": ["AI expertise", "Advanced Python"],
        "required": ["Python", "Machine Learning"]
    },
    "suggestions": [
        "Highlight relevant experience in AI projects.",
        "Add certifications in Python."
    ]
}
```

### **POST** `api/fit-score`

#### Description
This endpoint calculates the fit score based on the resume text and job description, and provides feedback including matched and missing keywords.

#### Status Code
- **200 OK**: Fit score calculated successfully.
- **400 Bad Request**: Invalid or missing resume text or job description.
  
**Request Headers Example:** Session-Token: `<your-session-token>`
**Request Example:**
```
{
    "resumeText": "Experienced software engineer with expertise in Python and machine learning.",
    "jobDescription": "We are looking for a Python developer with experience in AI and machine learning."
}
```
**Response Example:**
```
{
    "fitScore": 90,
    "matchedKeywords": ["Python", "machine learning", "AI"],
    "missingKeywords": ["Deep Learning", "Cloud Computing"],
    "feedback": "Consider adding experience with Deep Learning and Cloud Computing to improve fit."
}
```