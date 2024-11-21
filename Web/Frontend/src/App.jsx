import React, { useState } from 'react';

function App() {
  const [output, setOutput] = useState('');

  // Function to run the first Python script
  const runPythonScript = async () => {
    try {
      const response = await fetch('http://localhost:8080/run-python');
      const data = await response.json();
      setOutput(data.output);
    } catch (error) {
      console.error('Error running Python script:', error);
      setOutput('Error running Python script');
    }
  };

  // Function to run the second Python script
  const runAnotherPythonScript = async () => {
    try {
      const response = await fetch('http://localhost:8080/run-another-python');
      const data = await response.json();
      setOutput(data.output);
    } catch (error) {
      console.error('Error running another Python script:', error);
      setOutput('Error running another Python script');
    }
  };

  return (
    <div className="App">
      <h1>Run Python Script from Web</h1>
      <button onClick={runPythonScript}>Run First Python Script</button>
      <button onClick={runAnotherPythonScript}>Run Second Python Script</button>
      <div>
        <h2>Output:</h2>
        <pre>{output}</pre>
      </div>
    </div>
  );
}

export default App;
