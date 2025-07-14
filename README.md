GenAI_Document_Assistant

An intelligent assistant to summarize, answer questions, and challenge users with logic-based questions from uploaded
research files (PDF/TXT). Built using Flask, HuggingFace Transformers, and PyPDF2.

Features:
- Upload PDF or TXT files.
- Auto-generate a summary of up to 150 words.
- Ask natural language questions based on the uploaded document.
- Challenge Mode: Generates logic-based questions and evaluates responses.
- Justified answers with context.
- Flask backend with REST APIs.


Tech Stack:
- Flask (Backend REST API)
- Transformers (Summarization & QA)
- PyPDF2 (PDF text extraction)
- uuid / random (Logic Qn generation)


Run:
$ code.py


Endpoints:
- POST /upload : Upload PDF/TXT, returns summary
- POST /ask : Ask questions about file
- GET /challenge : Get logic-based Qs
- POST /evaluate : Evaluate user answers

Author:
Harsh Rana
Email: harshrana3519@gmail.com
GitHub: https://github.com/harshrana3519
