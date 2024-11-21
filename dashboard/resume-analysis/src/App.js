import React from "react";
import Dashboard from "./dashboard";
import { mockData } from "./mock-data";

const App = () => {
  return (
    <div>
      <Dashboard
        fitScore={mockData.fitScore}
        skillsMatched={mockData.skillsMatched}
        improvementSuggestions={mockData.improvementSuggestions}
      />
    </div>
  );
};

export default App;
