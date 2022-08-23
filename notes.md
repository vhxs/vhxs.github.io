---
layout: post
title: Notes
permalink: /notes/
---

More freeform, less structured, less complete, more subject to change. Mostly (but not all) about software. I read *a lot* about new software technologies, often by choice, sometimes because of projects I work on, and always because I want to keep up with the latest technologies.

<ul>
  {% for item in site.notes  %}
    <li><a href="{{ item.url }}">{{ item.title }} </a></li>
  {% endfor %}
</ul>

[//]: # totally ripped from here: https://raw.githubusercontent.com/philzook58/philzook58.github.io/59834213f54ee87d79963d9cfcb9e48ff8fe9ed6/notes.md