# AdoptifAI - Animal Description Generator

## Project Overview
This project automates the generation of engaging animal shelter descriptions using Google's Gemini AI. Let me walk you through it!

## File Structure
```
adoptifAI/
├── data/
│   ├── animals.csv                    # Input file with animal data
│   └── animals_with_descriptions.csv  # Output file with generated descriptions
├── generating_content/
│   ├── description_generator.py       # Core AI description generation logic
│   ├── description_call.py           # Single animal processing
│   └── chunked_description_call.py   # Batch processing for multiple animals
└── gemini_key.txt                    # Your Gemini API key
```

## Setup

1. **Prerequisites**
```bash
pip install google.generativeai
pip install pandas
pip install tenacity  # For retry logic
```

2. **API Key Setup**
- Get a Gemini API key from Google
- Either:
  - Set it as environment variable: `GEMINI_API_KEY`
  - Or place it in `gemini_key.txt` in the root directory

## Input Data Format

Your `animals.csv` should have these columns:
```
animal_type,name,age,color,months_in_shelter,behavior,health,vaccinated,target_audience
```

Example:
```csv
dog,Bella,3,black,12,"friendly, energetic",excellent,True,families
```

## Running the Generator


### Option 1: Single Animal Processing
```python
python description_call.py
```

### Option 2: Batch Processing (Recommended!)
```python
python chunked_description_call.py
```

The batch processor:
- Processes animals in groups of 5 (configurable)
- More efficient API usage
- Better error handling
- Preserves existing descriptions

## How It Works


1. **Data Loading**
   ```
   CSV File → Load Animals → Check Existing Descriptions
   ```

2. **Batch Processing**
   ```
   Group Animals → Generate Descriptions → Save Results
   [5 animals] → [AI Generation] → [CSV Update]
   ```

3. **Description Generation**
   ```
   Animal Data → AI Prompt → Generated Description
   ```

## Configuration Options


In `chunked_description_call.py`:
```python
batch_size = 5  # Number of animals per batch
start_row = None  # Optional: Start from specific row
end_row = None   # Optional: End at specific row
```

## Error Handling


The system:
- Retries failed API calls
- Logs errors in `logs/` directory
- Continues processing even if some descriptions fail
- Preserves successfully generated descriptions

## Generated Descriptions

Example output:
```
"Bella is a playful and affectionate 3-year-old black beauty who is looking 
for her forever home. She's been with us for a while now, but her sweet 
disposition and boundless energy make her a joy to have around..."
```

## Tips for Best Results


1. Keep batch sizes reasonable (5-10 animals)
2. Verify your API key is working
3. Check the logs if something goes wrong

## Future Improvements

- Improve error recovery
- Add image generation
- Enhanced description customization

## Need Help?


Check the logs in the `logs/` directory for detailed error messages and processing information.
