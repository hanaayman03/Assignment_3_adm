import os
import time
from dotenv import load_dotenv
import groq

def load_api_key():
    """Load the Groq API key from .env file."""
    load_dotenv()
    return os.getenv("GROQ_API_KEY")

class LLMClient:
    def __init__(self):
        self.api_key = load_api_key()
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama3-70b-8192"
    
    def complete(self, prompt, max_tokens=1000, temperature=0.7):
        """Generate a completion for a given prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None

def create_structured_prompt(text, question):
    """Creates a structured prompt for structured completions."""
    return f"""
# Analysis Report

## Input Text
{text}

## Question
{question}

## Analysis
"""

def extract_section(completion, section_start, section_end=None):
    """Extracts a section from the completion text."""
    start_idx = completion.find(section_start)
    if start_idx == -1:
        return None
    start_idx += len(section_start)
    if section_end is None:
        return completion[start_idx:].strip()
    end_idx = completion.find(section_end, start_idx)
    if end_idx == -1:
        return completion[start_idx:].strip()
    return completion[start_idx:end_idx].strip()

def classify_with_confidence(client, text, categories, confidence_threshold=0.8):
    """Classifies text into a category with confidence analysis."""
    prompt = f"""
Classify the following text into one of these categories: {', '.join(categories)}.

Response format:
1. CATEGORY: [one of: {', '.join(categories)}]
2. CONFIDENCE: [high|medium|low]
3. REASONING: [explanation]

Text to classify:
{text}
"""
    response = client.complete(prompt, max_tokens=500, temperature=0)
    category = extract_section(response, "1. CATEGORY: ", "\n")
    confidence = extract_section(response, "2. CONFIDENCE: ", "\n")
    reasoning = extract_section(response, "3. REASONING: ")
    confidence_score = {"high": 1.0, "medium": 0.7, "low": 0.4}.get(confidence, 0.0)
    
    if confidence_score > confidence_threshold:
        return {"category": category, "confidence": confidence_score, "reasoning": reasoning}
    else:
        return {"category": "uncertain", "confidence": confidence_score, "reasoning": "Confidence below threshold"}

def compare_prompt_strategies(client, texts, categories):
    """Compares different prompt strategies."""
    strategies = {
        "basic": lambda text: f"Classify this text into one of these categories: {', '.join(categories)}.\n\nText: {text}",
        "structured": lambda text: f"""
Classification Task
Categories: {', '.join(categories)}
Text: {text}
Classification: """,
        "few_shot": lambda text: f"""
Here are some examples:
Text: "I hate this product!" Classification: Negative
Text: "I love it!" Classification: Positive
Now classify this text:
Text: "{text}"
Classification: """
    }
    results = {}
    for strategy_name, prompt_func in strategies.items():
        strategy_results = []
        for text in texts:
            prompt = prompt_func(text)
            result = client.complete(prompt, max_tokens=50, temperature=0)
            strategy_results.append(result)
        results[strategy_name] = strategy_results
    return results
if __name__ == "__main__":
    client = LLMClient()
    
    prompt = "Tell me a fun fact about space."
    response = client.complete(prompt)
    print("Basic Completion Response:\n", response)

    structured_prompt = create_structured_prompt("The sun is a star.", "What is the significance of this?")
    structured_response = client.complete(structured_prompt)
    print("\nStructured Completion Response:\n", structured_response)

   
    categories = ["Positive", "Negative", "Neutral"]
    text_to_classify = "I love this product, it's amazing!"
    classification_result = classify_with_confidence(client, text_to_classify, categories)
    print("\nClassification Result:\n", classification_result)


    texts = ["This laptop is too slow.", "The movie was fantastic!", "Service was okay, but could be better."]
    comparison_results = compare_prompt_strategies(client, texts, categories)
    print("\nPrompt Strategy Comparison Results:\n", comparison_results)
