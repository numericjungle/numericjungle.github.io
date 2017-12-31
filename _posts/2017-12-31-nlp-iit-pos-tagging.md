---
date: 2017-12-31 15:04:56.824688
layout: post
title: NLP IIT POS tagging
description: "NLP IIT POS tagging"
tags: [NLP, machine learning, POS tagging]
comments: true
---
### NLP POS-tagging (lecture by [Pushpak Bhattacharyya](https://nlpsummerschool2017.wordpress.com/schedule/))

<!--
<img width="594" alt="screen shot 2017-12-31 at 1 08 44 pm" src="https://user-images.githubusercontent.com/5177427/34464212-c6212f54-ee2b-11e7-89af-4abc9818708a.png">
-->

* NLP= Ambiguity Processing
  - Lexical Ambiguity: dog (noun vs verb), (animal vs detesable person), contexts. 
  - Structural Ambiguity
  - Semantic Ambiguity
  - Pragmatic Ambiguity

<img width="336" alt="screen shot 2017-12-31 at 12 57 24 pm" src="https://user-images.githubusercontent.com/5177427/34464178-3ed0dc12-ee2a-11e7-8a9f-95fa73302487.png">
<!--excerpt-->
* Main methodology
  - A: extract parts & features
  - B: which is in correspondence with A: extract parts and features
  - Learn mapping of these features and parts
  - Apply to new situations (decoding)
 

### POS tagging
* POS Tagging: attaches to each word in a sentence a part of speech tag from a given set of tags called the Tag-Set
* A word can have multiple POS tags
* New examples break rules, so we need a robust system.
* Generative: HMM
  - Training: Maximize the likelihood of observations
  - Testing: search the best POS tag sequence in the hypothesis space
  - generate POS tag sequences and score them
  - HMM
  - Given the observation sequence, find the possible state sequences- Viterbi
  - Given the observation sequence, find its probability- forward/backward algorithm
  - Given the observation sequence find the HMM prameters.- Baum-Welch algorithm
* Discriminative
  - Training: Maximize entropy of probability distribution subject to the constraints from data
  - Testing: discriminate amongst hypotheses by scoring them
  - MEMM, CRF
<img width="598" alt="screen shot 2017-12-31 at 2 22 25 pm" src="https://user-images.githubusercontent.com/5177427/34464492-11dd0ed6-ee36-11e7-9709-4abecdda3457.png">

* Classification
  - Training: Minimize loss function (Total sum square error, cross entropy- soft_max)
  - Testing: classify the input into one of the class
  - SVM, neural net
* Deep Learning
  - Training: minimize the loss function
  - DL = feature discovery + classification
  - classifiy POS tag + discover required features
<img width="644" alt="screen shot 2017-12-31 at 2 23 29 pm" src="https://user-images.githubusercontent.com/5177427/34464501-3b24c5ae-ee36-11e7-8418-95bd5182e76a.png">

* Deep Learning II - sequence to sequence
<img width="631" alt="screen shot 2017-12-31 at 2 30 43 pm" src="https://user-images.githubusercontent.com/5177427/34464520-483e786a-ee37-11e7-8b53-5d5e1fbb3a5f.png">
 
  - An RNN encoder (words -> hidden states) + a RNN decoder (hidden states -> tags)
  - get a richer representations from the sentences
  - long dependencies 
    - Represent the source sentence by the set of output vectors from the encoder)
    - Replace RNN encoder to LSTM
  - RNN cann't see future -> use a bdirectional RNN/LSTM
  - Due to the sequential nature of RNN, parallelism is limited.
  - Compare to CNN: good in parallel, can't model the whole history, more local. 
 
* POS tagging vs MT:
  - 1-1 vs 1 to none ~ many
  - the order may change in MT
  - one to many/ many to one

* Complexity:
  - POS, HMM: linear
  - MT, Bear search: exponential

