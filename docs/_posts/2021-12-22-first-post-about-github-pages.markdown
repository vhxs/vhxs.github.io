---
layout: post
title:  "How to update this website"
date:   2021-12-22 00:00:00 -0500
categories: meta
---

Jekyll is a static site generator. Github Pages has support for Jekyll and makes it really quick and easy to write blog posts like this. This blog was setup by following the tutorial [here](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll).

Each blog post is rendered from a markdown file, so to create a new blog post, all you have to do is create a markdown file with your new content, and rerender the page. To render the HTML static pages from your markdown files, run `bundle exec jekyll build` within the `doc/` directory (this directory depends on how you configure your GitHub Pages site). Then to view changes locally before they're pushed to your GitHub repo for the world to see, run `bundle exec jekyll serve`. This will start a web server hosting your static website on `localhost:4000` (though host and port are probably configurable from command line). Finally, commit and push, and see your changes [here](https://vhxs.github.io/meta/2021/12/22/first-post-about-github-pages.html).