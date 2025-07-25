# Joke Data Enrichment System

A modular system for enriching programming jokes with various metadata decorators. This system processes JSONL joke data and applies different enrichment options to add valuable metadata.

## Features

The system supports four types of enrichment:

1. **Sentiment Analysis** (`sentiment`): Analyzes the emotional tone of jokes using TextBlob
2. **Keyword Extraction** (`keywords`): Identifies programming-related terms and concepts
3. **Readability Scoring** (`readability`): Calculates Flesch-Kincaid grade level and readability metrics
4. **Length Classification** (`length`): Categorizes jokes as short, medium, or long based on word count

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Hermetic MongoDB Setup with Docker Compose

This project supports a fully hermetic (self-contained) MongoDB setup using Docker Compose. This ensures anyone can run the enrichment pipeline and database locally with no manual database setup.

### 1. Start MongoDB with Docker Compose

```bash
docker compose up -d
```
This will start a MongoDB server on `localhost:27017` with persistent storage in a Docker volume.

### 2. Configure Environment Variables

Create a `.env` file in the project root with the following content:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=jokesdb
MONGO_COLLECTION=jokes
```

### 3. Run the Enrichment Script

#### Save to MongoDB (recommended for hermetic setup)
```bash
python joke_enrichment.py ProgrammingJokes.jsonl --output-mode mongo
```

#### Save to File (default)
```bash
python joke_enrichment.py ProgrammingJokes.jsonl --output-mode file --output enriched_jokes.jsonl
```

### 4. Stopping MongoDB
To stop the MongoDB container:
```bash
docker compose down
```

### Viewing Data in MongoDB
If you want to visually explore or query the enriched joke data in MongoDB, download and install [MongoDB Compass](https://www.mongodb.com/try/download/compass). MongoDB Compass is a free, official GUI tool for connecting to your local MongoDB instance, browsing collections, and running queries interactively.

## Usage

### Basic Usage (Sentiment Analysis)

```bash
python joke_enrichment.py ProgrammingJokes.jsonl
```

This will apply sentiment analysis to all jokes and save the results to `enriched_jokes.jsonl`.

### Multiple Enrichment Types

```bash
python joke_enrichment.py ProgrammingJokes.jsonl --enrichment sentiment keywords readability
```

### All Enrichment Types

```bash
python joke_enrichment.py ProgrammingJokes.jsonl --enrichment sentiment keywords readability length
```

### Custom Output File

```bash
python joke_enrichment.py ProgrammingJokes.jsonl --output my_enriched_jokes.jsonl
```

### With Summary

```bash
python joke_enrichment.py ProgrammingJokes.jsonl --summary
```

## Command Line Options

- `input_file`: Path to the JSONL file containing jokes (required)
- `--enrichment, -e`: Enrichment types to apply (choices: sentiment, keywords, readability, length)
- `--output, -o`: Output file path (default: enriched_jokes.jsonl)
- `--output-mode`: Output destination, either `file` or `mongo` (default: file)
- `--summary, -s`: Print a summary of enrichment results

## Input Format

The system expects JSONL format with each line containing a JSON object with these fields:
- `joke_id`: Unique identifier for the joke
- `setup`: The setup part of the joke
- `punchline`: The punchline of the joke
- `source_url`: Source URL for the joke

Example:
```json
{"joke_id": "001", "setup": "Why do programmers always mix up Halloween and Christmas?", "punchline": "Because Oct 31 == Dec 25!", "source_url": "https://example.com"}
```

## Output Format

The enriched jokes will have an additional `enrichment` field containing the metadata from each applied enrichment type.

### Sentiment Analysis Output
```json
{
  "enrichment": {
    "sentiment_analysis": {
      "sentiment": "positive",
      "polarity": 0.2,
      "subjectivity": 0.1,
      "setup_polarity": 0.0,
      "punchline_polarity": 0.3
    }
  }
}
```

### Keyword Extraction Output
```json
{
  "enrichment": {
    "keyword_extraction": {
      "keywords_by_category": {
        "languages": ["java", "python"],
        "concepts": ["function", "variable"],
        "tools": ["git"]
      },
      "top_keywords": ["java", "function", "python"],
      "total_keywords": 4,
      "keyword_density": 0.15
    }
  }
}
```

### Readability Scoring Output
```json
{
  "enrichment": {
    "readability_scoring": {
      "flesch_kincaid_grade": 8.5,
      "word_count": 12,
      "sentence_count": 2,
      "average_word_length": 4.2,
      "readability_level": "moderate"
    }
  }
}
```

### Length Classification Output
```json
{
  "enrichment": {
    "length_classification": {
      "word_count": 12,
      "character_count": 85,
      "length_category": "short",
      "setup_word_count": 8,
      "punchline_word_count": 4
    }
  }
}
```

## Architecture

The system uses a modular design with:

- **JokeEnricher**: Base class for all enrichment decorators
- **JokeEnrichmentPipeline**: Main pipeline that orchestrates the enrichment process
- **Individual Enrichers**: Specialized classes for each enrichment type

This design makes it easy to add new enrichment types by extending the `JokeEnricher` base class.
