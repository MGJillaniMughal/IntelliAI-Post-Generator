from llm_helper import get_model
from few_shot import FewShotPosts

few_shot = FewShotPosts()
llm = None  # Global variable to store the selected model instance

def set_llm_model(choice):
    """Sets the global llm instance to the chosen model."""
    global llm
    llm = get_model(choice)

def get_length_str(length):
    """Maps length descriptor to text representation."""
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 12 lines"
    elif length == "Long":
        return "12 to 18 lines"

def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag):
    length_str = get_length_str(length)
    prompt = f'''
    Generate a LinkedIn post based on the following details. Ensure the post aligns with the specified language and length requirements. Do not include any introductory text.
    1) Topic: {tag}
    2) Length: {length_str} (Short: 1-5 lines, Medium: 6-12 lines, Long: 12-18 lines)
    3) Language: {language}

    Language Guidelines:
    - English: Write in standard English.
    - Hinglish: A blend of Hindi and English words, using the English script.
    - Roman English: English words written phonetically as spoken in Urdu, using the English script.
    - Urdu: Written in the Urdu language and script.

    Please follow these language instructions closely. Use examples where necessary to align with the tone and style relevant to LinkedIn.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)
    if examples:
        prompt += "\n4) Use the style shown in the examples below."
        for i, post in enumerate(examples[:2]):  # Limit to two examples
            prompt += f'\nExample {i+1}:\n{post["text"]}'
    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))