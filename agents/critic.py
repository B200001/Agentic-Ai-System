import re

class CriticAgent:
    def __init__(self, llm=None):
        self.llm = llm  # optional

    def evaluate(self, goal: str, output_text: str) -> dict:
        issues = []
        improvements = []

        text = output_text.strip()

        # Rule 1: Must not be empty
        if len(text) < 80:
            issues.append("Output is too short / incomplete.")
            improvements.append("Write a more detailed summary (5-10 lines).")

        # Rule 2: Should contain 'risks' section or bullet points
        has_bullets = bool(re.search(r"(\n-|\n\*|\n•)", text))
        if not has_bullets:
            issues.append("No bullet points found for risks.")
            improvements.append("Add key risks as bullet points.")

        # Rule 3: Should mention at least 3 risks
        risk_keywords = ["bias", "hallucination", "privacy", "jobs", "security", "misinformation", "copyright", "regulation"]
        found = [k for k in risk_keywords if k in text.lower()]
        if len(found) < 2:
            issues.append("Not enough concrete AI risks mentioned.")
            improvements.append("Include real risks like bias, privacy, misinformation, security, job displacement.")

        # Rule 4: Structure check
        if "summary" not in text.lower():
            improvements.append("Add a clear 'Summary' section heading.")

        # Scoring logic
        score = 10
        score -= len(issues) * 2
        score = max(0, min(10, score))

        is_good = score >= 8

        return {
            "score": score,
            "is_good": is_good,
            "issues": issues,
            "improvements": improvements
        }
