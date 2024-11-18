# AdoptifAI - Multilingual Animal Description Generator

## Project Overview
This project automates the generation of engaging animal shelter descriptions using Google's Gemini AI and provides translations to Dutch using a pretrained model. Perfect for shelters serving multilingual communities!

## File Structure
```
adoptifAI/
├── content/
│   ├── chunked_generation/
│   │   ├── chunked_description_call.py       # Main processing script
│   │   ├── chunked_description_generator.py  # Batch description generation
│   │   └── description_text.py              # Text saving utilities
│   ├── normal_generation/                   # Alternative processing methods
│   ├── object_based/                       # Object-oriented implementation
│   └── tests/                              # Test files
├── data/
│   ├── animals.csv                         # Input file with animal data
│   └── animals_with_descriptions.csv       # Output file with generated descriptions
└── gemini_key.txt                         # Your Gemini API key
```

## Setup

1. **Prerequisites**
```bash
pip install google.generativeai
pip install pandas
pip install transformers  # For translation model
pip install torch  # Required for transformers
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

The main processing script is `chunked_description_call.py`:

```python
python chunked_description_call.py
```

This will:
1. Process animals in configurable batch sizes (default: 5)
2. Generate English descriptions using Gemini AI
3. Translate descriptions to Dutch
4. Save both versions to the output CSV

## How It Works

1. **Data Processing Flow**
   ```
   CSV Input → Batch Processing → English Generation → Dutch Translation → CSV Output
   ```

2. **Batch Processing**
   - Animals are processed in groups for efficiency
   - Existing descriptions are preserved
   - Failed generations are handled gracefully

3. **Translation Process**
   - Uses a pretrained model for English to Dutch translation
   - Maintains the engaging tone and key information
   - Processes translations in batches for efficiency

## Configuration Options

In `chunked_description_call.py`:
```python
batch_size = 5       # Number of animals per batch
start_row = None     # Optional: Start from specific row
end_row = None       # Optional: End at specific row
```

## Error Handling

The system includes:
- Automatic retries for failed API calls
- Error logging in the `logs/` directory
- Preservation of successful generations
- Batch-level error recovery

## Generated Descriptions

Example output:
```
English:
"Bella is a playful and affectionate 3-year-old black beauty who is looking 
for her forever home. She's been with us for a while now, but her sweet 
disposition and boundless energy make her a joy to have around..."

Dutch:
"Bella is een speelse en liefdevolle 3-jarige zwarte schoonheid die op zoek 
is naar haar forever home. Ze is al een tijdje bij ons, maar haar lieve karakter 
en grenzeloze energie maken haar een vreugde om in de buurt te hebben..."
```

## Tips for Best Results

1. Keep batch sizes reasonable (5-10 animals)
2. Verify your API key and model access
3. Monitor translation quality
4. Check the logs for any issues
5. Consider memory usage when processing large batches

## Future Improvements

- Enhanced translation quality checks
- More customization options for descriptions
- API endpoint for real-time generation

## Need Help?

- Check the logs in the `logs/` directory
- Ensure all dependencies are correctly installed
- Verify your API key permissions
- Monitor system resources during large batch processing

## Contributing

Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Request additional language support
