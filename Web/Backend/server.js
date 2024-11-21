const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 8080;

app.use(cors());

// Utility function to execute a Python script
const runPythonScript = (scriptPath) => {
  return new Promise((resolve, reject) => {
    // Ensure the script path is wrapped in quotes if it contains spaces
    const quotedScriptPath = `"${scriptPath}"`;
    
    exec(`python3 ${quotedScriptPath}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        reject(`Error executing script: ${error.message}`);
      } else if (stderr) {
        console.error(`Script Error: ${stderr}`);
        reject(`Script error: ${stderr}`);
      } else {
        resolve(stdout.trim());
      }
    });
  });
};

// Route for crop prediction
app.get('/crop-prediction', async (req, res) => {
  try {
    // Get absolute paths for the Python scripts in the updated CS667 folder structure
    const aggregateScript = path.resolve(__dirname, './Python/aggregate.py');
    const cropPredictionScript = path.resolve(__dirname, './Python/crop_prediction.py');

    console.log('Running aggregate.py at:', aggregateScript);  // Debugging
    console.log('Running crop_prediction.py at:', cropPredictionScript);  // Debugging

    // Run aggregate.py and then crop_prediction.py
    await runPythonScript(aggregateScript);
    const output = await runPythonScript(cropPredictionScript);

    // Check for output file and return content to frontend
    const outputFilePath = path.join(__dirname, 'predicted_crop.xlsx');
    if (fs.existsSync(outputFilePath)) {
      res.download(outputFilePath); // Send the file to the frontend
    } else {
      res.status(500).send({ error: 'Output file not found.' });
    }
  } catch (error) {
    res.status(500).send({ error });
  }
});

// Route for fertilizer prediction
app.get('/fertilizer-prediction', async (req, res) => {
  try {
    // Get absolute paths for the Python scripts in the updated CS667 folder structure
    const aggregateScript = path.resolve(__dirname, './Python/aggregate.py');
    const fertilizerPredictionScript = path.resolve(__dirname, './Python/fertilizer_prediction.py');

    console.log('Running aggregate.py at:', aggregateScript);  // Debugging
    console.log('Running fertilizer_prediction.py at:', fertilizerPredictionScript);  // Debugging

    // Run aggregate.py and then fertilizer_prediction.py
    await runPythonScript(aggregateScript);
    const output = await runPythonScript(fertilizerPredictionScript);

    // Return the output directly (or save to file if needed)
    res.send({ output });
  } catch (error) {
    res.status(500).send({ error });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
