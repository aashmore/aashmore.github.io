---
title: Research
nav:
  order: 1
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-microscope" %}Research

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

{% include search-box.html %}

{% include search-info.html %}

{% include section.html %}

## Deep learning for gauge theories

{% capture lattice %}
  {% include figure.html image="images/nn.png" caption="A gauge-equivariant neural network." width="400px" %}
{% endcapture %}

{%
  include float.html
  content=lattice
  flip=false
%}

Lattice gauge theories play a pivotal role in our understanding of fundamental physics in nature, particularly in the realm of quantum chromodynamics (QCD), which governs the strong nuclear force. QCD, a non-abelian gauge theory, describes the interactions between quarks and gluons, the elementary constituents of protons and neutrons. Despite its simple formulation, the non-perturbative regime of QCD exhibits remarkably complex phenomena, including confinement and chiral symmetry breaking. Monte Carlo methods have led to profound insights into the behaviour of these theories at strong coupling, and produced remarkable results such as computation of hadron masses from first principles. Despite the tremendous progress made over the last four decades, fundamental stumbling blocks such as the sign problem and the inability to simulate real-time dynamics still remain. 

We are actively investigating the use of neural networks to model the ground-state wavefunctions of lattice gauge theories. Our previous work has included studying discrete gauge theories using gauge-equivariant convolutional neural networks. We identified the distinct topological phases and the confinement phase transition in these systems. For Z2 theories, we probed the continuous transition and computed critical exponents, with excellent agreement with previous Monte Carlo simulations and the conformal bootstrap. These findings suggest that so-called neural-network quantum states are a promising method for precision studies of lattice gauge theory.

{% include float.html clear=true %} 

{% include list.html data="citations" component="citation" style="rich" filters="lattice: true" %}



{% include section.html %}

## Numerical and machine-learning methods for string theory

{% capture numerical %}
  {% include figure.html image="images/eigenvalues.png" caption="Scalar eigenvalues of the Laplacian on a Calabi-Yau manifold as a function of complex structure moduli." width="400px" %}
{% endcapture %}

{%
  include float.html
  content=numerical
  flip=false
%}

DESCRIPTION HERE

{% include float.html clear=true %} 

{% include list.html data="citations" component="citation" style="rich" filters="numerical: true" %}

{% include section.html %}

## Geometric structures in supergravity and string theory

{% capture geometry %}
  {% include figure.html image="images/moduli_space.png" caption="Space of holomorphic structures with a flow by complexified generalised diffeomorphisms." width="400px" %}
{% endcapture %}

{%
  include float.html
  content=geometry
  flip=false
%}

DESCRIPTION HERE

{% include float.html clear=true %} 

{% include list.html data="citations" component="citation" style="rich" filters="geometry: true" %}

{% include section.html %}

## String model building and phenomenology

{% capture model %}
  {% include figure.html image="images/model.png" caption="Distribution of unification scale among heterotic string models." width="400px" %}
{% endcapture %}

{%
  include model.html
  content=numerical
  flip=false
%}

DESCRIPTION HERE

{% include float.html clear=true %} 

{% include list.html data="citations" component="citation" style="rich" filters="model: true" %}
