"""
Security Awareness Training Generator

Generates cybersecurity awareness training content using local LLMs.
Creates slide outlines and detailed content for PowerPoint presentations.

Usage:
    python awareness_generator.py

Environment:
    OLLAMA_MODEL: Model to use (default: llama3.2)
    HF_TOKEN: HuggingFace token for Flux image generation (optional)
    FLUX_SPACE: HuggingFace space for Flux (optional)

Output:
    - Text file with slide content and speaker notes
"""

import os
import threading
import time
from datetime import datetime
from tqdm import tqdm
import ollama

# Configuration
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", ".")

# Optional: Flux image generation
try:
    from gradio_client import Client
    HF_TOKEN = os.getenv("HF_TOKEN")
    FLUX_SPACE = os.getenv("FLUX_SPACE", "black-forest-labs/FLUX.1-schnell")
    if HF_TOKEN:
        flux_client = Client(FLUX_SPACE, hf_token=HF_TOKEN)
        FLUX_AVAILABLE = True
    else:
        FLUX_AVAILABLE = False
except ImportError:
    FLUX_AVAILABLE = False

# System prompt for cybersecurity expert
SYSTEM_PROMPT = "You are a cybersecurity professional with more than 25 years of experience."


def display_elapsed_time(event):
    """Display elapsed time while waiting for API calls."""
    start_time = time.time()
    while not event.is_set():
        elapsed = time.time() - start_time
        print(f"\rProcessing... {elapsed:.1f}s", end="")
        time.sleep(1)
    print()


def generate_outline(industry: str = "general business") -> str:
    """Generate training outline."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""Create a cybersecurity awareness training slide list for a PowerPoint
presentation, targeting employees in the {industry} sector.

Requirements:
- Single-level list (no sub-bullets)
- Each item = one slide
- Cover essential topics: phishing, passwords, social engineering, data protection
- 10-15 slides total

Output only the numbered list."""
        }
    ]

    response = ollama.chat(model=MODEL_NAME, messages=messages)
    return response['message']['content'].strip()


def generate_slide_content(section: str, outline: str) -> str:
    """Generate detailed content for a single slide."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""Create content for this slide from the training outline:

Outline: {outline}

Current Section: {section}

Format your response as:

[Title]
(Clear, engaging title)

[Content]
(3-5 bullet points with key information)

---

[Speaker Notes]
(Detailed talking points for the presenter, 2-3 paragraphs)"""
        }
    ]

    response = ollama.chat(model=MODEL_NAME, messages=messages)
    return response['message']['content'].strip()


def save_to_file(content: str, filename: str):
    """Append content to output file."""
    with open(filename, 'a') as f:
        f.write(content + "\n\n---\n\n")


def main():
    print(f"Security Awareness Training Generator")
    print(f"Using model: {MODEL_NAME}")
    print("-" * 50)

    # Get industry input
    industry = input("Target industry [general business]: ").strip() or "general business"

    # Generate timestamp for output file
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_file = os.path.join(OUTPUT_DIR, f"Security_Training_{timestamp}.txt")

    # Progress tracking
    api_event = threading.Event()

    print("\nGenerating training outline...")
    api_event.clear()
    timer_thread = threading.Thread(target=display_elapsed_time, args=(api_event,))
    timer_thread.start()

    try:
        outline = generate_outline(industry)
        api_event.set()
        timer_thread.join()

        print("\nOutline generated:")
        print(outline)
        print()

        # Parse sections
        sections = [s.strip() for s in outline.split("\n") if s.strip()]

        # Initialize output file
        with open(output_file, 'w') as f:
            f.write(f"# Security Awareness Training - {industry.title()}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Model: {MODEL_NAME}\n\n")
            f.write("## Outline\n")
            f.write(outline + "\n\n---\n\n")

        # Generate content for each slide
        print(f"\nGenerating {len(sections)} slides...")
        for i, section in tqdm(enumerate(sections, 1), total=len(sections)):
            slide_content = generate_slide_content(section, outline)
            save_to_file(f"## Slide {i}\n\n{slide_content}", output_file)

        print(f"\nTraining content saved to: {output_file}")

        # Summary
        print("\n" + "=" * 50)
        print("Generation Complete!")
        print(f"  - Slides: {len(sections)}")
        print(f"  - Output: {output_file}")
        if FLUX_AVAILABLE:
            print("  - Image generation: Available (set HF_TOKEN)")
        else:
            print("  - Image generation: Not configured")

    except Exception as e:
        api_event.set()
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
