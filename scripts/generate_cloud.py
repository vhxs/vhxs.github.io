import os
from wordcloud import WordCloud

BLOG_ROOT = os.getenv("BLOG_ROOT")
if not BLOG_ROOT:
    BLOG_ROOT = ".."
POSTS_PATH = f"{BLOG_ROOT}/_posts/"
ASSETS_PATH = f"{BLOG_ROOT}/assets/images/"

all_text = ""
for filename in os.listdir(POSTS_PATH):
    # go through all non-draft posts
    if filename.endswith('.markdown') and not filename.endswith('-draft.markdown'):
        all_text += open(os.path.join(POSTS_PATH, filename)).read()

wordcloud = WordCloud(max_font_size=40).generate(all_text)
wordcloud.to_file(os.path.join(ASSETS_PATH, "blog_wordcloud.png"))