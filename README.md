# Insurance Policy RAG

A Retrieval-Augmented Generation (RAG) system for querying health insurance policies and generating **evidence-backed answers** from policy documents.

The project is designed as the foundation for an AI-assisted insurance claim assessment system, where unstructured documents such as insurance policies, discharge summaries, and hospital bills can be processed to determine applicable coverage and estimate claim eligibility.

---

## Overview

Health insurance policies are often lengthy, complex documents containing:

* Coverage conditions
* Waiting periods
* Exclusions
* Benefit limits
* Sub-limits
* Definitions
* Claim procedures
* Policy-specific terms and conditions

Finding the relevant information manually can be time-consuming.

This project uses **RAG** to retrieve the most relevant sections of an insurance policy and provide them as context to an LLM. The LLM then generates an answer grounded in the retrieved policy content instead of relying solely on its internal knowledge.

The system also preserves **section and page metadata**, allowing answers to be traced back to the original policy document.

---

## Current Capabilities

The current implementation supports:

* PDF policy document ingestion
* PDF text extraction using PyMuPDF
* Hierarchical policy structure detection
* Recursive document chunking
* Section and page metadata preservation
* Vector embedding generation
* PostgreSQL + pgvector storage
* Semantic similarity search
* RAG context generation
* LLM-based policy question answering
* Evidence-backed responses with policy section and page references

The current dataset uses the **Royal Sundaram Family Plus** health insurance policy as an example policy document.

---

## Architecture

```text
                    ┌──────────────────────┐
                    │   Insurance Policy   │
                    │        PDF           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    PDF Extraction    │
                    │       PyMuPDF        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Structuring │
                    │ Sections / Headings  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Chunking        │
                    │ Section-aware chunks │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Embeddings       │
                    │ BGE-small-en-v1.5    │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       PostgreSQL + pgvector    │
              │                                │
              │ Policy chunks + metadata +     │
              │ vector embeddings              │
              └───────────────┬────────────────┘
                              │
                     User Question
                              │
                              ▼
                    ┌──────────────────────┐
                    │ Query Embedding      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Vector Similarity    │
                    │ Search               │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relevant Policy      │
                    │ Context              │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Groq LLM             │
                    │ GPT-OSS 120B         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Evidence-backed      │
                    │ Answer               │
                    └──────────────────────┘
```

---

## Tech Stack

### Backend / Processing

* Python
* PyMuPDF
* Sentence Transformers
* Pydantic *(planned for structured document extraction)*

### Embeddings

**BAAI/bge-small-en-v1.5**

* 384-dimensional embeddings
* Used for both document chunks and user queries
* Embeddings are normalized before storage and retrieval

### Vector Database

**PostgreSQL + pgvector**

Stores:

* Policy document ID
* Chunk text
* Section title
* Section hierarchy/path
* Page range
* Vector embedding

### LLM

**Groq**

Current model:

```text
openai/gpt-oss-120b
```

The LLM receives the retrieved policy context and generates an answer based only on that context.

### Infrastructure

**Docker Compose**

PostgreSQL + pgvector runs inside Docker for local development.

---

## Project Structure

```text
insurance-policy-rag/
│
├── data/
│   └── policies/
│       └── family_plus.pdf
│
├── ingestion/
│   ├── __init__.py
│   ├── extract.py
│   ├── document.py
│   ├── structure.py
│   ├── chunk.py
│   └── ingest.py
│
├── embeddings/
│   ├── __init__.py
│   └── embed.py
│
├── db/
│   ├── __init__.py
│   └── setup.py
│
├── tests/
│   ├── __init__.py
│   ├── test_structure.py
│   ├── test_chunk.py
│   ├── test_pages.py
│   ├── test_embedding.py
│   ├── test_db_insert.py
│   ├── test_retrieval.py
│   └── ...
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Document Ingestion Pipeline

The ingestion pipeline converts an insurance policy PDF into searchable vector representations.

### 1. Extract PDF text

Policy pages are extracted using PyMuPDF while preserving page numbers.

```text
PDF
 ↓
Page 1 → text
Page 2 → text
...
Page 59 → text
```

### 2. Build document structure

The extracted text is converted into a hierarchical document representation.

For example:

```text
Section 3 — Benefits
    3.10 — AYUSH
    3.11 — Animal Bite
    3.12 — Health Check-up
    3.16 — Maternity Benefits
```

This structure allows chunks to retain information about where they came from.

### 3. Create chunks

Large sections are recursively split into smaller chunks while preserving:

* Section title
* Section hierarchy
* Page range
* Chunk text

The current policy produces approximately **594 searchable chunks**.

### 4. Generate embeddings

Each chunk is converted into a 384-dimensional vector using:

```text
BAAI/bge-small-en-v1.5
```

Section path information is included when generating the embedding so that semantic retrieval also has structural context.

### 5. Store vectors

The resulting chunks and embeddings are stored in PostgreSQL using pgvector.

---

## Retrieval

When a user asks a question such as:

> Is maternity treatment covered?

the question is converted into an embedding.

PostgreSQL then performs vector similarity search:

```text
User Question
      ↓
Query Embedding
      ↓
pgvector similarity search
      ↓
Top relevant policy chunks
      ↓
