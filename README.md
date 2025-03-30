Engage with locally deployed Ollama models on your GPU using a `streamlit`-powered GUI.

- Features include:
  - Multiple independent conversations
  - Saving conversation history with a backend SQLite database
  - Current support limited to text interactions; upcoming support for RAG with documents and images
- Available Models:
  - DeepSeekR1-7B
  - Gemma3-4B

# Instructions

1. Get started with [Ollama](https://ollama.com/) by downloading and installing it.
2. Install Gemma3 and DeepSeekR1 models:
   ```
   ollama run gemma3:4b
   ollama run deepseek-r1:7b
   ```
3. Launch the application via command line:
   ```
   streamlit run src/app.py
   ```
