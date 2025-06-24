# 🎙️ Multi-Agent Podcast Generator

The **Multi-Agent Podcast Generator** is an AI-powered pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph) that automates the process of creating fully-scripted and audio-generated podcast episodes. This system uses multiple cooperative agents to research, draft, simulate interviews, and generate audio content.

---

## 🚀 Features

- 📌 **Podcast Planning**: Automatically generates podcast metadata and structure.
- 🌐 **Web Search Agent**: Gathers relevant insights about the topic from online sources.
- ✍️ **Content Generation Agent**: Creates talking points and outlines.
- 🧠 **Feedback Loop**: Includes a step for human-in-the-loop refinement.
- 🗣️ **Multi-turn Interview Simulation**: Generates dynamic Q&A between host and expert.
- 🎧 **Intro & Outro Creation**: Crafts compelling openings and endings.
- 🔊 **Audio Synthesis**: Converts the final script into podcast-ready audio.

---

## 🧠 Architecture

The project is built using LangGraph's `StateGraph`, leveraging branching logic and checkpointing. It is composed of two main graph flows:

### 1. Conversation Graph
Handles the dynamic simulation of an interview with multiple turns.

The graph is shown below:

![Graph](https://github.com/user-attachments/assets/491e4403-ad34-408f-a6fd-7deab42c6833)

