import pandas as pd
import json

class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = []
        self.load_posts(file_path)

    def load_posts(self, file_path):
        # Load posts data and normalize into a DataFrame
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)

            # Extract unique tags
            all_tags = [tag for tags in self.df['tags'] for tag in tags]
            self.unique_tags = sorted(set(all_tags))

    def get_filtered_posts(self, length, language, tag):
        # Filter posts based on length, language, and tag
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        return df_filtered.to_dict(orient='records')

    @staticmethod
    def categorize_length(line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 12:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags
