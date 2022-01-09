from sys import argv
import os

DRAFTS_DIR = '../_drafts/'

if len(argv) <= 1:
    title = "New Post"
else:
    title = " ".join(argv[1:])

name = f"{title.lower().replace(' ', '-')}.markdown"
path = os.path.join(DRAFTS_DIR, name)

if os.path.exists(path):
    overwrite = input(f"{name} already exists, overwrite? (y/n) ")
    if overwrite != "y":
        exit()

new_post = open(path, "w")
new_post.write(f"---\n"
    f"layout: post\n"
    f"title: {title}\n"
    f"tags: \n"
    f"published: false\n"
    f"---\n")

new_post.write("\nThis is a new post.")
new_post.close()