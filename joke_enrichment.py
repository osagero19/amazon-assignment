#!/usr/bin/env python3
"""
Joke Data Enrichment System
A modular system for enriching programming jokes with various metadata decorators.
"""

import json
import argparse
import sys
from typing import Dict, List, Any, Callable
from textblob import TextBlob
import re
from collections import Counter
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class JokeEnricher:
    """Base class for joke enrichment decorators."""

    def __init__(self):
        self.name = "base_enricher"

    def enrich(self, joke: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a joke with additional metadata."""
        raise NotImplementedError("Subclasses must implement enrich method")


class SentimentAnalyzer(JokeEnricher):
    """Enriches jokes with sentiment analysis using TextBlob."""

    def __init__(self):
        self.name = "sentiment_analysis"

    def enrich(self, joke: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment of both setup and punchline."""
        setup = joke.get("setup", "")
        punchline = joke.get("punchline", "")

        # Combine setup and punchline for overall sentiment
        full_text = f"{setup} {punchline}"

        # Analyze sentiment using TextBlob
        blob = TextBlob(full_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Categorize sentiment
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Add enrichment data
        joke["enrichment"] = joke.get("enrichment", {})
        joke["enrichment"][self.name] = {
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "setup_polarity": round(TextBlob(setup).sentiment.polarity, 3),
            "punchline_polarity": round(TextBlob(punchline).sentiment.polarity, 3),
        }

        return joke


class KeywordExtractor(JokeEnricher):
    """Extracts programming-related keywords from jokes."""

    def __init__(self):
        self.name = "keyword_extraction"
        # Common programming terms and concepts
        self.programming_keywords = {
            "languages": [
                "python",
                "java",
                "javascript",
                "c++",
                "c#",
                "php",
                "ruby",
                "go",
                "rust",
                "swift",
                "kotlin",
                "scala",
                "perl",
                "cobol",
                "assembly",
                "html",
                "css",
                "sql",
                "xml",
                "json",
            ],
            "concepts": [
                "function",
                "variable",
                "loop",
                "array",
                "object",
                "class",
                "method",
                "inheritance",
                "polymorphism",
                "encapsulation",
                "abstraction",
                "recursion",
                "algorithm",
                "data structure",
                "database",
                "api",
                "framework",
                "library",
                "compiler",
                "interpreter",
                "debug",
                "bug",
                "code",
                "program",
                "software",
                "hardware",
                "network",
                "server",
                "client",
                "frontend",
                "backend",
                "fullstack",
                "devops",
                "git",
                "version control",
                "testing",
                "deployment",
                "microservices",
                "docker",
                "kubernetes",
                "cloud",
                "aws",
                "azure",
                "gcp",
            ],
            "tools": [
                "ide",
                "editor",
                "vscode",
                "vim",
                "emacs",
                "eclipse",
                "intellij",
                "github",
                "gitlab",
                "bitbucket",
                "jira",
                "confluence",
                "slack",
                "teams",
                "docker",
                "kubernetes",
                "jenkins",
                "travis",
                "circleci",
                "npm",
                "pip",
                "maven",
                "gradle",
                "webpack",
                "babel",
                "eslint",
                "prettier",
            ],
        }

    def enrich(self, joke: Dict[str, Any]) -> Dict[str, Any]:
        """Extract programming keywords from the joke."""
        setup = joke.get("setup", "").lower()
        punchline = joke.get("punchline", "").lower()
        full_text = f"{setup} {punchline}"

        found_keywords = {"languages": [], "concepts": [], "tools": []}

        # Find keywords in each category
        for category, keywords in self.programming_keywords.items():
            for keyword in keywords:
                if keyword in full_text:
                    found_keywords[category].append(keyword)

        # Get top keywords by frequency
        all_keywords = []
        for category_keywords in found_keywords.values():
            all_keywords.extend(category_keywords)

        keyword_freq = Counter(all_keywords)
        top_keywords = [kw for kw, freq in keyword_freq.most_common(5)]

        joke["enrichment"] = joke.get("enrichment", {})
        joke["enrichment"][self.name] = {
            "keywords_by_category": found_keywords,
            "top_keywords": top_keywords,
            "total_keywords": len(all_keywords),
            "keyword_density": (
                round(len(all_keywords) / len(full_text.split()), 3)
                if full_text.split()
                else 0
            ),
        }

        return joke


class ReadabilityScorer(JokeEnricher):
    """Calculates readability scores for jokes."""

    def __init__(self):
        self.name = "readability_scoring"

    def count_syllables(self, word: str) -> int:
        """Simple syllable counting algorithm."""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel

        # Adjust for words ending in 'e'
        if word.endswith("e"):
            count -= 1

        return max(count, 1)

    def calculate_flesch_kincaid(self, text: str) -> float:
        """Calculate Flesch-Kincaid Grade Level."""
        sentences = len(re.split(r"[.!?]+", text))
        words = len(text.split())
        syllables = sum(self.count_syllables(word) for word in text.split())

        if sentences == 0 or words == 0:
            return 0

        # Flesch-Kincaid Grade Level formula
        grade_level = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        return round(grade_level, 2)

    def enrich(self, joke: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate readability scores for the joke."""
        setup = joke.get("setup", "")
        punchline = joke.get("punchline", "")
        full_text = f"{setup} {punchline}"

        # Calculate various readability metrics
        flesch_kincaid = self.calculate_flesch_kincaid(full_text)

        # Word count analysis
        words = full_text.split()
        word_count = len(words)
        avg_word_length = (
            round(sum(len(word) for word in words) / word_count, 2)
            if word_count > 0
            else 0
        )

        # Sentence count
        sentences = len(re.split(r"[.!?]+", full_text))

        joke["enrichment"] = joke.get("enrichment", {})
        joke["enrichment"][self.name] = {
            "flesch_kincaid_grade": flesch_kincaid,
            "word_count": word_count,
            "sentence_count": sentences,
            "average_word_length": avg_word_length,
            "readability_level": self._categorize_readability(flesch_kincaid),
        }

        return joke

    def _categorize_readability(self, grade_level: float) -> str:
        """Categorize readability based on grade level."""
        if grade_level <= 6:
            return "easy"
        elif grade_level <= 10:
            return "moderate"
        else:
            return "difficult"


class JokeLengthClassifier(JokeEnricher):
    """Classifies jokes by length based on word count."""

    def __init__(self):
        self.name = "length_classification"
        self.length_thresholds = {"short": 15, "medium": 30}

    def enrich(self, joke: Dict[str, Any]) -> Dict[str, Any]:
        """Classify joke length based on word count."""
        setup = joke.get("setup", "")
        punchline = joke.get("punchline", "")
        full_text = f"{setup} {punchline}"

        word_count = len(full_text.split())
        char_count = len(full_text)

        # Classify length
        if word_count <= self.length_thresholds["short"]:
            length_category = "short"
        elif word_count <= self.length_thresholds["medium"]:
            length_category = "medium"
        else:
            length_category = "long"

        joke["enrichment"] = joke.get("enrichment", {})
        joke["enrichment"][self.name] = {
            "word_count": word_count,
            "character_count": char_count,
            "length_category": length_category,
            "setup_word_count": len(setup.split()),
            "punchline_word_count": len(punchline.split()),
        }

        return joke


class JokeEnrichmentPipeline:
    """Main pipeline for processing and enriching jokes."""

    def __init__(self):
        self.enrichers = {
            "sentiment": SentimentAnalyzer(),
            "keywords": KeywordExtractor(),
            "readability": ReadabilityScorer(),
            "length": JokeLengthClassifier(),
        }

    def load_jokes(self, file_path: str) -> List[Dict[str, Any]]:
        """Load jokes from JSONL file."""
        jokes = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        jokes.append(json.loads(line))
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file: {e}")
            sys.exit(1)

        return jokes

    def enrich_jokes(
        self, jokes: List[Dict[str, Any]], enrichment_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Apply specified enrichment types to jokes."""
        enriched_jokes = []

        for joke in jokes:
            enriched_joke = joke.copy()

            for enrichment_type in enrichment_types:
                if enrichment_type in self.enrichers:
                    enriched_joke = self.enrichers[enrichment_type].enrich(
                        enriched_joke
                    )
                else:
                    print(f"Warning: Unknown enrichment type '{enrichment_type}'")

            enriched_jokes.append(enriched_joke)

        return enriched_jokes

    def save_enriched_jokes(
        self, jokes: List[Dict[str, Any]], output_file: str, output_mode: str = "file"
    ):
        """Save enriched jokes to JSONL file or MongoDB."""
        if output_mode == "file":
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    for joke in jokes:
                        file.write(json.dumps(joke, ensure_ascii=False) + "\n")
                print(f"Enriched jokes saved to '{output_file}'")
            except Exception as e:
                print(f"Error saving file: {e}")
                sys.exit(1)
        elif output_mode == "mongo":
            mongo_uri = os.getenv("MONGO_URI")
            mongo_db = os.getenv("MONGO_DB")
            mongo_collection = os.getenv("MONGO_COLLECTION")
            if not (mongo_uri and mongo_db and mongo_collection):
                print("MongoDB credentials are not set in the environment variables.")
                sys.exit(1)
            try:
                client = MongoClient(mongo_uri)
                db = client[mongo_db]
                collection = db[mongo_collection]
                # Insert many, overwrite if joke_id exists
                for joke in jokes:
                    collection.update_one(
                        {"joke_id": joke["joke_id"]}, {"$set": joke}, upsert=True
                    )
                print(f"Enriched jokes saved to MongoDB: {mongo_db}.{mongo_collection}")
            except Exception as e:
                print(f"Error saving to MongoDB: {e}")
                sys.exit(1)
        else:
            print(f"Unknown output mode: {output_mode}")
            sys.exit(1)

    def print_summary(self, jokes: List[Dict[str, Any]], enrichment_types: List[str]):
        """Print a summary of the enrichment results."""
        print(f"\n=== Enrichment Summary ===")
        print(f"Total jokes processed: {len(jokes)}")
        print(f"Enrichment types applied: {', '.join(enrichment_types)}")

        # Show sample enriched joke
        if jokes:
            print(f"\n=== Sample Enriched Joke ===")
            sample_joke = jokes[0]
            print(f"Joke ID: {sample_joke.get('joke_id')}")
            print(f"Setup: {sample_joke.get('setup')}")
            print(f"Punchline: {sample_joke.get('punchline')}")

            if "enrichment" in sample_joke:
                print(f"Enrichment data:")
                for enrichment_type, data in sample_joke["enrichment"].items():
                    print(f"  {enrichment_type}: {data}")


def main():
    """Main function to run the joke enrichment pipeline."""
    parser = argparse.ArgumentParser(
        description="Enrich programming jokes with various metadata"
    )
    parser.add_argument("input_file", help="Input JSONL file containing jokes")
    parser.add_argument(
        "--enrichment",
        "-e",
        nargs="+",
        choices=["sentiment", "keywords", "readability", "length"],
        default=["sentiment"],
        help="Enrichment types to apply (default: sentiment)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="enriched_jokes.jsonl",
        help="Output file for enriched jokes (default: enriched_jokes.jsonl)",
    )
    parser.add_argument(
        "--output-mode",
        choices=["file", "mongo"],
        default="file",
        help="Output mode: file or mongo (default: file)",
    )
    parser.add_argument(
        "--summary",
        "-s",
        action="store_true",
        help="Print summary of enrichment results",
    )

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = JokeEnrichmentPipeline()

    # Load jokes
    print(f"Loading jokes from '{args.input_file}'...")
    jokes = pipeline.load_jokes(args.input_file)
    print(f"Loaded {len(jokes)} jokes")

    # Enrich jokes
    print(f"Applying enrichment: {', '.join(args.enrichment)}...")
    enriched_jokes = pipeline.enrich_jokes(jokes, args.enrichment)

    # Save enriched jokes
    pipeline.save_enriched_jokes(enriched_jokes, args.output, args.output_mode)

    # Print summary if requested
    if args.summary:
        pipeline.print_summary(enriched_jokes, args.enrichment)


if __name__ == "__main__":
    main()
