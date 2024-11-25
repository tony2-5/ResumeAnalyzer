import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Login from '../components/Login';
import axiosInstance from '../api/axios';

// Mock axiosInstance
jest.mock('../api/axios');
describe('Login Component', () => {

	beforeAll(() => {
		delete window.location; // Delete the original location object
		window.location = { reload: jest.fn() }; // Mock the reload method
	});
  
  	afterAll(() => {
    	// Clean up the mock after all tests
    	delete window.location;
  	});

	test('renders login form with email, password, and submit button', () => {
		render(
		<MemoryRouter>
			<Login />
		</MemoryRouter>
		);
		expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
		expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
		expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
	});
	
	test('check for register here link', async () => {
		render(
		<MemoryRouter>
			<Login />
		</MemoryRouter>
		);

		expect(screen.getByRole('link', { name: 'Register here'})).toHaveAttribute('href', '/register')
	});

	test('shows error message with invalid email', async () => {
		render(
		<MemoryRouter>
			<Login />
		</MemoryRouter>
		);

		fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'wrong@exa' } });
		fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrongpassword' } });

		fireEvent.click(screen.getByRole('button', { name: /login/i }));

		await waitFor(() => {
		expect(screen.getByText(/invalid email address/i)).toBeInTheDocument();
		});
	});

	test('shows error message when login API fails', async () => {
		// Mock failed login response
		axiosInstance.post.mockRejectedValueOnce({ response: { data: { detail: 'Invalid credentials' } } });

		render(
		<MemoryRouter>
			<Login />
		</MemoryRouter>
		);

		fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'wrong@example.com' } });
		fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrongpassword' } });

		fireEvent.click(screen.getByRole('button', { name: /login/i }));

		await waitFor(() => {
		expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
		});
	});

	test('submits form with correct credentials and stores token in localStorage', async () => {
		// Mock successful API response
		axiosInstance.post.mockResolvedValueOnce({ data: { accessToken: 'dummy_token' } });
	
		// Mock localStorage.setItem
		const setItemMock = jest.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {});
	
		render(
		<MemoryRouter>
			<Login />
		</MemoryRouter>
		);
	
		fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
		fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });

		fireEvent.click(screen.getByRole('button', { name: /login/i }));
	
		// Wait for the localStorage.setItem to be called
		await waitFor(() => {
		expect(setItemMock).toHaveBeenCalledWith('accessToken', 'dummy_token');
		});
	
		// Clean up mock
		setItemMock.mockRestore();
	});
});
