# AIDRA — Adaptive Intelligent Disaster Response Agent

Artificial Intelligence (AIC 201) CCP-Based Project

## Project Overview

AIDRA (Adaptive Intelligent Disaster Response Agent) is an AI-based disaster management and emergency response simulation system developed in Python. The system demonstrates the integration of multiple Artificial Intelligence techniques for intelligent decision-making in dynamic disaster environments.

The project simulates:

* Ambulance routing
* Victim prioritization
* Resource allocation
* Hazard avoidance
* Dynamic route replanning
* Emergency response coordination

The system is designed to represent a real-world intelligent disaster response framework using integrated AI components.

---

# AI Techniques Implemented

## 1. A* Search Algorithm

Used for:

* Optimal pathfinding
* Safe route generation
* Dynamic navigation

The algorithm calculates efficient rescue routes while avoiding hazards and blocked roads.

f(n)=g(n)+h(n)

Where:

* (g(n)) = actual path cost
* (h(n)) = heuristic estimate to the goal

---

## 2. Constraint Satisfaction Problem (CSP)

Used for:

* Ambulance assignment
* Resource scheduling
* Victim allocation

Constraints include:

* Ambulance availability
* Limited medical kits
* Blocked routes
* Rescue priorities

---

## 3. Machine Learning-Based Prediction

The system includes lightweight predictive logic for:

* Victim survival estimation
* Rescue priority analysis
* Risk evaluation

Factors considered:

* Injury severity
* Rescue delay
* Distance
* Environmental risk

---

## 4. Fuzzy Logic

Used for uncertainty handling in disaster environments.

The fuzzy system evaluates:

* Smoke intensity
* Structural vibration
* Environmental danger levels

Outputs:

* LOW risk
* MEDIUM risk
* HIGH risk

---

## 5. Probabilistic Reasoning

Bayesian-style probabilistic reasoning is used for:

* Route risk estimation
* Hazard prediction
* Decision support

genui{"math_block_widget_always_prefetch_v2":{"content":"P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}"}}

---

# Features

* Real-time disaster simulation
* Interactive graphical interface
* Ambulance movement visualization
* Dynamic obstacle generation
* Victim rescue tracking
* Route replanning
* Simulation metrics dashboard
* Decision logs

---

# Technologies Used

* Python 3
* Tkinter GUI
* Object-Oriented Programming
* AI Search Algorithms
* CSP Techniques
* Fuzzy Logic
* Probabilistic Reasoning

---

# Project Structure

```text id="0v4rj4"
AIDRA/
│
├── AIDRA.py
├── README.md
└── report.pdf
```

---

# How to Run

## 1. Install Python

[Python Official Website](https://www.python.org?utm_source=chatgpt.com)

---

## 2. Run the Project

Open terminal in the project folder:

```bash id="2m74q9"
python main.py
```

---

# System Workflow

1. Disaster environment is initialized
2. Victims are generated with different severity levels
3. AI agent evaluates priorities
4. A* computes rescue paths
5. CSP allocates ambulances
6. Fuzzy logic evaluates environmental risk
7. Ambulances perform rescue operations
8. System dynamically replans routes during obstacles

---

# Educational Objectives

This project demonstrates:

* Intelligent agent architecture
* Search-based problem solving
* Knowledge representation
* Decision-making under uncertainty
* Real-world AI integration

---

# GitHub Repository

[AIDRA GitHub Repository](https://github.com/ab9876-maker/AIDRA?utm_source=chatgpt.com)

---

# LinkedIn Demonstration Video

[LinkedIn Demo Video](https://www.linkedin.com/posts/abu-bakar-7041b140a_this-video-presents-our-aic-201-course-project-ugcPost-7459283312839225344-Hj0O?utm_medium=member_desktop&rcm=ACoAAGhS8bQBIidmqsh_95-D51WhbNDzRQJJmQo&utm_source=chatgpt.com)

---

# Authors

* Abu Bakar
* Adeel Yaqoob

---

# Course Information

Course: Artificial Intelligence (AIC 201)
Instructor: Dr. Arshad Farhad


