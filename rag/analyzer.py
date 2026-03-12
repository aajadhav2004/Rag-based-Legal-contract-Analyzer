from langchain_groq import ChatGroq
from config import GROQ_API_KEY

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0  # Lower temperature for more consistent, factual responses
)


def generate(prompt):
    response = llm.invoke(prompt)
    return response.content


# Contract Summary with Structured Output
def summarize_contract(text):
    prompt = f"""You are a legal contract analyst. Analyze the contract and provide a STRUCTURED summary.

Contract Text:
{text}

Return ONLY the following structured information (use "Not specified" if information is not found):

Contract Type: [type of contract]
Parties Involved: [list all parties]
Effective Date: [date or "Not specified"]
Duration: [contract duration]
Payment Terms: [payment details]
Termination Conditions: [how contract can be terminated]
Jurisdiction: [governing law/location]
Key Obligations: [main obligations of parties]

IMPORTANT: Do NOT use asterisks (*) or any markdown formatting. Use plain text only.
Be precise and extract ONLY information explicitly stated in the contract.
"""
    return generate(prompt)


# Clause Extraction with Page Numbers
def extract_clauses(docs):
    """Extract key clauses with concise summaries"""
    clauses_list = []
    
    for doc in docs[:10]:  # Analyze first 10 pages for clauses
        page_num = doc.metadata.get('page', 'Unknown')
        text = doc.page_content
        
        prompt = f"""Extract important legal clauses from this contract page and provide CONCISE summaries.

Page {page_num} Text:
{text}

For each clause found, return in this EXACT format:
CLAUSE_TYPE: [Termination/Payment/Confidentiality/Liability/Indemnification/Other]
PAGE: {page_num}
SUMMARY: [1-2 sentence concise summary of what this clause means]
---

IMPORTANT: Do NOT use asterisks (*) or any markdown formatting. Use plain text only.
DO NOT include the full text. Only provide brief, actionable summaries.
Only extract clauses that are clearly present. If no significant clauses on this page, return "No major clauses found."
"""
        
        result = generate(prompt)
        if "No major clauses found" not in result:
            clauses_list.append(result)
    
    return "\n\n".join(clauses_list)


# Risk Detection with Severity and Page Numbers
def detect_risks(docs):
    """Detect risks with severity levels and concise descriptions"""
    risks_list = []
    
    for doc in docs[:15]:  # Analyze first 15 pages for risks
        page_num = doc.metadata.get('page', 'Unknown')
        text = doc.page_content
        
        prompt = f"""Analyze this contract page for potential legal risks and provide CONCISE insights.

Page {page_num} Text:
{text}

For each risk found, return in this EXACT format:
RISK_TYPE: [Unlimited Liability/Termination Penalties/Indemnification/Payment Penalties/One-sided Obligations/Other]
SEVERITY: [Low/Medium/High]
PAGE: {page_num}
INSIGHT: [1-2 sentence concise explanation of why this is risky and what it means]
---

IMPORTANT: Do NOT use asterisks (*) or any markdown formatting. Use plain text only.
DO NOT include the full contract text. Only provide brief, actionable insights.
Only identify REAL risks. If no significant risks on this page, return "No major risks found."
"""
        
        result = generate(prompt)
        if "No major risks found" not in result:
            risks_list.append(result)
    
    return "\n\n".join(risks_list) if risks_list else "No significant risks detected in the analyzed sections."


# Calculate Overall Risk Score
def calculate_risk_score(risks_text):
    """
    Calculate overall contract risk score (1-10) based on detected risks
    1-3: Low Risk (Green)
    4-6: Medium Risk (Yellow/Orange)
    7-10: High Risk (Red)
    """
    
    if not risks_text or "No significant risks detected" in risks_text:
        return {
            "score": 2,
            "level": "Low Risk",
            "description": "Contract appears to have minimal risk factors."
        }
    
    # Count severity levels
    high_count = risks_text.count("SEVERITY: High")
    medium_count = risks_text.count("SEVERITY: Medium")
    low_count = risks_text.count("SEVERITY: Low")
    
    # Calculate weighted score
    # High risk = 3 points, Medium = 2 points, Low = 1 point
    total_points = (high_count * 3) + (medium_count * 2) + (low_count * 1)
    total_risks = high_count + medium_count + low_count
    
    if total_risks == 0:
        score = 2
        level = "Low Risk"
        description = "Contract appears to have minimal risk factors."
    else:
        # Calculate score (1-10 scale)
        avg_severity = total_points / total_risks
        
        if avg_severity >= 2.5:  # Mostly high risks
            score = min(10, 7 + high_count)
            level = "High Risk"
            description = f"Contract contains {high_count} high-severity risk(s). Careful review recommended."
        elif avg_severity >= 1.5:  # Mostly medium risks
            score = min(7, 4 + medium_count)
            level = "Medium Risk"
            description = f"Contract has moderate risk factors. Review key clauses carefully."
        else:  # Mostly low risks
            score = min(4, 2 + low_count)
            level = "Low Risk"
            description = "Contract has some minor concerns but overall acceptable risk level."
    
    return {
        "score": score,
        "level": level,
        "description": description
    }
 

