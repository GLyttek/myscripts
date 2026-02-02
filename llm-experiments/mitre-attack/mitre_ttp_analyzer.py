"""
MITRE ATT&CK TTP Analyzer

Extracts Tactics, Techniques, and Procedures (TTPs) from cybersecurity
scenario descriptions using local LLMs via Ollama.

Usage:
    python mitre_ttp_analyzer.py

Requirements:
    - Ollama running locally
    - MITRE ATT&CK dataset (enterprise-attack.json)
    - pip install ollama mitreattack-stix20

Environment:
    OLLAMA_MODEL: Model to use (default: llama3.2)
    MITRE_DATA_PATH: Path to enterprise-attack.json
"""

import os
import ollama
from mitreattack.stix20 import MitreAttackData

# Configuration via environment variables
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")
MITRE_DATA_PATH = os.getenv("MITRE_DATA_PATH", "enterprise-attack.json")

# Load the MITRE ATT&CK dataset
try:
    mitre_attack_data = MitreAttackData(MITRE_DATA_PATH)
except FileNotFoundError:
    print(f"Error: MITRE ATT&CK data file not found at {MITRE_DATA_PATH}")
    print("Download from: https://github.com/mitre/cti/releases")
    exit(1)


def extract_keywords_from_description(description: str) -> list:
    """
    Uses LLM to extract security-relevant keywords from a scenario description.
    """
    prompt = (
        f"Given the cybersecurity scenario description: '{description}', "
        "identify and list the key terms, techniques, or technologies relevant to MITRE ATT&CK. "
        "Extract TTPs from the scenario. If the description is too basic, expand upon it with "
        "additional details, applicable campaign, or attack types based on dataset knowledge. "
        "Then, extract the TTPs from the revised description."
    )

    messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity professional with expertise in MITRE ATT&CK framework."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={'temperature': 0.7},
        )
        response_content = response['message']['content']
        keywords = [kw.strip() for kw in response_content.split(',') if kw.strip()]
        return keywords

    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return []


def search_dataset_for_matches(keywords: list) -> list:
    """
    Searches MITRE ATT&CK dataset for techniques matching the keywords.
    """
    matches = []
    for item in mitre_attack_data.get_techniques():
        name_match = any(keyword.lower() in item['name'].lower() for keyword in keywords)
        desc_match = 'description' in item and any(
            keyword.lower() in item['description'].lower() for keyword in keywords
        )
        if name_match or desc_match:
            matches.append(item)
    return matches


def score_matches(matches: list, keywords: list) -> list:
    """
    Scores matches based on keyword frequency in name and description.
    """
    scores = []
    for match in matches:
        score = sum(kw.lower() in match['name'].lower() for kw in keywords)
        if 'description' in match:
            score += sum(kw.lower() in match['description'].lower() for kw in keywords)
        scores.append((match, score))
    return scores


def generate_ttp_chain(match: dict) -> str:
    """
    Generates an example TTP chain for a given MITRE ATT&CK technique.
    """
    prompt = (
        f"Given the MITRE ATT&CK technique '{match['name']}' and its description "
        f"'{match.get('description', 'No description available')}', "
        "generate an example scenario and TTP chain demonstrating its use."
    )

    messages = [
        {
            "role": "system",
            "content": "You are a cybersecurity professional with expertise in MITRE ATT&CK techniques."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={'temperature': 0.7},
        )
        return response['message']['content']

    except Exception as e:
        print(f"Error generating TTP chain: {e}")
        return "Unable to generate TTP chain."


def main():
    print(f"MITRE ATT&CK TTP Analyzer (using {MODEL_NAME})")
    print("-" * 50)

    description = input("Enter your scenario description: ")

    print("\nExtracting keywords...")
    keywords = extract_keywords_from_description(description)
    print(f"Keywords found: {keywords[:10]}...")  # Show first 10

    print("\nSearching MITRE ATT&CK database...")
    matches = search_dataset_for_matches(keywords)
    scored_matches = score_matches(matches, keywords)

    # Sort by score and take top 3
    top_matches = sorted(scored_matches, key=lambda x: x[1], reverse=True)[:3]

    print("\n" + "=" * 50)
    print("Top 3 matches from the MITRE ATT&CK dataset:")
    print("=" * 50)

    for i, (match, score) in enumerate(top_matches, 1):
        print(f"\n[{i}] {match['name']} (Score: {score})")
        print(f"Description: {match.get('description', 'N/A')[:200]}...")
        print("\nExample Scenario and TTP Chain:")
        ttp_chain = generate_ttp_chain(match)
        print(ttp_chain)
        print("-" * 50)


if __name__ == "__main__":
    main()
