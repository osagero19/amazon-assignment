# Project Approach: Joke Enrichment & Integration

## Overview
This project processes and enriches a dataset of programming jokes, then integrates the enriched data into a target platform—in this case, a MongoDB database. The solution is designed to be modular, extensible, and hermetic, supporting both local and containerized (Docker) development.

---

## Approach

### 1. **Data Enrichment Pipeline**
- **Modular Design:** Implemented a pipeline with pluggable "enrichers" (decorators) for different types of metadata (sentiment, keywords, readability, length).
- **Command-Line Interface:** The script accepts arguments to select enrichment types and output destination (file or MongoDB).
- **Extensibility:** New enrichers can be added by subclassing a base class and registering in the pipeline.

### 2. **Integration with MongoDB**
- **Hermetic Setup:** Used Docker Compose to provide a reproducible, isolated MongoDB environment for all users.
- **Environment Variables:** All database credentials and connection details are managed via a `.env` file for security and portability.
- **Flexible Output:** Users can choose to save enriched data to a file or directly to MongoDB with a simple CLI flag.

### 3. **Developer Experience**
- **README Documentation:** Step-by-step instructions for setup, running, and stopping the system.
- **Error Handling:** Robust error messages for missing files, invalid JSON, or database connection issues.
- **Sample Data:** Provided a JSONL file with programming jokes for immediate testing.

---

## Chosen Technologies

- **Python 3:** Main language for scripting and data processing.
- **TextBlob:** For sentiment analysis (NLP tasks).
- **Flesch-Kincaid Readability Formula:** Used to assess the readability of each joke, providing a grade-level score that is widely recognized and easy to interpret.
- **pymongo:** For MongoDB integration.
- **python-dotenv:** For loading environment variables from `.env` files.
- **Docker & Docker Compose:** For hermetic, reproducible MongoDB setup.

---

## Tradeoffs & Rationale

### 1. **TextBlob for Sentiment Analysis**
- **Tradeoff:** TextBlob is simple and easy to use, but not as powerful as transformer-based models (e.g., BERT) for nuanced sentiment.
- **Rationale:** For joke data, high accuracy is less critical than speed and simplicity. TextBlob is lightweight and has no external dependencies.

### 2. **MongoDB as Target Database**
- **Tradeoff:** MongoDB is schema-less and easy to set up, but may not be ideal for complex relational queries.
- **Rationale:** Jokes are semi-structured and may have evolving metadata. MongoDB’s flexibility and Docker support make it a good fit for this use case.

### 3. **Docker Compose for Hermeticity**
- **Tradeoff:** Adds a dependency on Docker, but ensures everyone can run the same environment regardless of host OS.
- **Rationale:** Hermeticity is critical for reproducibility, onboarding, and CI/CD. Docker Compose is widely supported and easy to use.

### 4. **Environment Variables for Configuration**
- **Tradeoff:** Requires users to manage a `.env` file, but keeps secrets and config out of code.
- **Rationale:** This is a best practice for 12-factor apps and makes the project portable and secure.

---

## Summary
This project demonstrates a robust, extensible, and developer-friendly approach to data enrichment and integration. The use of Docker Compose, environment variables, and modular Python code ensures that anyone can run, test, and extend the system with minimal setup and maximum reproducibility. 