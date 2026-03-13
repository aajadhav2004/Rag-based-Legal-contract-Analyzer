import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import UPLOAD_FOLDER, SECRET_KEY
from rag.loader import load_pdf
from rag.chunker import split_docs
from rag.embeddings import load_embeddings
from rag.vectordb import create_vector_db, load_vector_db
from rag.analyzer import summarize_contract, extract_clauses, detect_risks, calculate_risk_score
from rag.qa_system import ask_question
from auth import User

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

embeddings = load_embeddings()
vector_db = None
is_uploading = False
current_filename = None

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route("/home")
@login_required
def home():
    return render_template("index.html", user=current_user)


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("login.html")


@app.route("/signup")
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("signup.html")


@app.route("/api/signup", methods=["POST"])
def api_signup():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Check if user already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        # Create user
        user = User.create_user(name, email, password)
        if user:
            login_user(user)
            return jsonify({"success": True, "message": "Account created successfully"})
        else:
            return jsonify({"error": "Failed to create account. Please try again."}), 500
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.verify_password(email, password)
    if user:
        login_user(user)
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/upload", methods=["POST"])
@login_required
def upload():

    global vector_db, is_uploading, current_filename

    try:
        is_uploading = True
        
        file = request.files["file"]

        if not file or file.filename == "":
            is_uploading = False
            return jsonify({"error": "No file selected"}), 400

        # Save file
        filename = file.filename
        current_filename = filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        # Load and process PDF
        docs = load_pdf(path)
        chunks = split_docs(docs)

        # Create new vector database (old one is automatically replaced)
        vector_db = create_vector_db(chunks, embeddings)

        # Generate structured analysis
        # Pass first 10 pages for summary
        full_text = " ".join([d.page_content for d in docs[:10]])[:5000]
        summary = summarize_contract(full_text)

        # Pass document chunks for clause and risk extraction
        clauses = extract_clauses(docs)
        risks = detect_risks(docs)
        
        # Calculate risk score
        risk_score = calculate_risk_score(risks)

        is_uploading = False

        return jsonify({
            "summary": summary,
            "clauses": clauses,
            "risks": risks,
            "risk_score": risk_score,
            "filename": filename,
            "success": True
        })
    
    except Exception as e:
        is_uploading = False
        print(f"Upload error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
@login_required
def ask():

    if is_uploading:
        return jsonify({
            "error": "Document is still uploading. Please wait..."
        }), 400

    if vector_db is None:
        return jsonify({
            "error": "Please upload a document first"
        }), 400

    try:
        data = request.json
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        # Get answer with sources
        result = ask_question(vector_db, question, current_filename or "contract.pdf")

        return jsonify(result)
    
    except Exception as e:
        print(f"Ask error: {e}")
        return jsonify({
            "error": "Failed to process question",
            "answer": "An error occurred while processing your question.",
            "sources": []
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
