---
layout: post
title:  "Notes about this blog"
date:   2021-12-22 00:00:00 -0500
tags: meta
published: true
---

## Writing philosopy
As you can probably tell, this blog is very minimal. I am trying to strike the right balance between something that is presentable enough to show, and automated enough to lower the bar for my future self to get content out there, but not so overengineered that all my time is [wasted](https://xkcd.com/974/){:target="_blank"} [in](https://xkcd.com/1205/){:target="_blank"} [automation](https://xkcd.com/1319/){:target="_blank"}. As has been observed by [others](https://danluu.com/writing-non-advice/){:target="_blank"}, there are so many blogs out there that consist of just a single post about starting a blog and nothing more, probably in part due the upfront investment required in bootstrapping a blog and workflow. I myself have been guilty of this more than once and hope that this iteration doesn't suffer the same fate. Different processes work for different people, and GitHub Pages and Jekyll with a few custom automation scripts to aid my workflow process seems to be the sweet spot that I am content with.

I will iteratively make updates to posts (and sometimes delete them) if I'm displeased with something. Below are some notes for myself and any other readers on how I set up this blog, and how I contribute content to it.

## Hosting this site
Jekyll is a static site generator. Github Pages has support for Jekyll and makes it really quick and easy to write blog posts like this. This blog was setup by following the tutorial [here](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll){:target="_blank"}. Its source code is [here](https://github.com/vhxs/vhxs.github.io){:target="_blank"}. Locally, I use VSCode to manage content and version control, since its user interface makes it very easy and efficient to write and push new content (though in my opinion it's still important to understand the basic concepts of version control).

Each blog post is rendered from a markdown file, so to create a new blog post, all you have to do is create a markdown file with your new content, and rerender the website. To render the HTML static pages from your markdown files, run `bundle exec jekyll build` within the `docs/` directory (this directory depends on how you configure your GitHub Pages site). Then to view changes locally before they're pushed to your GitHub repo for the world to see, run `bundle exec jekyll serve`. This will start a web server hosting your static website on `localhost:4000` (though host and port are probably configurable from command line). Finally, commit and push, and see your changes [here](https://vhxs.github.io/meta/2021/12/22/first-post-about-github-pages.html){:target="_blank"}.

## My custom workflow
I added a Python script in `scripts/` called `new_post.py` that creates a default template for a new post. This creates a new post with `published: false` set, so that by default, `jekyll build` doesn't render it. Adding the `--unpublished` flag to `jekyll build` and `jekyll serve`, on the other hand, will force unpublished posts to be rendered and served locally, respectively, so that I can still see how a blog post looks locally before pushing it to the GitHub site.

In my `.gitignore` file, I've included a `todo.yml` with semi-structured notes about topics I may wish to write about in the future but notes which I don't want globally visible. Since I tend to write stuff incrementally, I use Jekyll's `_drafts` feature to work on drafts locally and added `_draft` to `.gitignore` as well.

## Features I want
I want to be able to render $$\LaTeX$$ so here's [Stokes theorem](https://en.wikipedia.org/wiki/Generalized_Stokes_theorem){:target="_blank"} in terms of differential forms:

$$\displaystyle \int_{\partial \Omega} \omega = \int_\Omega d \omega$$

I also want to include footnotes so here's a footnote[^1] on what I had to do to add LaTeX support.

This blog now has :sparkles: *emojis* :sparkles: to spice things up! I installed `jemoji` using [these instructions](https://github.com/jekyll/jemoji).

## Domain name
I registered the domain name [vikramsaraph.com](vikramsaraph.com). It was pretty straightforward to buy the domain through Cloudflare and also easy to direct [vhxs.github.io](vhxs.github.io) to [vikramsaraph.com](vikramsaraph.com) through their dashboard. [These instructions](https://blog.cloudflare.com/secure-and-fast-github-pages-with-cloudflare/){:target="_blank"} came in handy.

[^1]: There seem to be two popular JavaScript libraries for rendering LaTex in a web browser: MathJax and KaTeX. MathJax is older and easier to setup with Jekyll, but KaTeX is catching on probably because it renders LaTeX faster, so I went with KaTeX. To use KaTeX, I needed to fetch the minified library somewhere in the header, which meant adding a `<script>` element to `<head>` for each post using KaTeX, as outlined in this [StackOverflow answer](https://stackoverflow.com/a/66511285/1411590){:target="_blank"}. To do this in Jekyll, I'd need to modify `_includes/head.html` But since I'm using Jekyll's default [minima](https://github.com/jekyll/minima){:target="_blank"} theme, I didn't have an `_includes` directory. As the README on minima's github repository suggests, I copied `_includes/head.html` to my repository to be able to modify it directory. This also meant copying the `_sass` (styling) directory, since `_includes/head.html` references it.