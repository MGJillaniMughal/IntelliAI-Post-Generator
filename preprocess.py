import json
from llm_helper import get_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

llm = get_model("openai")

def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = [enrich_post_metadata(post) for post in posts]

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        post['tags'] = [unified_tags.get(tag, tag) for tag in post['tags']]

    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def enrich_post_metadata(post):
    template = '''
    Extract metadata from the following LinkedIn post. Provide the output as a JSON object containing:
    
    1) line_count: The total number of lines in the post.
    2) language: The detected language of the post. This should be one of the following:
       - "English" (standard English)
       - "Hinglish" (a mix of Hindi and English using English script)
       - "Roman English" (Urdu written phonetically in English script)
       - "Urdu" (written in Urdu script)
    3) tags: An array of up to two relevant tags that capture the primary themes or topics of the post.
    
    Instructions:
    - Ensure the JSON object has exactly these three keys: line_count, language, and tags.
    - Do not include any additional text outside the JSON format.

    LinkedIn Post:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post['text']})
    
    try:
        json_parser = JsonOutputParser()
        return post | json_parser.parse(response.content)
    except OutputParserException:
        print("Parsing error, skipping post.")
        return post

def get_unified_tags(posts):
    tags = {tag for post in posts for tag in post['tags']}
    template = '''
    Given a list of tags, unify them according to the following requirements:
    
    1) Merge related tags into a single, unified tag to create a streamlined list. Use examples as a guide:
       - Example 1: Merge "Jobseekers" and "Job Hunting" into "Job Search".
       - Example 2: Map "Motivation", "Inspiration", and "Drive" to "Motivation".
       - Example 3: Map "Personal Growth", "Personal Development", and "Self Improvement" to "Self Improvement".
       - Example 4: Map "Scam Alert" and "Job Scam" to "Scams".
    
    2) Each unified tag should follow title case convention (e.g., "Job Search", "Self Improvement").

    3) Output the result as a JSON object. Do not include any text or comments outside the JSON object.
    
    4) Format the JSON object to show each original tag and its corresponding unified tag. For example:
       {
         "Jobseekers": "Job Search",
         "Job Hunting": "Job Search",
         "Motivation": "Motivation"
       }
    
    Here is the list of tags to unify:
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": ', '.join(tags)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse tags.")
    return res



if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")