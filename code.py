from flask import Flask, request, jsonify
from transformers import pipeline
import PyPDF2
import os
import random

app = Flask(__name__)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization")

# Global context storage
document_text = ""
filename = ""

@app.route('/upload', methods=['POST'])
def upload():
    global document_text, filename
    file = request.files['file']
    filename = file.filename

    if filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        document_text = "\n".join([page.extract_text() or "" for page in reader.pages])
    elif filename.endswith('.txt'):
        document_text = file.read().decode('utf-8')
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    summary = summarizer(document_text[:3000], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    return jsonify({"summary": summary})

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")
    if not document_text:
        return jsonify({"error": "No document uploaded"}), 400

    answer = qa_pipeline(question=question, context=document_text)
    return jsonify({
        "answer": answer['answer'],
        "confidence": answer['score'],
        "justification": f"Found in text near: ...{document_text[answer['start']:answer['end']+50]}..."
    })

@app.route('/challenge', methods=['GET'])
def challenge():
    sentences = [s for s in document_text.split('.') if len(s.split()) > 5]
    questions = random.sample(sentences, k=min(3, len(sentences)))
    challenge_qs = [f"What is implied or stated in: '{q.strip()}?'" for q in questions]
    return jsonify({"questions": challenge_qs})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    user_answers = request.json.get("answers")
    questions = request.json.get("questions")
    results = []

    for q, user_ans in zip(questions, user_answers):
        ai_ans = qa_pipeline(question=q, context=document_text)
        match = user_ans.lower() in ai_ans['answer'].lower()
        results.append({
            "question": q,
            "your_answer": user_ans,
            "correct_answer": ai_ans['answer'],
            "correct": match,
            "justification": f"Matched: ...{document_text[ai_ans['start']:ai_ans['end']+50]}..."
        })

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
