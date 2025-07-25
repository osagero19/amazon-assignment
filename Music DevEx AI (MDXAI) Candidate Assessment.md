# Music DevEx AI (MDXAI) Candidate Assessment

## Overview

This assessment evaluates your technical capabilities and alignment with MDXAI’s AI-first development philosophy. You’ll complete both a coding challenge and behavioral questions that explore your approach to automation and continuous improvement. To submit your answer and for the behavioral questions see [this link](https://app.survey.amazon.dev/M2NjOTJjMzYtODBhNC00Y2FlLWIzY2EtNjk0MmExZTY3OTAz)

-----

## Part A: Coding Assessment

### **Challenge: Claude’s Joke Factory Data Processing & Integration**

**Scenario**: Claude’s Joke Factory has compiled a database of programming jokes in JSONL format. Your challenge is to design a system that processes and enriches these jokes before integrating them into a platform or database of your choice.

**Joke Data Format**: JSONL (newline-delimited JSON) with fields: `joke_id`, `setup`, `punchline`, `source_url`

#### **Part 1: Joke Data Enrichment**

Design a data processor that ingests the joke data and applies “data decorators” to augment each joke with additional metadata. Examples include:

- **Sentiment analysis**: Determine sentiment (positive, negative, neutral) of each joke
- **Keyword extraction**: Identify key programming concepts mentioned
- **Readability scoring**: Calculate readability score (e.g., Flesch-Kincaid)
- **Joke length classification**: Categorize as short, medium, or long based on word count

**Requirement**: Implement at least one data decorators of your choice using libraries, APIs, or custom algorithms.

#### **Part 2: Joke Integration**

Choose a target platform or database for integration. Examples:

- **Collaboration platforms**: Slack, Microsoft Teams, Email, etc.
- **Productivity tools**: SIM, Jira, Taskei, etc.
- **Databases**: DynamoDB, PostgreSQL, Elasticsearch
- **Knowledge bases**: Confluence, GitLab Wiki, AMZN Wiki

Design and implement a system that integrates enriched joke data, considering:

- Data format compatibility and transformation
- API integration or data import mechanisms
- Data synchronization and update strategies
- Error handling and data validation

### **Evaluation Criteria**

Your solution will be assessed on:

1. **Correctness & Completeness**: Data enrichment pipeline functionality
2. **Design Efficiency**: Appropriateness and effectiveness of chosen data decorators
3. **Integration Soundness**: Robustness and reliability of the integration system
4. **Code Quality**: Clarity, organization, and modularity of implementation
5. **Novelty**: Creativity and originality of overall approach

### **Instructions**

- Complete both data enrichment and integration components
- Document your approach, chosen technologies, and trade-offs
- Ensure your solution can be easily run and tested by our team
- Time expectation: 1-4 hours. Do not exceed more than 1 & 1/2 coding sessions on this. 
