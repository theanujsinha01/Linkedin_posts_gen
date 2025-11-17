import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):   # FIXED: __init__
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)

            # FIX: Ensure 'line_count' exists before applying
            if "line_count" in self.df.columns:
                self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            else:
                raise KeyError("'line_count' column missing in JSON")

            # Collect unique tags
            self.df["tags"] = self.df["tags"].apply(lambda x: x if isinstance(x, list) else [])
            all_tags = sum(self.df["tags"], [])
            self.unique_tags = list(set(all_tags))

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(posts)
