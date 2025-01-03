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
        expect(screen.getByRole('button', { name: /Download PDF Report/i })).toBeInTheDocument();
	});

    test('renders Improvement Suggestions section correctly', async () => {
        render(
        <MemoryRouter>
          <Dashboard />
        </MemoryRouter>
        );

        // Wait for the dashboard to load the data
        await waitFor(() => screen.getByText('Resume Analysis Results'));

        // Check if the "Improvement Suggestions" heading is rendered
        expect(screen.getByText('Improvement Suggestions')).toBeInTheDocument();

        // Check if the select dropdown is rendered with the options
        const selectElement = screen.getByRole('combobox');
        expect(selectElement).toBeInTheDocument();
        expect(screen.getByRole('option', { name: 'All' })).toBeInTheDocument();
        expect(screen.getByRole('option', { name: 'Skills' })).toBeInTheDocument();
        expect(screen.getByRole('option', { name: 'Experience' })).toBeInTheDocument();
        expect(screen.getByRole('option', { name: 'Education' })).toBeInTheDocument();
        expect(screen.getByRole('option', { name: 'Achievements' })).toBeInTheDocument();
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

	test('handles error when uploading resume', async () => {
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

    test('handles error when uploading job description', async () => {
        axiosInstance.post.mockRejectedValueOnce({
            response: { data: { detail: 'Failed to upload job description.' } },
        });
    
        render(
            <MemoryRouter>
                <Dashboard />
            </MemoryRouter>
        );
    
        // Simulate entering a job description in the textarea
        const mockDescription = 'Sample job description content';
        const descriptionTextarea = screen.getByTestId(/description/i);
        fireEvent.change(descriptionTextarea, { target: { value: mockDescription } });
    
        // Trigger the upload for the job description
        fireEvent.click(screen.getByRole('button', { name: /Upload Job Description/i }));
    
        // Wait for the error message to be displayed
        await waitFor(() => {
            expect(screen.getByText(/Failed to upload job description./i)).toBeInTheDocument();
        });
    });

	test('handles error when uploading a file larger than 2MB', async () => {
    	// Create a file that exceeds 2MB in size
		const largeFileContent = new Array(2097152).join('A');
		const largeFile = new File([largeFileContent], 'largeResume.pdf', { type: 'application/pdf' });

		axiosInstance.post.mockRejectedValueOnce({
			response: { data: { detail: 'File size exceeds 2MB limit.' } },
		});

		render(
			<MemoryRouter>
				<Dashboard />
			</MemoryRouter>
		);

		// Set file for resume
		const fileInput = screen.getByTestId(/resume/i);
		fireEvent.change(fileInput, { target: { files: [largeFile] } });

		fireEvent.click(screen.getByRole('button', { name: /Upload Resume/i }));

		await waitFor(() => {
			expect(screen.getByText(/File size exceeds 2MB limit./i)).toBeInTheDocument();
		});
 	 });

    test('handles error when fetching resume data', async () => {
        // Mock axiosInstance.post to reject with an error
        jest.spyOn(axiosInstance, 'post').mockRejectedValueOnce({
            response: { data: { detail: 'Failed to fetch resume data.' } },
        });
    
        render(
            <MemoryRouter>
                <Dashboard />
            </MemoryRouter>
        );
    
        // Simulate setting valid resume and job description
        const mockResume = new File(['Sample resume content'], 'resume.pdf', { type: 'application/pdf' });
        const mockDescription = 'Sample job description content';
    
        // Set the file for resume upload
        const resumeInput = screen.getByTestId(/resume/i);
        fireEvent.change(resumeInput, { target: { files: [mockResume] } });
    
        // Set the job description
        const descriptionTextarea = screen.getByTestId(/description/i);
        fireEvent.change(descriptionTextarea, { target: { value: mockDescription } });
    
        // Trigger the upload for both resume and job description
        fireEvent.click(screen.getByRole('button', { name: /Upload Resume/i }));
    
        // Wait for the error message to be displayed
        await waitFor(() => {
            expect(screen.getByText(/Failed to fetch resume data./i)).toBeInTheDocument();
        });
    });

	test('handles error when uploading a job description longer than 10000 characters', async () => {
		const longJobDescription = 'A'.repeat(10001);

		axiosInstance.post.mockRejectedValueOnce({
			response: { data: { detail: 'Job description must be less than 10000 characters.' } },
		});

		render(
			<MemoryRouter>
				<Dashboard />
			</MemoryRouter>
		);

		const textarea = screen.getByTestId(/description/i);
		fireEvent.change(textarea, { target: { value: longJobDescription } });

		fireEvent.click(screen.getByRole('button', { name: /Upload Job Description/i }));

		await waitFor(() => {
			expect(screen.getByText(/Job description exceeds the maximum length of 10,000 characters./i)).toBeInTheDocument();
		});
	});
});
