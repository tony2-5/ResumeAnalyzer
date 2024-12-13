const { defineConfig } = require('cypress')
const pdf = require('pdf-parse');
const fs = require('fs');

module.exports = defineConfig({
    e2e: {
        setupNodeEvents(on, config) {
            on('task', {
                // Define the task for reading and parsing the PDF
                readPdf: (filePath) => {
                    return new Promise((resolve, reject) => {
                    const dataBuffer = fs.readFileSync(filePath);
                    pdf(dataBuffer)
                    .then((data) => {
                        resolve(data.text);  // Resolve with the text content of the PDF
                    })
                    .catch((err) => {
                        reject(err);  // Reject if an error occurs
                    });
                });
                },
            });
        }
    },
})