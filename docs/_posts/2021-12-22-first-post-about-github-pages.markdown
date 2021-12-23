---
layout: post
title:  "Notes about this blog"
date:   2021-12-22 00:00:00 -0500
categories: meta
published: true
---

As you can probably tell, this blog is very minimal. I am trying to strike the right balance between something that is presentable enough to show, and automated enough to lower the bar for my future self to get content out there, but not so overengineered that all my time is [wasted](https://xkcd.com/974/) [in](https://xkcd.com/1205/) [automation](https://xkcd.com/1319/). As has been observed by [others](view-source:https://danluu.com/writing-non-advice/), there are so many blogs out there that consist of just a single post about starting a blog and nothing more, probably in part due the upfront investment required in bootstrapping a blog and workflow. I myself have been guilty of this more than once and hope that this iteration doesn't suffer the same fate. Different processes work for different people, and GitHub Pages and Jekyll with a few custom automation scripts to aid my workflow process seems to be the sweet spot that I am content with.

Below are some notes for myself and any other readers on how I set up this blog, and how I contribute content to it.

Jekyll is a static site generator. Github Pages has support for Jekyll and makes it really quick and easy to write blog posts like this. This blog was setup by following the tutorial [here](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll). Its source code is [here](https://github.com/vhxs/vhxs.github.io). Locally, I use VSCode to manage content and version control, since its user interface makes it very easy and efficient to write and push new content (though in my opinion it's still important to understand the basic concepts of version control).

Each blog post is rendered from a markdown file, so to create a new blog post, all you have to do is create a markdown file with your new content, and rerender the website. To render the HTML static pages from your markdown files, run `bundle exec jekyll build` within the `docs/` directory (this directory depends on how you configure your GitHub Pages site). Then to view changes locally before they're pushed to your GitHub repo for the world to see, run `bundle exec jekyll serve`. This will start a web server hosting your static website on `localhost:4000` (though host and port are probably configurable from command line). Finally, commit and push, and see your changes [here](https://vhxs.github.io/meta/2021/12/22/first-post-about-github-pages.html).

I added a Python script in `scripts/` called `new_post.py` that creates a default template for a new post. This creates a new post with `published: false` set, so that by default, `jekyll build` doesn't render it. Adding the `--unpublished` flag to `jekyll build` and `jekyll serve`, on the other hand, will force unpublished posts to be rendered and served locally, respectively, so that I can still see how a blog post looks locally before pushing it to the GitHub site. In addition, new posts are post-fixed with `-draft.markdown` so that they are ignored by version control (see below).

In my `.gitignore` file, I've included a `todo.yml` with semi-structured notes about topics I may wish to write about in the future. I have also added the rule `docs/_posts/*-draft.markdown` so that `.markdown` content in draft status is automatically ignored by `git`.