# 💡 YouTube Study & Research Studio

> An advanced AI-powered educational platform that converts any YouTube video link into a fully interactive, end-to-end learning workstation. Powered by **Gemini 2.5 Flash**, the system parses video transcripts to instantly generate comprehensive executive summaries, custom study guides, interactive flashcards, responsive testing engines, and contextual chat interfaces.

📺 **Project Presentation:** [Watch Local Walkthrough Video](YOUR_LOOM_OR_YOUTUBE_LINK_HERE)

---

## 📋 Workspace Modules

The platform is engineered into 5 highly targeted learning modules, accessible via a responsive custom navigation bar:

* 📝 **Executive Summary:** Condenses extensive multi-hour video material into structural summaries containing high-signal core takeaways.
* 💬 **Deep-Dive Context Chat:** A session-isolated conversational agent allowing users to interrogate the video context, track down definitions, and run deep-dive queries.
* 📚 **Structured Study Notes:** Automatically builds an elegant textbook-style layout featuring overviews, conceptual definitions, and nested bullet breakdowns.
* 🔮 **Interactive Active-Recall Cards:** Generates sleek, hidden-answer flashcard blocks utilizing collapsible UI accordion elements for optimized self-testing.
* 📊 **Performance Assessment Quiz:** A dynamically compiled multiple-choice testing framework complete with paginated step-through logic and interactive state handling.

---

## ✨ System Architecture Features

* **Zero-Contamination Video Isolation:** Reloading a new URL completely flushes the memory matrix and instantiates a clean context block specific to that video's signature.
* **Persistent Local Audio Parsing Engine:** Gracefully falls back to high-fidelity subtitle processing loops if official video data channels are restricted.
* **Sleek Custom UI Injection:** Overrides standard layouts with micro-padded cards, custom emoji tags, and highly responsive control buttons.

---

## 🛠️ Technologies Used

### **Frontend & Interface:**
* Streamlit (Custom Multi-Tab Layout State Management)
* HTML5 / CSS3 Layout Adjustments

### **AI Core & Document Intelligence:**
* Google GenAI Framework (`gemini-2.5-flash`)
* LangChain Core Architecture (Prompt Templates & Structured Parsing)
* YouTube Transcript API Engine (Transcript Data Extraction Hub)

### **Development Ecosystem:**
* Python 3.11+
* Pydantic (Schema Enforcement)
* Dotenv (Secure Context Injection)

---

## 🚀 Getting Started Locally

*Note: Due to cloud provider IP restrictions implemented by video streaming networks, running this application locally provides the most stable, unthrottled context-loading performance.*

### **Prerequisites**
* Python 3.11 or above
* A Google AI Studio API Key (Gemini)

### **Steps**

#### 1. Clone the repository:
```bash
>> git clone [https://github.com/Ayush6318/YouTube-Study-Studio.git](https://github.com/Ayush6318/YouTube-Study-Studio.git)
>> cd YouTube-Study-Studio
