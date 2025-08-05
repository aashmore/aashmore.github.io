---
title: Preparing LaTeX files for arXiv submission
author: anthony-ashmore
tags:
  - arxiv
  - latex
last_modified_at: ""
---

<!-- excerpt start -->
Submitting to the arXiv requires some preparation of your LaTeX files to ensure proper formatting and avoid common pitfalls. This guide walks through the essential steps, from bibliography management during writing to final file cleanup before upload.
<!-- excerpt end -->

## During writing

Use `\bibliographystyle{utphys}` to format your bibliography. [Jacques Distler](https://golem.ph.utexas.edu/~distler/TeXstuff/) wrote this style to work seamlessly with arXiv citations.

At the end of your LaTeX file, before `\end{document}`, add `\bibliography{inspire,extra}`. The `inspire.bib` file contains references from [INSPIRE-HEP](https://inspirehep.net), while `extra.bib` holds references not available there.

Create the `extra.bib` file and add citations as needed. Many mathematics papers, for instance, don't appear on INSPIRE and require manual citation.

Autogenerate `inspire.bib` using the [INSPIRE bibliography generator](https://inspirehep.net/bibliography-generator). In your main `.tex` file, cite works using their INSPIRE key (preferred) or arXiv number - for example, `\cite{Apte:2024vwn}` or `\cite{2405.14830}`. After finishing your draft, upload the main tex file to the bibliography generator, which creates the `inspire.bib` contents automatically. This approach ensures correct arXiv numbers and proper citation formatting.

## Final draft

Clean both `.bib` files using [bibtex-tidy](https://flamingtempura.github.io/bibtex-tidy/). This tool merges or deletes duplicates. You should also use it to remove problematic fields like `url`, `issn`, and `month` that can disrupt reference formatting.

Comment out extra packages like `todonotes` and similar development tools.

Process your main `.tex` file through the [arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner). This removes all comments, preventing embarrassing situations where personal notes appear in the source. You can install this locally with Python or use Google Colab: run `!pip install arxiv-latex-cleaner`, upload files to the `content` folder, then execute `!arxiv_latex_cleaner .` (the period indicates the current directory). This creates a `content_arXiv` directory with the cleaned files.

Format the cleaned `.tex` file using the [LaTeX formatter](https://latex-editor.pages.dev/formatter). While not essential, this creates nicely indented, readable code.

## Uploading to arXiv

~~Create a file named `00README.XXX` in your submission folder's base directory. Enter `nohypertex` as the file's content. This prevents arXiv from running its own `hyperref` version, using instead the version you explicitly load.~~ (No longer needed. The new arXiv submission system [does not add hypertex](https://info.arxiv.org/help/faq/texprobs.html#hyperlink-related-issues:~:text=The%20current%20submission%20system%20does%20not%20automatically%20add%20hypertex).)

Compile your file one final time. Delete all files except `main.tex`, `main.bbl`, ~~and `00README.XXX`~~. Zip these files (not the folder containing them) and upload the zip file as your submission.