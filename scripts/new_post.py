#!/usr/local/bin/python3

from datetime import datetime
from sys import argv
import os

POSTS_DIR = '../_posts/'

date_today = datetime.today().strftime('%Y-%m-%d')

if len(argv) <= 1:
    title = "New Post"
else:
    title = " ".join(argv[1:])

name = f"{date_today}-{title.lower().replace(' ', '-')}-draft.markdown"
path = os.path.join(POSTS_DIR, name)

if os.path.exists(path):
    overwrite = input(f"{name} already exists, overwrite? (y/n) ")
    if overwrite != "y":
        exit()

new_post = open(path, "w")
new_post.write(f"---\n"
    f"layout: post\n"
    f"title: {title}\n"
    f"date: {date_today}\n"
    f"categories: []\n"
    f"published: false\n"
    f"---\n")

new_post.write("\nThis is a new post.")
new_post.close()