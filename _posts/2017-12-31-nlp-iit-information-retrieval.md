---
date: 2017-12-31 15:01:47.157476
layout: post
title: NLP IIT information retrieval
description: "NLP IIT information retrieval"
tags: [NLP, information retrieval, machine learning]
comments: true
---

### Informational retrieval  (lecture by [ARNAB BHATTACHARYA](https://nlpsummerschool2017.wordpress.com/schedule/))
* Retrieval (finding) of information (e.g., documents) that is mostly unstructured (e.g., text) and is relevant to 
* Tokenization is the process of breaking the text into terms.
  - Token normalization finds more documents Increases recall but decreases precision
* Stemming or lemmatization refers to stripping the word to its root or lemma:
  - e.g. “system”, “systems”, “systematic” Requires morphological analysis and is language specific
  
<!--excerpt-->
* Inverse document frequency: 
  tf-idf(t,d) = tf(t, d) * idf(t)
  - High when t appears in a small number of documents
  - Low when t appears in many documents
  - High when t appears many number of times in d Low when t appears few number of times in d Zero if it does not 
  - appear at all in d
* Scalability
  - Filter query terms with very low idf
  - Cache scores of a champion lists
  - Take union of top-r of every query term to get top-K
  - Build layers, each layer populates docs whose tf for the term > a threshold

<img width="616" alt="screen shot 2017-12-31 at 12 48 08 pm" src="https://user-images.githubusercontent.com/5177427/34464154-e2ad66b8-ee28-11e7-938c-08849b4ebd9b.png">

<!--excerpt-->