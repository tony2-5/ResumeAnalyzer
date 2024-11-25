import { render, screen, fireEvent, waitFor, act  } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Register from '../components/Register';
import axiosInstance from '../api/axios';

// Mock axiosInstance
jest.mock('../api/axios');

describe('Register Component', () => {

	test('renders registration form with email, username, password, confirm password, and submit button', () => {
		render(
			<MemoryRouter>
				<Register />
			</MemoryRouter>
		);
		expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
		expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
		expect(screen.getByTestId('registerPassword')).toBeInTheDocument();
		expect(screen.getByTestId('confirmPassword')).toBeInTheDocument();
		expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
	});

	test('check for login here link', async () => {
		render(
			<MemoryRouter>
				<Register />
			</MemoryRouter>
		);

		expect(screen.getByRole('link', { name: 'Login here'})).toHaveAttribute('href', '/login')
	});

	test('shows error message with invalid email', async () => {
		render(
			<MemoryRouter>
				<Register />
			</MemoryRouter>
		);

		fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'wrong@exa' } });
		fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'wrong' } });
		fireEvent.change(screen.getByTestId('registerPassword'), { target: { value: 'wrongpassword' } });
		fireEvent.change(screen.getByTestId('confirmPassword'), { target: { value: 'wrongpassword' } });

		fireEvent.click(screen.getByRole('button', { name: /register/i }));

		await waitFor(() => {
			expect(screen.getByText(/invalid email address/i)).toBeInTheDocument();
		});
	});

	test('displays error message when API call fails', async () => {
		axiosInstance.post.mockRejectedValueOnce({
			response: { data: { detail: 'Email is already in use.' } },
		});

		render(
			<MemoryRouter>
				<Register />
			</MemoryRouter>
		);

		fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
		fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
		fireEvent.change(screen.getByTestId('registerPassword'), { target: { value: 'password123' } });
		fireEvent.change(screen.getByTestId('confirmPassword'), { target: { value: 'password123' } });

		fireEvent.click(screen.getByRole('button', { name: /register/i }));

		// Wait for the error message to appear
		await waitFor(() => {
			expect(screen.getByText(/email is already in use/i)).toBeInTheDocument();
		});

		expect(axiosInstance.post).toHaveBeenCalledWith('/api/register', {
			email: 'test@example.com',
			username: 'testuser',
			password: 'password123',
		});
	});

	test('allows for successful registration', async () => {
		axiosInstance.post.mockResolvedValueOnce({
			data: { message: 'User registered.' },
		});

		render(
			<MemoryRouter>
				<Register />
			</MemoryRouter>
		);

		fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
		fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
		fireEvent.change(screen.getByTestId('registerPassword'), { target: { value: 'password123' } });
		fireEvent.change(screen.getByTestId('confirmPassword'), { target: { value: 'password123' } });

		await act(async () => {
			fireEvent.click(screen.getByRole('button', { name: /register/i }));
		});  

		expect(axiosInstance.post).toHaveBeenCalledWith('/api/register', {
			email: 'test@example.com',
			username: 'testuser',
			password: 'password123',
		});
	});
});