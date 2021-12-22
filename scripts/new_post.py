#!/usr/local/bin/python3

from datetime import datetime
from sys import argv
import os

POSTS_DIR = '../docs/_posts/'

date_today = datetime.today().strftime('%Y-%m-%d')

if not argv[1]:
    title = "New Post"
else:
    title = argv[1]

name = f"{date_today}-{title.lower().replace(' ', '-')}.markdown"
path = os.path.join(POSTS_DIR, name)

if os.path.exists(path):
    overwrite = input(f"{name} already exists, overwrite? (y/n)")
    if overwrite != "y":
        exit()

new_post = open(path, "w")
new_post.write(f"---\nlayout: post\ntitle: {title}\ndate: {date_today}\ncategories: []\n---\n")
new_post.write("\nThis is a new post.")
new_post.close()