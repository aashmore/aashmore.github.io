---
title: Teaching
nav:
  order: 2
  tooltip: Software, datasets, and more
---

# {% include icon.html icon="fa-solid fa-wrench" %}Projects

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

{% include tags.html tags="publication, resource, website" %}

{% include search-info.html %}

{% include section.html %}

## Introductory Physics I with Lab: Forces and Energy

{% capture text %}

{%
  include button.html
  link="research"
  text="PY 130 (Fall 2024)"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

A calculus-based introduction to the concepts and principles of mechanics, emphasizing translational and rotational kinematics and dynamics, work and energy, conservation laws, and gravitation. Hands-on exploration of physical systems using computer-interfaced laboratory equipment and modeling techniques are used to illustrate physical principles.

{% endcapture %}

{%
  include feature.html
  image="images/photo.jpg"
  link="research"
  text=text
%}