# Choose ONE provider by importing it:

# Change groq --> hf to use hugging face API
# Change hf --> groq to use groq API
from groq import generate_response
# from groq import generate_response

def run_activity():
    print("ZERO-SHOT, ONE-SHOT & FEW-SHOT LEARNING ACTIVITY")

    category = input("Enter a category (e.g., animal, food, city): ").strip()
    item = input(f"Enter a specific {category} to classify: ").strip()

    if not category or not item:
        print("Please fill in both fields to run the activity.")
        return

    # Zero-shot example
    zero_shot = f"Is {item} a {category}? Answer yes or no."
    print("\n--- ZERO-SHOT LEARNING ---")
    y = generate_response(zero_shot, temperature=0.3, max_tokens=1024)   # run generate_response first and store the result in y
    print(f"Response: {y}")                                              # then print y

    # One-shot example
    one_shot = f"""Example:
Category: fruit
Item: apple
Answer: Yes, apple is a fruit.

Now you try. Do not repeat the Category, Item, or the example Answer above — write only your final answer sentence.
Category: {category}
Item: {item}
Previous Answer: {y}
Answer:(explain why {item} is or isn't a {category} in two or three sentences)"""
    print("\n--- ONE-SHOT LEARNING ---")
    x = generate_response(one_shot, temperature=0.3, max_tokens=1024)    # same pattern, store result in x
    print(f"Response: {x}")

    # Few-shot example (kept same as your original prompt format)
    few_shot = f"""Example 1:
Category: fruit
Item: apple
Answer: Yes, apple is a fruit.

Now you try. Do not repeat the Category, Item, or the example Answer above — write only your final answer sentence.
Category: {category}
Item: {item}
Previous Answer: {x}
Answer:(explain why {item} is or isn't a {category} in two or three sentences)"""
    print("\n--- FEW-SHOT LEARNING ---")
    z = generate_response(few_shot, temperature=0.3, max_tokens=1024)
    print(f"Response: {z}")

    # Creative task
    creative_prompt = f"""Write a one-sentence story about the given word.

Example 1: Word: moon
Story: The moon winked at the lovers as they shared their first kiss.

Word: {item}
Story:"""
    print("\n--- CREATIVE FEW-SHOT EXAMPLE ---")
    creative = generate_response(creative_prompt, temperature=0.7, max_tokens=1024)
    print(f"Response: {creative}")

    # Reflection questions
    print("\n--- REFLECTION QUESTIONS ---")
    print("1. How did the responses differ between zero-shot, one-shot, and few-shot?")
    print("2. Which approach gave the most helpful response?")
    print("3. How did the examples influence the model's output?")

if __name__ == "__main__":
    run_activity()