import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Dashboard from '../components/Dashboard';
import axiosInstance from '../api/axios';
import { mockData } from '../mock_data';
import { MemoryRouter } from 'react-router-dom';

// Mock the necessary API calls
jest.mock('../api/axios');

describe('Dashboard', () => {
	beforeEach(() => {
		jest.clearAllMocks();
	});

	test('renders upload elements', () => {
		render(
			<MemoryRouter>
				<Dashboard />
			</MemoryRouter>
		);

		expect(screen.getByRole('button', { name: /Upload Resume/i })).toBeInTheDocument();
		expect(screen.getByRole('button', { name: /Upload Job Description/i })).toBeInTheDocument();
		expect(screen.getByRole("heading", {name: /Upload Resume/i})).toBeInTheDocument();
		expect(screen.getByRole("heading", {name: /Upload Job Description/i})).toBeInTheDocument();
		expect(screen.getByTestId(/resume/i)).toBeInTheDocument();
		expect(screen.getByTestId(/description/i)).toBeInTheDocument();
	});

	test('renders Dashboard component with all elements', () => {
		render(
			<MemoryRouter>
				<Dashboard />
			</MemoryRouter>
		);

		expect(screen.getByRole('button', { name: /Sign Out/i })).toBeInTheDocument();
		expect(screen.getByText(/Resume Analysis Results/i)).toBeInTheDocument();
		expect(screen.getByText(/Resume Fit Score/i)).toBeInTheDocument();
		expect(screen.getByText(/Skills and Keywords Matched/i)).toBeInTheDocument();
		expect(screen.getByText(/Improvement Suggestions/i)).toBeInTheDocument();
	});

	test('uploads resume and job description successfully', async () => {
		// prevent data populating page after successful submit from causing error: 
		jest.spyOn(console, 'error').mockImplementation(() => {});

		axiosInstance.post.mockResolvedValueOnce({ data: { message: 'File uploaded successfully.' } });
		axiosInstance.get.mockResolvedValueOnce({
			data: mockData,
		});

		render(
			<MemoryRouter>
				<Dashboard />
			</MemoryRouter>
		);

		const resumeFile = new File(['resume content'], 'resume.pdf', { type: 'application/pdf' });
		const jobDescription = 'Job description content here.';

		// Set file for resume
		const fileInput = screen.getByTestId(/resume/i);
		fireEvent.change(fileInput, { target: { files: [resumeFile] } });

		// Set the job description
		const textarea = screen.getByTestId(/description/i);
		fireEvent.change(textarea, { target: { value: jobDescription } });

		// upload resume
		fireEvent.click(screen.getByRole('button', { name: /Upload Resume/i }));

		await waitFor(() => {
			expect(screen.getByText(/Resume uploaded successfully/i)).toBeInTheDocument();
		});

		// upload description
		fireEvent.click(screen.getByRole('button', { name: /Upload Job Description/i }));

		await waitFor(() => {
			expect(screen.getByText(/Job description uploaded successfully/i)).toBeInTheDocument();
		});
	});

	test('handles error when uploading resume or job description', async () => {
		axiosInstance.post.mockRejectedValueOnce({
			response: { data: { detail: 'Failed to upload resume.' } },
		});

		render(
			<MemoryRouter>
				<Dashboard />
			</MemoryRouter>
		);
		const resumeFile = new File(['resume content'], 'resume.pdf', { type: 'application/pdf' });
		// Set file for resume
		const fileInput = screen.getByTestId(/resume/i);
		fireEvent.change(fileInput, { target: { files: [resumeFile] } });

		fireEvent.click(screen.getByRole('button', { name: /Upload Resume/i }));

		await waitFor(() => {
			expect(screen.getByText(/Failed to upload resume./i)).toBeInTheDocument();
		});
	});
});
