const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const progressContainer = document.getElementById('progressContainer');
const resultsSection = document.getElementById('resultsSection');
const qaSection = document.getElementById('qaSection');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const chatContainer = document.getElementById('chatContainer');

let isUploading = false;
let hasDocument = false;
let currentFilename = null;

// File selection
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = `Selected: ${file.name}`;
        uploadBtn.disabled = false;
    } else {
        fileName.textContent = '';
        uploadBtn.disabled = true;
    }
});

// Drag and drop
const fileLabel = document.querySelector('.file-label');

fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#667eea';
    fileLabel.style.background = '#f5f7ff';
});

fileLabel.addEventListener('dragleave', () => {
    fileLabel.style.borderColor = '#e0e0e0';
    fileLabel.style.background = '#fafafa';
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#e0e0e0';
    fileLabel.style.background = '#fafafa';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = `Selected: ${file.name}`;
        uploadBtn.disabled = false;
    }
});

// Upload button
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    isUploading = true;
    hasDocument = false;
    
    // Hide previous results
    resultsSection.style.display = 'none';
    qaSection.style.display = 'none';
    chatContainer.innerHTML = '';
    
    // Show progress
    uploadBtn.style.display = 'none';
    progressContainer.style.display = 'inline-block';
    
    // Animate progress
    animateProgress();

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Complete progress
            setProgress(100);
            
            setTimeout(() => {
                isUploading = false;
                hasDocument = true;
                
                // Hide progress, show results
                progressContainer.style.display = 'none';
                uploadBtn.style.display = 'inline-block';
                
                // Display results
                displayResults(data);
                
                // Show Q&A section
                qaSection.style.display = 'block';
                
                // Reset for next upload
                fileInput.value = '';
                fileName.textContent = '';
                uploadBtn.disabled = true;
            }, 500);
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        isUploading = false;
        progressContainer.style.display = 'none';
        uploadBtn.style.display = 'inline-block';
        alert('Error: ' + error.message);
    }
});

// Progress animation
function animateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        if (!isUploading) {
            clearInterval(interval);
            return;
        }
        
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        
        setProgress(progress);
    }, 500);
}

function setProgress(percent) {
    const circle = document.querySelector('.progress-ring-circle');
    const percentText = document.querySelector('.progress-percentage');
    const radius = 54;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percent / 100) * circumference;
    
    circle.style.strokeDashoffset = offset;
    percentText.textContent = Math.round(percent) + '%';
}

// Display results
function displayResults(data) {
    document.getElementById('summaryContent').textContent = data.summary;
    document.getElementById('clausesContent').textContent = data.clauses;
    document.getElementById('risksContent').textContent = data.risks;
    
    currentFilename = data.filename;
    
    // Display risk score
    if (data.risk_score) {
        displayRiskScore(data.risk_score);
    }
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display risk score with animated bar
function displayRiskScore(riskScore) {
    const riskScoreCard = document.getElementById('riskScoreCard');
    const riskScoreNumber = document.getElementById('riskScoreNumber');
    const riskScoreLabel = document.getElementById('riskScoreLabel');
    const riskScoreBar = document.getElementById('riskScoreBar');
    const riskScoreDescription = document.getElementById('riskScoreDescription');
    
    // Set values
    riskScoreNumber.textContent = riskScore.score;
    riskScoreLabel.textContent = riskScore.level;
    riskScoreDescription.textContent = riskScore.description;
    
    // Calculate percentage (score out of 10)
    const percentage = (riskScore.score / 10) * 100;
    
    // Determine color class based on score
    let colorClass = 'low';
    if (riskScore.score >= 7) {
        colorClass = 'high';
        riskScoreNumber.style.color = '#ef4444';
    } else if (riskScore.score >= 4) {
        colorClass = 'medium';
        riskScoreNumber.style.color = '#f59e0b';
    } else {
        colorClass = 'low';
        riskScoreNumber.style.color = '#10b981';
    }
    
    // Reset and animate bar
    riskScoreBar.style.width = '0%';
    riskScoreBar.className = `risk-score-bar ${colorClass}`;
    
    // Show card
    riskScoreCard.style.display = 'block';
    
    // Animate bar after a short delay
    setTimeout(() => {
        riskScoreBar.style.width = percentage + '%';
        riskScoreBar.textContent = riskScore.score + '/10';
    }, 100);
}

// Ask question
askBtn.addEventListener('click', askQuestion);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') askQuestion();
});

