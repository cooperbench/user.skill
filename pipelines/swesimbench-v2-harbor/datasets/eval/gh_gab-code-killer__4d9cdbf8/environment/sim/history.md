[DEVELOPER]: fait un istorique comme pour chatgpt dans firebase avec l'ia

[AGENT]: The user wants to implement a chat history feature for the AI chat (like ChatGPT) using Firebase. Let me first look at the current `ai-chat.js` to understand the existing implementation.

[DEVELOPER]: Erreur: Gemini 503: This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.

[AGENT]: The user wants me to handle the 503 error from Gemini (high demand) better. Currently, only 429 errors have special handling. I need to add 503 handling with a retry mechanism. Let me look at the current error handling in ai-chat.js.