# Assignment 3 - Taming LLMs with Groq API  

## 📌 Project Overview  
This project is a **content classification and analysis tool** built using the **Groq API**. It implements various **prompt engineering** techniques to control model behavior, extract precise answers, and analyze confidence levels in responses. The tool allows for structured completions, classification with confidence analysis, and comparison of different prompt strategies.

## 📌 Model Used  
This project utilizes the **LLaMA 3-70B-8192** model provided by Groq API. This model is optimized for natural language processing tasks and allows for structured prompting, classification, and confidence analysis.

## 📌 API Calls  
The project interacts with the Groq API using the following API calls:
- **Completion API:** Used to generate text completions based on structured prompts.
- **Logprob Analysis API:** Retrieves token log probabilities to analyze the model’s confidence in its output.
- **Streaming API:** Optimized for real-time responses, stopping text generation when a specified pattern is detected.

## 📂 Folder Structure  
```
assignment3Adm/
│-- taming_llm.py   # Main Python script
│-- .env            # Stores API key (DO NOT SHARE)
│-- README.md       # Project documentation
│-- .gitignore      # Specifies files to ignore in Git
```


## 📌 Features  
✅ **Basic Completion:** Generates simple model completions.  
✅ **Structured Completion:** Extracts key insights using start/end patterns.  
✅ **Classification with Confidence Analysis:** Classifies text and analyzes confidence levels.  
✅ **Prompt Strategy Comparison:** Tests different prompt strategies for classification tasks.  





