def classify_document(filename: str, extracted_text: str) -> str:
    haystack = f"{filename} {extracted_text[:2000]}".lower()
    rules = {
        "HR": ("resume", "cv", "employee", "leave", "payroll"),
        "Finance": ("invoice", "payment", "expense", "budget", "tax"),
        "Legal": ("agreement", "contract", "nda", "legal"),
        "Operations": ("purchase order", "inventory", "delivery", "operation"),
    }
    for category, keywords in rules.items():
        if any(word in haystack for word in keywords):
            return category
    return "General"
