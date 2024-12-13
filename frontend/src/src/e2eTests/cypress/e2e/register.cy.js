export const email = "test2@test.com"
export const password = "dietdew"

describe('User Register', () => {
    it('Allows access to the site', () => {
        cy.visit('http://localhost:3000')
        cy.url().should('include', '/login')
    })
    it('Navigates to register page', () => {
        cy.visit('http://localhost:3000')
        cy.get('a').contains('Register here').click()
        cy.url().should('include', '/register')
    })
    it('Checks for empty register fields', () => {
        cy.visit('http://localhost:3000/register')
        cy.get('#registerEmail:invalid')
        .invoke('prop', 'validationMessage')
        .should('not.be.empty');
        cy.get('#registerEmail').type('sdfsd@gdsf.com')

        cy.get('#username:invalid')
        .invoke('prop', 'validationMessage')
        .should('not.be.empty');
        cy.get('#username').type('dsfsdfsd')

        cy.get('#registerPassword:invalid')
        .invoke('prop', 'validationMessage')
        .should('not.be.empty');
        cy.get('#registerPassword').type('dietdew')

        cy.get('#confirmPassword:invalid')
        .invoke('prop', 'validationMessage')
        .should('not.be.empty');
        cy.get('#confirmPassword').type('dietdew')
    })

    it('Checks for invalid email', () => {
		cy.visit('http://localhost:3000/register')
		cy.get('#username').type('dsfsdfsd')
		cy.get('#registerPassword').type('dietdew')
		cy.get('#confirmPassword').type('dietdew')

        cy.get('#registerEmail').type('sdfsd')
        cy.get('#registerEmail:invalid')
        .invoke('prop', 'validationMessage')
        .should('not.be.empty')

		cy.get('#registerEmail').clear()
		cy.get('#registerEmail').type('sdfsd@fsd')
        
		cy.get('button').contains("Register").click()

		cy.get('.error').contains("Invalid email address.").should('exist')
    })

	it('Checks for invalid password', () => {
		cy.visit('http://localhost:3000/register')
		cy.get('#registerEmail').type('sdfsd@fsd.com')
		cy.get('#username').type('dsfsdfsd')
		cy.get('#registerPassword').type('cokezero')
		cy.get('#confirmPassword').type('dietdew')
        
		cy.get('button').contains("Register").click()

		cy.get('.error').contains("Passwords do not match.").should('exist')
    })

	it('Allows a user to register', () => {
		cy.intercept('POST', "http://localhost:8000/api/register").as('registerRequest');

		cy.visit('http://localhost:3000/register')
		cy.get('#registerEmail').type(email)
		cy.get('#username').type('test2')
		cy.get('#registerPassword').type(password)
		cy.get('#confirmPassword').type(password)
        
		// incase user already exists
		cy.request({method: "DELETE",url: "http://localhost:8000/api/delete_user",qs: { email: email }})

		cy.get('button').contains("Register").click()
	
		cy.wait('@registerRequest').then((interception) => {
            expect(interception.response.statusCode).to.eq(201);
            expect(interception.response.body).to.have.property(
                "message",
                "User registered."
            );
        });
	})

	it('Checks if user already registered', () => {
		cy.visit('http://localhost:3000/register')
		cy.get('#registerEmail').type(email)
		cy.get('#username').type('test2')
		cy.get('#registerPassword').type(password)
		cy.get('#confirmPassword').type(password)
        
		cy.get('button').contains("Register").click()

		cy.get('.error').contains("Email already registered.").should('exist')
	})
})

// cy.request({method: "DELETE",url: "http://localhost:8000/api/delete_user",qs: { email: 'test2@test.com' }})
// .then((response) => {
// 	expect(response.body).to.have.property(
// 		"message",
// 		`User with email test2@test.com has been deleted.`
// 	);
// });