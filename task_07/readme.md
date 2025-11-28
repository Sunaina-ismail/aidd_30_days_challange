# What is SPECKit Plus?

**SPECKit Plus** is a cutting-edge AI prompting framework designed to formalize and structure collaboration between developers and large language model (LLM) coding agents, such as Copilot, Claude Code, or Gemini CLI. It implements **Specification-Driven Development with Reusable Intelligence (SDD-RI)**, a methodology that ensures AI-generated code is consistent, traceable, and aligned with project standards.

The main philosophy behind SPECKit Plus is the *Two-Output Philosophy: every feature must produce both **Working Code** and *Reusable Intelligence*. Developers first define project rules, architecture, and requirements in a structured specification before the AI generates code. This approach guarantees standard-aligned outputs, clear documentation, and a long-term improvement in human-AI collaboration.

---

# 5 Core Concepts of SPECKit Plus

The following five slash commands represent the sequential core concepts of the SDD-RI workflow implemented by SPECKit Plus:

## 1️ /constitution
**Concept:** Purpose: Project-Wide Quality Standards  
This command initiates the creation of the project's Constitution file (`constitution.md`). This document defines the non-negotiable, guiding principles (e.g., must be accessible, use a specific architecture, focus on performance) that all subsequent specifications, plans, and code must adhere to. It serves as the project's foundational rulebook and reusable intelligence artifact.

## 2️ /specify
**Concept:** Purpose: Writing Complete Specifications  
This command captures a new feature idea as a formal high-level specification (Spec). The developer describes what the feature should accomplish and what it should do from a user perspective, without including any technical implementation details. This Spec acts as the source of truth for the new feature.

## 3️ /plan
**Concept:** Purpose: Architecture Decisions and Implementation Plan  
The `/plan` command instructs the AI to analyze the new Spec and the existing Constitution to create a detailed Technical Plan. This plan outlines the required architectural decisions, necessary tools (e.g., Tailwind, specific libraries), and the overall strategy for implementation. It documents how the feature will be built.

## 4️ /tasks
**Concept:** Purpose: Atomic Work Units and Checkpoints  
This command decomposes the Technical Plan into a logical, sequential list of atomic, actionable coding tasks. These tasks are small enough to be easily executed and verified by the AI agent or a developer. This step turns the high-level strategy into a concrete to-do list that minimizes the AI's tendency to "wander off" or generate buggy, unmanaged code.

## 5️ /implement
**Concept:** Purpose: Execute Tasks with AI Collaboration  
This is the final stage where the AI agent is instructed to execute the list of tasks generated in the previous step. The agent writes the actual code for the new feature, constantly checking its output against the Tasks, the Plan, and the original Constitution to ensure consistency, correctness, and adherence to project standards.

---

# Prepared by: *SUNAINA_ISMAIL*#
