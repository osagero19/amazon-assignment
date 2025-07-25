#!/usr/bin/env python3
"""
Test script to demonstrate the joke enrichment system with different options.
"""

import json
from joke_enrichment import JokeEnrichmentPipeline


def create_sample_jokes():
    """Create a few sample jokes for testing."""
    return [
        {
            "joke_id": "test_001",
            "setup": "Why do programmers prefer dark mode?",
            "punchline": "Because light attracts bugs!",
            "source_url": "https://example.com",
        },
        {
            "joke_id": "test_002",
            "setup": "A programmer had a problem. He decided to use Java.",
            "punchline": "He now has a ProblemFactory.",
            "source_url": "https://example.com",
        },
        {
            "joke_id": "test_003",
            "setup": "Why don't bachelors like Git?",
            "punchline": "Because they are afraid to commit.",
            "source_url": "https://example.com",
        },
    ]


def test_enrichment_options():
    """Test different enrichment options."""
    pipeline = JokeEnrichmentPipeline()
    sample_jokes = create_sample_jokes()

    print("=== Testing Different Enrichment Options ===\n")

    # Test 1: Sentiment Analysis
    print("1. SENTIMENT ANALYSIS")
    print("-" * 50)
    enriched_sentiment = pipeline.enrich_jokes(sample_jokes, ["sentiment"])
    for joke in enriched_sentiment:
        print(f"Joke {joke['joke_id']}: {joke['setup']}")
        print(f"Sentiment: {joke['enrichment']['sentiment_analysis']['sentiment']}")
        print(f"Polarity: {joke['enrichment']['sentiment_analysis']['polarity']}")
        print()

    # Test 2: Keyword Extraction
    print("2. KEYWORD EXTRACTION")
    print("-" * 50)
    enriched_keywords = pipeline.enrich_jokes(sample_jokes, ["keywords"])
    for joke in enriched_keywords:
        print(f"Joke {joke['joke_id']}: {joke['setup']}")
        print(
            f"Top Keywords: {joke['enrichment']['keyword_extraction']['top_keywords']}"
        )
        print(
            f"Total Keywords: {joke['enrichment']['keyword_extraction']['total_keywords']}"
        )
        print()

    # Test 3: Readability Scoring
    print("3. READABILITY SCORING")
    print("-" * 50)
    enriched_readability = pipeline.enrich_jokes(sample_jokes, ["readability"])
    for joke in enriched_readability:
        print(f"Joke {joke['joke_id']}: {joke['setup']}")
        print(
            f"Grade Level: {joke['enrichment']['readability_scoring']['flesch_kincaid_grade']}"
        )
        print(
            f"Readability: {joke['enrichment']['readability_scoring']['readability_level']}"
        )
        print(f"Word Count: {joke['enrichment']['readability_scoring']['word_count']}")
        print()

    # Test 4: Length Classification
    print("4. LENGTH CLASSIFICATION")
    print("-" * 50)
    enriched_length = pipeline.enrich_jokes(sample_jokes, ["length"])
    for joke in enriched_length:
        print(f"Joke {joke['joke_id']}: {joke['setup']}")
        print(
            f"Length Category: {joke['enrichment']['length_classification']['length_category']}"
        )
        print(
            f"Word Count: {joke['enrichment']['length_classification']['word_count']}"
        )
        print()

    # Test 5: All Enrichments Combined
    print("5. ALL ENRICHMENTS COMBINED")
    print("-" * 50)
    enriched_all = pipeline.enrich_jokes(
        sample_jokes, ["sentiment", "keywords", "readability", "length"]
    )
    for joke in enriched_all:
        print(f"Joke {joke['joke_id']}: {joke['setup']}")
        print(f"Sentiment: {joke['enrichment']['sentiment_analysis']['sentiment']}")
        print(f"Keywords: {joke['enrichment']['keyword_extraction']['top_keywords']}")
        print(
            f"Readability: {joke['enrichment']['readability_scoring']['readability_level']}"
        )
        print(
            f"Length: {joke['enrichment']['length_classification']['length_category']}"
        )
        print()


if __name__ == "__main__":
    test_enrichment_options()
