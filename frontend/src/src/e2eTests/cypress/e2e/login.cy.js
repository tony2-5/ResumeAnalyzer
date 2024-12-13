const email = "test2@test.com"
const password = "dietdew"

describe('User Login', () => {
    before(()=>{
        cy.intercept('POST', "http://localhost:8000/api/register").as('registerRequest');

		cy.visit('http://localhost:3000/register')
		cy.get('#registerEmail').type(email)
		cy.get('#username').type('test2')
		cy.get('#registerPassword').type(password)
		cy.get('#confirmPassword').type(password)

		cy.get('button').contains("Register").click()
    })
    
	it('Allows access to the site', () => {
		cy.visit('http://localhost:3000')
		cy.url().should('include', '/login')
	})

	it('Checks for empty login fields', () => {
		cy.visit('http://localhost:3000/login')
		cy.get('#email:invalid')
		.invoke('prop', 'validationMessage')
		.should('not.be.empty');
		cy.get('#email').type('sdfsd@gdsf.com')

		cy.get('#password:invalid')
		.invoke('prop', 'validationMessage')
		.should('not.be.empty');
		cy.get('#password').type('dsfsdfsd')
	})

	it('Checks for invalid email', () => {
		cy.visit('http://localhost:3000/login')
		cy.get('#password').type(password)

		cy.get('#email').type('sdfsd')
		cy.get('#email:invalid')
		.invoke('prop', 'validationMessage')
		.should('not.be.empty')

		cy.get('#email').clear()
		cy.get('#email').type('sdfsd@fsd')
			
		cy.get('button').contains("Login").click()

		cy.get('.error').contains("Invalid email address.").should('exist')
	})

	it('Dashboard route is protected', () => {
		cy.visit('http://localhost:3000/dashboard')
		
		cy.url().should('include', '/login')
	})

	it('Allows a user to login', () => {
		cy.visit('http://localhost:3000/login')
		cy.get('#email').type(email)
		cy.get('#password').type(password)
			
		cy.get('button').contains("Login").click()

		cy.url().should('include', '/dashboard')

        // delete user incase tests ever rerun
        cy.request({method: "DELETE",url: "http://localhost:8000/api/delete_user",qs: { email: email }})
  	})
})