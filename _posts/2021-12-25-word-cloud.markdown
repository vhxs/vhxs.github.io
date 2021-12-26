---
layout: post
title: Word clouds
date: 2021-12-25
tags: meta language visualization
published: false
---

[Word clouds](https://en.wikipedia.org/wiki/Tag_cloud){:target="_blank"} seem like a fun thing to show people in a presentation, or in a blog post like this. They're one of probably several ways to summarize a set of documents, say if you're taking a first shot at exploratory data analysis of a text corpus that you don't anything about yet. I'm not sure I've seen word clouds online as often as I used to a few years ago when I was still in grad school, with [Google Trends](https://trends.google.com/trends/explore?date=all&geo=US&q=word%20cloud){:target="_blank"} supporting this hypothesis. Maybe because on their own they're not actually so useful beyond showing people a cool thing.

Let's make a script that automatically generates a word cloud from my blog posts' content, each time I re-render the website. It probably won't look very interesting initially, but maybe it'll show me something I don't know about my writing style as I write more?

[GitHub actions](https://docs.github.com/en/actions){:target="_blank"} look like a useful automation tool to add CI/CD to a GitHub repository (for a software development workflow and not just a blog), though I'll go with something more simple as of this writing. Instead of running `jekyll build` each time I update this blog, I'll throw this command in a script, in addition to any other commands I want to run each time I re-render the site.

There's a [Python package](https://pypi.org/project/wordcloud/){:target="_blank"} on PyPI, aptly called `wordcloud`, that generates word clouds. The code I wrote to automatically generate a word cloud from all blog posts is found here, but since I also want to figure out how to include code snippets in a blog post, here's the code:

{% highlight python %}
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

BLOG_ROOT = os.getenv("BLOG_ROOT")
POSTS_PATH = f"{BLOG_ROOT}/_posts/"
ASSETS_PATH = f"{BLOG_ROOT}/assets/images/"

all_text = ""
for filename in os.listdir(POSTS_PATH):
    # go through all non-draft posts
    if filename.endswith('.markdown') and not filename.endswith('-draft.markdown'):
        all_text += open(os.path.join(POSTS_PATH, filename)).read()

wordcloud = WordCloud(max_font_size=40).generate(all_text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(os.path.join(ASSETS_PATH, "blog_wordcloud.png"))
{% endhighlight %}

This script creates and saves an image in `assets/images`. Let's now embed the image, since I also want to know how to embed images:

![Word cloud](/assets/images/blog_wordcloud.png)

Notice this creates a word cloud from *all* tokens in each `.markdown` file, including tokens like `https` (from hyperlinks) and `_blank` (that are part of kramdown/Liquid syntax) but not actual blog content. I could write a Jekyll post parser that extracts content from each `.markdown` file, but that doesn't seem worthwhile.

Other more useful ways to summarize text:
- TF-IDF
    - term frequency–inverse document frequency
    - predates deep learning explosion, introduced in the 70s
    - *A survey conducted in 2015 showed that 83% of text-based recommender systems in digital libraries use tf–idf*, so it's tried and true
    - assigns a number to a each word (or "term"), as a product of "term frequency" and "inverse document frequency"
    - [formulas](https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Definition){:target="_blank"} on Wikipedia are relatively straightforward
- Word embeddings
    - maps words taken from a training corpus to vectors in high-dimensional space (these are "embeddings")
    - semantically similar words (as defined by corpus) are "closed" to one another (as defined by the Euclean metric)
    - common first layer in any neural network that processes text data, since neural networks operate on vectors of numbers
    - good [tutorial](https://www.tensorflow.org/text/guide/word_embeddings){:target="_blank"} TensorFlow's website
