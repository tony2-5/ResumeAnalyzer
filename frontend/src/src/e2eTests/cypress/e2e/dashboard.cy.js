const email = "test2@test.com"
const password = "dietdew"
const jobDescription = "An experienced and self-motivated Test Engineer with a strong technical background, proficient in acceptance testing, exploratory testing, and test management, skilled in creating and executing test plans, documenting results, improving testing strategies, and collaborating with teams to deliver high-quality software solutions while ensuring attention to detail and effective problem-solving."

describe('Dashboard', () => {
    before(()=>{
        cy.intercept('POST', "http://localhost:8000/api/register").as('registerRequest');

		cy.visit('http://localhost:3000/register')
		cy.get('#registerEmail').type(email)
		cy.get('#username').type('test2')
		cy.get('#registerPassword').type(password)
		cy.get('#confirmPassword').type(password)

		cy.get('button').contains("Register").click()
    })
    
    beforeEach(()=> {
        cy.visit('http://localhost:3000/login')
        cy.get('#email').type(email)
		cy.get('#password').type(password)	
		cy.get('button').contains("Login").click()
        cy.wait(2000)
    })

	it('Correct Url', () => {
		cy.url().should('include', '/dashboard')
	})

    it("Validate elements rendered correctly", ()=> {
    // buttons
        cy.get('button').contains('Sign Out').should('exist')
        cy.get('button').contains('Upload Resume').should('exist')
        cy.get('button').contains('Upload Job Description').should('exist')
        cy.get('button').contains('Download PDF Report').should('exist')
        // headers
        cy.contains('Upload Resume').should('exist')
        cy.contains('Upload Job Description').should('exist')
        cy.contains('Resume Analysis Results').should('exist')
        cy.contains('Resume Fit Score').should('exist')
        cy.contains('Skills and Keywords Matched').should('exist')
        cy.contains('Improvement Suggestions').should('exist')
        // upload elements
        cy.get('[data-testid="resume"]').should('exist')
        cy.get('[data-testid="description"]').should('exist')
        // other
        cy.get('.progress').should('exist') // fitscore bar
        cy.get('select').should('exist')
        cy.get('select').children('option').should('have.length', 5)
    })

    it('Can sign out', ()=>{
        cy.get('button').contains('Sign Out').click()
        cy.url().should('include', '/login')
    })

    it('Uploads Resume', () => {
        cy.get('button').contains('Upload Resume').click()
        cy.contains("Please select a resume file to upload.").should('exist')
        cy.get('[data-testid="resume"]').selectFile('cypress/files/testresume.pdf')
        cy.get('button').contains('Upload Resume').click()
        cy.contains("Resume uploaded successfully.").should('exist')
    })

    it('Uploads Job Description', () => {
        cy.get('button').contains('Upload Job Description').click()
        cy.contains("Please enter a job description.").should('exist')
        cy.get('[data-testid="description"]').type("ksjdfhsdk")
        cy.get('button').contains('Upload Job Description').click()
        cy.contains("Upload resume first.").should('exist')

        cy.get('[data-testid="resume"]').selectFile('cypress/files/testresume.pdf')
        cy.get('button').contains('Upload Resume').click()

        cy.get('button').contains('Upload Job Description').click()

        // means job description accepted
        cy.get('.spinner-container').should('exist')
    })

    it('Data populates dashboard', () => {
        cy.get('button').contains('Upload Job Description').click()
        cy.contains("Please enter a job description.").should('exist')
        cy.get('[data-testid="description"]').type(jobDescription)
        cy.get('button').contains('Upload Job Description').click()
        cy.contains("Upload resume first.").should('exist')

        cy.get('[data-testid="resume"]').selectFile('cypress/files/testresume.pdf')
        cy.get('button').contains('Upload Resume').click()

        cy.get('button').contains('Upload Job Description').click() 

        cy.get('.spinner-container').should('not.exist', { timeout: 25000 }); // make sure loading done

        // suggestions and skills get populated
        cy.get(".dashboard > :nth-child(3) > ul > li")
        cy.get(".dashboard > :nth-child(4) > ul > li")
    })

    it('Download pdf works', () => {
        cy.get('button').contains('Upload Job Description').click()
        cy.contains("Please enter a job description.").should('exist')
        cy.get('[data-testid="description"]').type(jobDescription)
        cy.get('button').contains('Upload Job Description').click()
        cy.contains("Upload resume first.").should('exist')

        cy.get('[data-testid="resume"]').selectFile('cypress/files/testresume.pdf')
        cy.get('button').contains('Upload Resume').click()

        cy.get('button').contains('Upload Job Description').click()

        cy.get('.spinner-container').should('not.exist', { timeout: 25000 }); // make sure loading done

        cy.get('button').contains('Download PDF Report').click()

        cy.readFile("cypress/downloads/Resume_Analysis_Report.pdf", { timeout: 10000 }).should('exist');

        // Use pdf-parse to extract text from the PDF
        cy.task('readPdf', "cypress/downloads/Resume_Analysis_Report.pdf").then((pdfText) => {
            // Validate PDF content
            expect(pdfText).to.include('Resume Analysis Report');
            expect(pdfText).to.include('Fit Score:');
            expect(pdfText).to.include('Matched Keywords:');
            expect(pdfText).to.include('Feedback:');
        });

        // delete user incase tests ever rerun
        cy.request({method: "DELETE",url: "http://localhost:8000/api/delete_user",qs: { email: email }})
    })
})
