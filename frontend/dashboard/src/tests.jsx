import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./authContext";

test("redirects to /login if not authenticated", () => {
  render(
    <AuthProvider>
      <MemoryRouter initialEntries={["/dashboard"]}>
        <App />
      </MemoryRouter>
    </AuthProvider>
  );

  expect(screen.getByText(/login page/i)).toBeInTheDocument();
});

test("allows access to /dashboard if authenticated", () => {
  render(
    <AuthProvider>
      <MemoryRouter initialEntries={["/dashboard"]}>
        <App />
      </MemoryRouter>
    </AuthProvider>
  );

  // Mock authentication
  const authContext = require("./authContext");
  authContext.useAuth = () => ({ isAuthenticated: true });

  expect(screen.getByText(/welcome to the dashboard/i)).toBeInTheDocument();
});
