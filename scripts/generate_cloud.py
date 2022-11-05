import os
from wordcloud import WordCloud

BLOG_ROOT = os.getenv("BLOG_ROOT")
if not BLOG_ROOT:
    BLOG_ROOT = ".."
POSTS_PATH = f"{BLOG_ROOT}/_posts/"
ASSETS_PATH = f"{BLOG_ROOT}/assets/images/"

def remove_tokens(all_text):
    # things I see showing up in the word cloud that I don't want
    to_exclude = [
        "https://",
        "mathbb",
        "endhighlight",
    ]
    split = all_text.split()
    filtered = []
    for token in split:
        yes_exclude = False
        for substr in to_exclude:
            if substr in token:
                yes_exclude = True
                break

        if not yes_exclude:
            filtered.append(token)
    
    return " ".join(filtered)

all_text = ""
for filename in os.listdir(POSTS_PATH):
    # go through all non-draft posts
    if filename.endswith('.markdown') and not filename.endswith('-draft.markdown'):
        all_text += remove_tokens(open(os.path.join(POSTS_PATH, filename)).read())

wordcloud = WordCloud(max_font_size=40).generate(all_text)
wordcloud.to_file(os.path.join(ASSETS_PATH, "blog_wordcloud.png"))