async function askQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;

    // Check if uploading
    if (isUploading) {
        showError('Document is still uploading. Please wait...');
        return;
    }

    // Check if document exists
    if (!hasDocument) {
        showError('Please upload a document first');
        return;
    }

    // Display question
    addMessage(question, 'question');
    questionInput.value = '';
    askBtn.disabled = true;

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok) {
            // Create a container for answer + sources
            const answerContainer = document.createElement('div');
            answerContainer.className = 'answer-container';
            
            // Display answer
            const answerDiv = document.createElement('div');
            answerDiv.className = 'message answer';
            answerDiv.textContent = data.answer;
            answerContainer.appendChild(answerDiv);
            
            // Display sources if available (directly below answer)
            if (data.sources && data.sources.length > 0) {
                const sourcesDropdown = createSourcesDropdown(data.sources);
                answerContainer.appendChild(sourcesDropdown);
            }
            
            chatContainer.appendChild(answerContainer);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        } else {
            showError(data.error || 'Failed to get answer');
        }
    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        askBtn.disabled = false;
    }
}

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function createSourcesDropdown(sources) {
    const sourcesDiv = document.createElement('div');
    sourcesDiv.className = 'sources-dropdown';
    
    // Create collapsible header
    const sourcesHeader = document.createElement('div');
    sourcesHeader.className = 'sources-dropdown-header';
    sourcesHeader.innerHTML = `
        <span class="sources-dropdown-title">📄 View Sources (${sources.length})</span>
        <span class="sources-dropdown-toggle">▼</span>
    `;
    
    // Create collapsible content
    const sourcesContent = document.createElement('div');
    sourcesContent.className = 'sources-dropdown-content';
    sourcesContent.style.display = 'none'; // Hidden by default
    
    sources.forEach((source, index) => {
        const sourceItem = document.createElement('div');
        sourceItem.className = 'source-item';
        
        const sourceHeader = document.createElement('div');
        sourceHeader.className = 'source-header';
        sourceHeader.innerHTML = `<strong>Source ${index + 1}</strong> - Page ${source.page} | ${source.filename || 'contract.pdf'}`;
        
        const sourceText = document.createElement('div');
        sourceText.className = 'source-text';
        sourceText.textContent = source.text;
        
        sourceItem.appendChild(sourceHeader);
        sourceItem.appendChild(sourceText);
        sourcesContent.appendChild(sourceItem);
    });
    
    // Toggle functionality
    sourcesHeader.addEventListener('click', () => {
        const isVisible = sourcesContent.style.display === 'block';
        sourcesContent.style.display = isVisible ? 'none' : 'block';
        sourcesHeader.querySelector('.sources-dropdown-toggle').textContent = isVisible ? '▼' : '▲';
        sourcesHeader.classList.toggle('active');
    });
    
    sourcesDiv.appendChild(sourcesHeader);
    sourcesDiv.appendChild(sourcesContent);
    
    return sourcesDiv;
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    chatContainer.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

// Add SVG gradient for progress circle
const svg = document.querySelector('.progress-ring');
const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
gradient.setAttribute('id', 'progressGradient');
gradient.innerHTML = `
    <stop offset="0%" stop-color="#667eea"/>
    <stop offset="100%" stop-color="#764ba2"/>
`;
defs.appendChild(gradient);
svg.appendChild(defs);
