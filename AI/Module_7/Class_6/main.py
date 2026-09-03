# Choose ONE provider by importing it:

#Change groq --> hf to use hugging face API
#Change hf --> groq to use groq API
from groq import generate_response
# from hf import generate_response

def get_essay_details():
    print("\n=== AI Writing Assistant ===\n")
    topic = input("What is the topic of your essay? ").strip()
    essay_type = input("What type of essay are you writing? ").strip()
    lengths = ["300 words", "900 words", "1200 words", "2000 words"]
    print("Select essay word count:")
    for i, l in enumerate(lengths, 1): print(f"{i}) {l}")
    try:
        idx = int(input("> ").strip())
        length = lengths[idx - 1] if 1 <= idx <= len(lengths) else "300 words"
    except ValueError:
        length = "300 words"
    target_audience = input("Target audience (e.g., High school students): ").strip()
    return {"topic": topic, "essay_type": essay_type, "length": length, "target_audience": target_audience}

def generate_essay_content(details):
    # Temperature is no longer asked here — the AI provider (groq.py / hf.py)
    # automatically decides the best temperature based on the prompt itself.

    intro_p = f"Write an introduction for an {details['essay_type']} essay about {details['topic']} on the topic of {details['length']}."
    intro = generate_response(intro_p, max_tokens=1024)
    print("\n=== Generated Introduction ===\n")
    print(intro)

    print("\nWould you like the body written as a full draft or step-by-step?")
    print("1) Full draft\n2) Step-by-step")
    choice = input("> ").strip()

    if choice == "1":
        body_p = f"Write a full body for an essay on {details['topic']} with the stance of {details['target_audience']}."
        body = generate_response(body_p, max_tokens=1024)
        print("\n=== Generated Full Body ===\n")
        print(body)
    else:
        step_p = f"Write step-by-step arguments for an essay on {details['topic']}. Provide evidence and reasoning."
        body = generate_response(step_p, max_tokens=1024)
        print("\n=== Generated Step-by-Step Body ===\n")
        print(body)

    concl_p = f"Write a conclusion for an {details['essay_type']} essay about {details['topic']} with the stance of {details['target_audience']}."
    concl = generate_response(concl_p, max_tokens=1024)
    print("\n=== Generated Conclusion ===\n")
    print(concl)

    # Return the full essay so feedback_and_refinement can use it to regenerate later
    full_essay = f"{intro}\n\n{body}\n\n{concl}"
    return full_essay

def feedback_and_refinement(details, essay_text):
    try:
        rating = int(input("\nRate satisfaction (1-5): ").strip())
        if rating < 1 or rating > 5: raise ValueError
    except ValueError:
        print("Invalid rating. Using 3.")
        rating = 3

    if rating != 5:
        feedback = input("Provide feedback (tone, structure, etc.): ").strip()
        print(f"\nThank you for your feedback: {feedback}")

        refine_p = (
            f"Here is an essay about {details['topic']} written for {details['target_audience']}:\n\n"
            f"{essay_text}\n\n"
            f"The user gave this feedback: \"{feedback}\".\n"
            "Rewrite the full essay (introduction, body, and conclusion) improving it "
            "based on this feedback while keeping the topic and stance the same."
        )
        refined_essay = generate_response(refine_p, max_tokens=2048)
        print("\n=== Refined Essay (based on your feedback) ===\n")
        print(refined_essay)
    else:
        print("\nThank you! The essay looks good.")

def run_activity():
    print("\nWelcome to the AI Writing Assistant!")
    details = get_essay_details()
    if not details["topic"] or not details["essay_type"]:
        print("Please provide at least a topic and essay type to continue.")
        return
    essay_text = generate_essay_content(details)
    feedback_and_refinement(details, essay_text)

if __name__ == "__main__":
    run_activity()