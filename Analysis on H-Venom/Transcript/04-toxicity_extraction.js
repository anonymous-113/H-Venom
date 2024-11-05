const { google } = require("googleapis");

const API_KEY = "";
const DISCOVERY_URL =
  "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1";

const fs = require("fs").promises;
const transcript_path = "";

async function analyzeToxicity(text) {
  try {
    const client = await google.discoverAPI(DISCOVERY_URL);
    const analyzeRequest = {
      comment: {
        text,
      },
      requestedAttributes: {
        TOXICITY: {},
      },
    };

    const response = await client.comments.analyze({
      key: API_KEY,
      resource: analyzeRequest,
    });

    return response.data.attributeScores.TOXICITY;
  } catch (err) {
    throw new Error(`Error analyzing toxicity: ${err.message}`);
  }
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function readAndExtract() {
  try {
    // Read the JSON file
    const data = await fs.readFile(transcript_path, "utf8");

    // Parse the JSON data
    const jsonData = JSON.parse(data);
    const extractedData = jsonData.map((item) => ({
      video_name: item.video_name,
      transcription: item.transcription,
    }));

    const results = [];
    const errors = [];

    for (const item of extractedData) {
      try {
        const toxicity = await analyzeToxicity(item.transcription);
        const result = {
          video_name: item.video_name,
          span_toxicity: toxicity.spanScores[0]?.score.value || 0,
          summaryScore_toxicity: toxicity.summaryScore.value || 0,
        };

        results.push(result);
        console.log("Toxicity Analysis Result:", result);
      } catch (err) {
        errors.push({
          video_name: item.video_name,
          error: err.message,
        });
        console.error("Error processing item:", item.video_name, err);
      }

      // Wait 1 second between requests (1000 milliseconds)
      await delay(1000);
    }

    // Write results to a file
    await fs.writeFile(
      "./results_non_hate.json",
      JSON.stringify(results, null, 2)
    );
    console.log("Results saved to toxicity_non_hate.json");

    // Write errors to a file if any
    if (errors.length > 0) {
      await fs.writeFile(
        "./non_hate_errors.json",
        JSON.stringify(errors, null, 2)
      );
      console.log("Errors saved to toxicity_errors.json");
    }
  } catch (err) {
    console.error("Error:", err);
  }
}

readAndExtract();
