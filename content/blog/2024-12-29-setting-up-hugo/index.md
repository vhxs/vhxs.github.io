---
title: Setting up a Website with Hugo
author: Vikram Saraph
date: "2024-12-29"
tags:
  - meta
  - website
  - html
  - css
---

## Blogging and static site generators

Yes, I have a website and an online presence. My first incarnation of a (Wordpress) [blog](https://markivikram.wordpress.com/about) from 2013 is still out there living on the Internet; it was named after [Gödel’s constructible universe](https://en.wikipedia.org/wiki/Constructible_universe) since I was obsessed with the foundations of mathematics when studying theoretical computer science at that time.

This post is going to read like a diary entry for how I set up a blog-ready website.

Recently (early 2024), I’d wanted to quickly stand up a website to reestablish an online presence, but without getting bogged down by setting up a [static site generator](https://www.cloudflare.com/learning/performance/static-site-generator/) (SSG) to do it, and so I didn’t initially use an SSG. However in the long term, especially as I continue to blog, I want to use an SSG again. People probably have [lots](https://www.quora.com/Why-do-people-use-a-static-site-generator) [of](https://lobste.rs/s/3lvxdx/why_i_don_t_use_static_site_generator) [opinions](https://news.ycombinator.com/item?id=38126210) [about](https://stackoverflow.com/questions/51726069/why-use-a-static-site-generator-such-as-hugo-over-a-regular-bundler-webpack-pa) [SSGs](https://www.reddit.com/r/webdev/comments/zh13x8/why_do_we_need_static_site_generators/), and I’m not going to pretend having a full understanding of them, but based on what I've read (and some prior experience with it), the main value of an SSG is to separate of content from the design and presentation of that content. The more content you have, the more it probably makes sense to use an SSG. It becomes easier to migrate your content, or to change the design while leaving the content intact.

I used to use [Jekyll](https://jekyllrb.com/) to generate an older (2021-2023) iteration of a blog, hosting the content on [GitHub Pages](https://pages.github.com/). I still want to host my content on GitHub because it's convenient, easy, and I trust GitHub (Microsoft) with my content. But I didn’t like how my old blog looked like every other blog created by following [GitHub’s tutorial](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll) on making a Jekyll website, primarily because I went with the default theme, and I wanted something that was more characteristically me. I could have chosen one of [many themes that others created](https://jekyllthemes.io/), but I still wanted to be able to customize the theming and make it my own. That takes effort though, because I’d have to learn about the template engine that Hugo uses. By contrast, customizing plain HTML is easier than modifying an SSG theme. That’s how I settled on plain HTML to get something out quickly.

My domain is registed with [Cloudflare](https://www.cloudflare.com/products/registrar/). It's easy to [redirect](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) a GitHub Pages domain to your registered domain.

## Hugo

Now I’m once again returning to looking at static site generators, wanting to write and blog online again, and I’ve noticed that many of my favorite bloggers use [Hugo](https://gohugo.io/). I’m not sure I have a good reason for not wanting to use Jekyll again (it may be related to my frustrations with Ruby’s ecosystem when setting up and managing a Jekyll-generated site, though they may have had more to do with me generally being a novice software person at the time), but I would prefer to try out a new static site generator this time. And so I ended up on Hugo. (Who knows, maybe one day I'll switch to [Zola](https://thedataquarry.com/posts/static-site-zola/)).

Choosing Hugo over Jekyll isn’t exactly avoiding the problem of having to create one’s own theme, so I did have to dive into Hugo and its template engine, [Go templates](https://gohugo.io/templates/introduction/), to figure out what it is that I'm doing.

Hugo makes it very easy to create a new website from scratch. It's easier than Jekyll from what I can recall; for example, even though Hugo is written in Go, I haven't had to bother with any of the Go ecosystem to use Hugo so far, as fun as it might be working with Go. This wasn't the case with Jekyll as I had to make sure I had the right version of Ruby installed and had to use [bundler](https://bundler.io/) to work with Jekyll. These are the steps (on a Mac with `brew`) to install Hugo and use it to create a new site, taken [straight from Hugo's site](https://gohugo.io/getting-started/quick-start/):

```bash
brew install hugo           # installs Hugo
hugo new site quickstart    # creates a skeleton for a new site in a directory called "quickstart"
git init                    # initialize a git repository if you want to verison control your blog (you probably want to)
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke    # install predefined a Hugo theme called ananke
echo "theme = 'ananke'" >> hugo.toml    # update Hugo's configuration to use this theme
hugo server                 # build and serve the site
```

The tutorial has you install a theme, specifically `ananke`, which itself lives on GitHub as a [separate repository](https://github.com/theNewDynamic/gohugo-theme-ananke). Roughly, Hugo will take content you write as Markdown files in the `content` directory, and render and style it using the theme that you have installed (or defined yourself).

As I'd said earlier, I wasn't satisified with using a predefined theme, and I certainly didn't want to go with Hugo's default theme either. That meant I had to create a theme on my own, while takes ✨ _time_ ✨. I found a middle ground by looking for themes out there that I liked, and hacking on it to make it sufficiently my own.

## Finding a theme

Like Jekyll, Hugo maintains a [library of themes](https://themes.gohugo.io/) that other people have already created. I looked through the ones that are tagged ["blog"](https://themes.gohugo.io/tags/blog/) to find something that I liked. Many of them are too visually loud for my liking. I like minimal designs, but with enough flair to not be entirely boring. I came across the [XMin theme](https://themes.gohugo.io/themes/hugo-xmin/) which I liked; what lured me was seeing math rendered by \(\LaTeX\) on the example screenshot. I liked [XMin](https://xmin.yihui.org/) because it had all the features that I wanted, implemented it very few line of code. That made it relatively easy to comprehend and was a digestible step towards understanding how to work with Hugo.

After finding XMin, I had to get to work with morphing into something I particularly liked. I'm not going to write about every little detail about the experience, only some of the highlights when working with it. As suggested earlier, themes are themselved managed with separate git repositories. Generally, to install a theme, you install it as a git [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules). Since I wanted to modify XMin, I forked the repo first, and then hacked on that. XMin (and probably all other themes published on Hugo's site) has a directory called `exampleSite` with [sample Markdown content](https://github.com/yihui/hugo-xmin/tree/master/exampleSite). To give me something to work with, I copied whatever was in `exampleSite` into the new `quickstart` directory that was created with `hugo new site`. So I was simultaneously editing the XMin theme and the example content that it gave me, eventually changing the content as well to include what became this post. (I initially had issues with rendering the example content, posted about it on an [existing GitHub issue](https://github.com/yihui/hugo-xmin/issues/72), and subsequently found. The theme's creator is online enough to respond to me within a couple of hours.)

## Modifying it

One thing that XMin did really well was lay out exactly the files that defined the theme:

```
.
├── layouts/
│   ├── 404.html
│   ├── _default/
│   │   ├── single.html
│   │   ├── list.html
│   │   └── terms.html
│   ├── partials/
│   │   ├── foot_custom.html
│   │   ├── head_custom.html
│   │   ├── footer.html
│   │   └── header.html
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── fonts.css
```

I had to change these to change XMin into a theme I truly liked. These files were mostly in `layouts` and in `static/css`. The former defines templates used to generate various pages, while the latter is just styling. `layouts` consists of `_default` and `partials`. As the name suggests, `_default` contains various [default template types](https://gohugo.io/templates/types/), including `list.html` which was used to render the home page of XMin. I didn't like that since Hugo only [falls back](https://gohugo.io/templates/lookup-order/) on `list.html` if it can't find `home.html` or `index.html`. So I copied the contents of `list.html` into a separate `index.html` and changed it so that it didn't display a navbar, since I don't want a navbar on my landing page (at least for now).

`partials` is a directory containing [partial templates](https://gohugo.io/templates/partial/) that are smaller templates which define reusable functionality. For example, header and footer templates are defined here; these ones are often inserted into larger templates.
I didn't like the font that XMin used, so I searched for other fonts. I found myself at [fonts.google.com](https://fonts.google.com/) which is a playground for experimenting with fonts. It also lets you download a font if you want to use one that might not be available by default on your browser. I liked [Roboto](https://en.wikipedia.org/wiki/Roboto), so I pasted an HTML header into `header.html` that fetched Roboto and made it available to use, and then updated `style.css` to actually use it.

Hugo has what are called [taxonomies](https://gohugo.io/content-management/taxonomies/). In their words, taxonomies define logical relationships among content. Taxonomies are an abstraction of concepts like tags or categories. In fact, the two [default taxonomies](https://gohugo.io/content-management/taxonomies/#default-taxonomies) are `tag` and `category`, but in my case, I only wanted tags, so I had to explicitly removed categories by defining my taxonomies in my blog's `hugo.yaml`. Note that `hugo.yaml` is a configuration of your blog, not your blog's _theme_.

The original XMin theme had both `post` and `note` content types. These were also defined in `hugo.yaml`, as part of the `permalink` section. There's really no distinction between these two content types, as the [theme's creator admitted](https://github.com/yihui/hugo-xmin/issues/65). Their purpose as part of the template is to illustrate that one _can_ implememt different content types. I decided to go with one content type called `blog`, and delete the other two, so that all Markdown content is placed under `content/blog` and is referenced via URL that way.

These are the main changes I made that don't concern style. For styling changes I had to modify `style.css`. This is no different than styling plain HTML, so I don't have much to say here. I like red and blue, so I colored hyperlinks red and background colors different shades of blue. I learned about how use [flexboxes](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox) with this fun browser game called [Flexbox Froggy](https://flexboxfroggy.com/).

## Adding social media icons

I added hyperlinked icons for a few of my socials (GitHub, Bluesky, LinkedIn). I'm including a section on this mainly because I was surprised by how difficult it was to find a Bluesky icon. I had figured that Bluesky has a large enough userbase by now for there to be sufficient demand for a free icon that's easy to use. I did eventually find one I was satisified with, but it took some work.

There are lots of icon providers out there. After some searching online, [Font Awesome](https://fontawesome.com/) seems to be the most well known among them, but they've moved to a freemium model as of version 5 (and they're on version 6 now). When you follow their instructions on how to use their icons, you have to create an account, create a [Kit](https://docs.fontawesome.com/web/setup/use-kit), and provide your domain name that will fetch icons you select. Font Awesome will track how many downloads required by your domain from their CDN, and cap free usage at a maximum of 10,000 per year; after that you have to upgrade to a premiem tier.

I was almost ready to give up on Font Awesome because I didn't want to use a freemium service for my website. I tried a few other icon providers, and for the most part they had GitHub and LinkedIn icons available, but no Bluesky icon (Font Awesome does). After more searching, I did find a [StackOverflow post](https://stackoverflow.com/questions/71201741/how-to-use-font-awesome-6-icons) with a user asking whether it's possible to use Font Awesome 6 via CDN, because Font Awesome 4 icons were (and still are) useable [directly via public CDN](https://fontawesome.com/v4/get-started/). Another user answered with a link to a public Font Awesome 6 CDN link for their free-tier icons, and indeed, using the minified CSS that it provides did work for me. I can fetch all three icons I want. It makes me wonder why Font Awesome isn't advertising use of their public CDN for free-tier icons, but I would have to imagine that it's because they want to discourage its use.

I think this summarizes my changes to the original theme that I wanted to touch upon. I didn't have to change it all that much to end up with something I'm reasonably comfortable with using in the future. I'll only add more complexity to the structure of my blog if I end up with so much content that that is warranted, but after this exercise I'm confident I have a reasonable understanding of Hugo (and HTML and CSS) to do that, and only time will tell whether how much I actually write. My blog's source code can be found here, and my theme can be found here (I'm calling it `ivxenz`, which is "vikram" [ROT13'd](https://en.wikipedia.org/wiki/ROT13) and a cute nickname I got from a friend).

## Migrating my lonely blog post

I had a single blog post that I needed to migrate. It's about dice. It was written in plain HTML and so migrating it to Markdown was a chore. This is one reason why SSGs are nice to use.

It was at the time of blog post migration that I realized I want to use [page bundles](https://gohugo.io/content-management/page-bundles/), which logically group Markdown content with associated resources such as images and video. This is what the directory structure looks like; I actually didn't have to change the theme or `hugo.yaml` to use page bundles:

```
content/
├── blog/
│   ├── post1/
│   │   ├── index.md
│   │   └── image1.jpg
│   ├── post2/
│   │   ├── index.md
│   │   └── image2.jpg
```

My blog post on dice has several associated images, and my posts in the future will likely also use embedded images, so it makes sense to structure blog content this way.

Markdown leaves much to be desired when it comes to embedding images; for example, you can't resize images using just Markdown. This isn't a problem specific to Hugo, but Hugo does offer a feature called [shortcodes](https://gohugo.io/content-management/shortcodes/) which augments Markdown when its capabilities fall short. I used the `figure` shortcode to embed images. Hugo is also capable of rendering HTML inserted directly into Markdown, which I had to do to organize two images side by side.

## Using AI to help me

For better or worse, "AI" has become colloquially synonymous with large language models and ChatGPT in particular. In that sense I used AI to setup this blog.

Hugo, as with most other mature software, has a lot of documentation. Usually when learning new software, it doesn't make sense reading literally everything because you don't necessarily need to know everything to get started using it. If I spent my time reading it all, I'd get nowhere, so I had to be selective with how I spent my time. I wagered that Hugo has been around long enough and is used enough for GPT models to have learned enough to answer questions about Hugo and how to use it properly. Indeed, ChatGPT helped me answer some questions I had fairly quickly. And of course, after receiving suggestions from ChatGPT, I cross-checked it with what the documentation actually says. In this was ChatGPT was good at providing me with direction based on vague ideas I had for the blog.

Here's [one (long) conversation](https://chatgpt.com/share/6771ed08-1ca0-8000-bfb3-80442b71a7c8) I had as I worked on the theme and the site. Most questions are concerning the template engine or about styling. Working with AI saved me a lot of time, and it was even helpful with providing me explanations for things (I want to _understand_ what I'm doing instead of just blindly following instructions.)

By contrast, I didn't use AI to generate any _content_ on this blog and I'd like to keep in that way in the future.