RAG Context
```

For example, a query about maternity benefits can retrieve sections containing:

```text
Section 3 → 3.16 Maternity Benefits
Section 2 → Maternity Expenses definition
```

along with their corresponding page numbers.

---

## RAG Answer Generation

The retrieved policy chunks are passed to the LLM as context.

The model is instructed to:

1. Answer using only the supplied policy context.
2. Avoid inventing policy rules or values.
3. State when the retrieved information is insufficient.
4. Reference the relevant policy section and page whenever possible.

Example:

```text
Question:
Is maternity treatment covered?

Retrieved evidence:
Section 3 → 3.16 Maternity Benefits
Page 19

...

LLM:
Maternity treatment is covered under the Maternity Benefits section,
subject to the applicable conditions and a 24-month waiting period.
```

The goal is not simply to generate a plausible answer, but to make the answer **traceable to the source policy**.

---

# Future: AI-Assisted Claim Assessment

The current RAG system is the foundation for a larger insurance claim assessment workflow.

The planned system will accept:

```text
Hospital Discharge Summary
            +
Hospital Bill
            +
Insurance Policy
```

and process them through the following pipeline:

```text
             ┌─────────────────────┐
             │ Discharge Summary   │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Structured          │
             │ Information         │
             │ Extraction          │
             └──────────┬──────────┘
                        │
                        │
             ┌─────────────────────┐
             │ Hospital Bill       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Bill Item Extraction│
             └──────────┬──────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ RAG Retrieval    │
               │ Policy Clauses   │
               └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ Rules Engine     │
               │                  │
               │ Coverage         │
               │ Limits           │
               │ Exclusions       │
               │ Waiting Periods  │
               └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ Estimated        │
               │ Claim Amount     │
               └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ LLM Explanation  │
               │ + Evidence       │
               └──────────────────┘
```

### Why use a rules engine?

The LLM should **not** be responsible for performing the final financial calculation.

Instead:

* **LLM** → extracts information and explains results
* **RAG** → retrieves policy-specific evidence
* **Rules engine** → applies deterministic coverage rules and calculations

For example:

```text
Policy:
Maternity benefit = ₹50,000
Waiting period = 24 months

Claim:
Eligible maternity treatment
Hospital bill = ₹72,000

Rules Engine:
Applicable limit = ₹50,000
Estimated payable amount = ₹50,000
```

This separation makes the system more predictable, testable, and auditable.

---

## Planned Features

### Document Understanding

* [ ] Extract structured data from discharge summaries
* [ ] Extract hospital bill line items
* [ ] Support scanned PDFs using OCR
* [ ] Validate extracted information using Pydantic

### Policy Intelligence

* [ ] Improve policy structure detection
* [ ] Improve chunking and retrieval
* [ ] Hybrid keyword + vector retrieval
* [ ] Metadata filtering by policy/document
* [ ] Retrieval evaluation and relevance metrics
* [ ] Support multiple insurance policies

### Claim Assessment

* [ ] Identify applicable coverage
* [ ] Detect exclusions
* [ ] Determine waiting-period applicability
* [ ] Extract coverage limits and sub-limits
* [ ] Implement generic rules engine
* [ ] Calculate estimated payable amount
* [ ] Generate evidence-backed claim explanation

### Application

* [ ] REST API
* [ ] Web frontend
* [ ] Document upload
* [ ] Claim assessment dashboard
* [ ] Evidence/citation view
* [ ] Claim calculation breakdown

---

## Running Locally

### Prerequisites

* Python 3.10+
* Docker Desktop
* Git
* Groq API key

### 1. Clone the repository

```bash
git clone https://github.com/jyotsna1102/insurance-policy-rag.git
cd insurance-policy-rag
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Set the environment variable:

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key"
```

Linux/macOS:

```bash
export GROQ_API_KEY="your_api_key"
```

### 5. Start PostgreSQL + pgvector

```bash
docker compose up -d
```

### 6. Initialize the database

```bash
python -m db.setup
```

### 7. Ingest the policy

```bash
python -m ingestion.ingest
```

This will:

```text
Extract PDF
    ↓
Build document structure
    ↓
Create chunks
    ↓
Generate embeddings
    ↓
Store chunks + embeddings
```

### 8. Query the policy

Run the RAG tests/examples from the `tests/` directory.

---

## Design Principles

### 1. Don't let the LLM invent policy information

The model should answer from retrieved policy evidence rather than relying on its general knowledge.

### 2. Preserve source information

Every chunk retains its:

* Section
* Section hierarchy
* Page range

This makes retrieved information traceable to the original document.

### 3. Separate retrieval from reasoning

RAG is responsible for finding relevant policy information.

The application layer can then use that information for deterministic business logic.

### 4. Keep financial calculations deterministic

Claim amounts, limits, deductions, and other financial calculations should be performed by application code/rules rather than generated by an LLM.

### 5. Design for multiple policies

The retrieval layer is built around document IDs and metadata so that additional policy documents can be added without redesigning the entire system.

---

## Project Status

**Current stage: RAG prototype**

The core pipeline from:

```text
Policy PDF
    → Extraction
    → Structure
    → Chunking
    → Embeddings
    → pgvector
    → Retrieval
    → LLM
    → Evidence-backed answer
```

is implemented and working.

The next major stage is extending the system from **policy question answering** into **structured claim assessment**.

---

## Disclaimer

This project is an engineering/AI prototype intended for educational and portfolio purposes.

It is **not an insurance claim adjudication system** and should not be used to make real-world insurance or financial decisions.

Policy interpretation and claim settlement are subject to the actual policy wording, applicable regulations, insurer processes, and human review.
