[DEVELOPER]: /clear ⎿ (no content)

[DEVELOPER]: Alright so we developed a somewhat working version of the badge finally. All the code is here @local_llm_badge And the plan we sort of followed is here @workbench/docs/OAISYS_BADGE_PLAN.md I need you to first go through every file, flow and optimizations and all kinds of things we did in this local_llm_badge Most of the things were built from the prototypes in @workbench/working_protos Also the trainings models and stuff were done in @workbench/tests you can find folders with ipynb files here. You can also refer to different conversations in @.specstory/history (its a very long conversations history and md files, so read them carefully and do not exhaouse your whole context window just reading those md files) There have been so many amazing customizations, and tweaks and things we did in the code to get this somewhat working and moving, like the asmbly embedded inside cpp to eak out roughly 2-3x more performance from the matmuls in the llm infer code. THIS is just one of many. Another one I remember is doing this whole load/offload for memeory so that processes could run in memory as they were needed and so on. Use exhaustive sub-agents effectively to save on tokens of this main […]

[AGENT]: <think></think>

[AGENT]: I'll launch multiple exploration agents in parallel to thoroughly analyze the codebase, prototypes, training pipelines, and conversation history. This will save context on the main chat while getting comprehensive coverage.

[AGENT]: I'll conduct a thorough exploration of the training notebooks and tests directory. Let me start by examining the structure and reading the notebooks.

[AGENT]: I'll explore the conversation history to extract key insights from the development journey. Let me start by examining the structure of the history folder.

[AGENT]: I'll conduct a thorough exploration of the main firmware, reading all source files to document optimizations and implementations. Let me start systematically.

[AGENT]: I'll conduct a thorough exploration of all working prototypes in the badge project. Let me start by examining the directory structure and then diving into each prototype.

[AGENT]: Let me get a complete list and sort them chronologically:

[AGENT]: Now let me read all the Jupyter notebooks:

[AGENT]: Now let me examine each prototype directory in detail:

[AGENT]: Let me check the correct path for source files:

[AGENT]: Now let me strategically read key files, starting with early ones and focusing on technical decisions. I'll start with the first few sessions and then jump to more recent ones:

[AGENT]: Perfect! Now let me read all these source files systematically:

[AGENT]: Now let me read the remaining notebooks:

[AGENT]: Let me try a different approach:

[AGENT]: These files are quite large. Let me use grep to search for specific key topics instead:

[AGENT]: Now let me read the audio modules:

[AGENT]: Good! Now let me systematically explore each prototype:

[AGENT]: Good, now let me read targeted sections from key files. Let me start with early decision-making files with smaller sizes:

[AGENT]: Let me use Read to examine the files directly:

[AGENT]: Now let me read the ML modules, which are critical:

[AGENT]: Let me read some of the smaller, more focused sessions:

[AGENT]: 206→ 207→_**Agent (claude-sonnet-4-5-20250929)**_ 208→ 209→<think></think> 224→ 225→_**Agent (claude-sonnet-4-5-20250929)**_ 226→ 227→Looking at the code, **there are no frame-related settings or limits configured in the code itself**. 228→ 229→The code plays back frames as fast as it can decode them: 230→ 231→**Key observations:** 232→ 233→- **Line 101-102**: `loop()` calls `player.play()` with no delay 234→- **Line 81-88**: `play()` method decodes and displays frames immediately 235→- **No FPS throttling**: The code doesn't limit playback speed 236→ 237→**The actual frame rate is determined by:** 238→ 239→1. **The MJPEG file itself** - whatever frame rate was encoded by ffmpeg (10 fps in your command) 240→2. **Decoding speed** - how fast the ESP32-S3 can decode JPEG frames from PSRAM 241→ 242→So if your `output.mjpeg` was created with `-r 10` (10 fps), the video contains frames meant to play at 10 fps, but the code will decode them as fast as possible. The actual playback speed depends on the JPEG decoding performance. 243→ 244→If you want to match the encoded frame rate, you'd need to add timing/delay logic in the `play()` method - currently it's a "decode as fast as you can" approach. 245→ 246→--- 247→ 248→_**User**_ 249→ 250→since this originally was a 1080p video getting resized to […]

[AGENT]: Now let me examine the variants and other prototypes:

[AGENT]: Now let me read the remaining ML modules (embed_search, llm_inference, llm_core, sampler, tokenizer) and TTS:

[AGENT]: Excellent! I found a comprehensive session. Now let me read a few more key sessions to capture different phases of the project:

[AGENT]: Excellent! Now let me examine the LLM prototypes:

[AGENT]: 69→ 70→_**Agent (claude-sonnet-4-5-20250929)**_ 71→ 72→<think></think> 75→ 76→_**Agent (claude-sonnet-4-5-20250929)**_ 77→ 78→ 91→ 92→_**Agent (claude-sonnet-4-5-20250929)**_ 93→ 94→<think></think> 97→ 98→_**Agent (claude-sonnet-4-5-20250929)**_ 99→ 100→ 113→ 114→_**Agent (claude-sonnet-4-5-20250929)**_ 115→ 116→<think></think> 119→ 120→_**Agent (claude-sonnet-4-5-20250929)**_ 121→ 122→ 135→ 136→_**Agent (claude-sonnet-4-5-20250929)**_ 137→ 138→<think></think> 141→ 142→_**Agent (claude-sonnet-4-5-20250929)**_ 143→ 144→ 157→ 158→_**Agent (claude-sonnet-4-5-20250929)**_ 159→ 160→<think></think> 163→ 164→_**Agent (claude-sonnet-4-5-20250929)**_ 165→ 166→ 179→ 180→_**Agent (claude-sonnet-4-5-20250929)**_ 181→ 182→<think></think> 187→ 188→_**Agent (claude-sonnet-4-5-20250929)**_ 189→ 190→ 203→ 204→_**Agent (claude-sonnet-4-5-20250929)**_ 205→ 206→<think></think> 216→ 217→_**Agent (claude-sonnet-4-5-20250929)**_ 218→ 219→ 232→ 233→_**Agent (claude-sonnet-4-5-20250929)**_ 234→ 235→<think></think> 238→ 239→_**Agent (claude-sonnet-4-5-20250929)**_ 240→ 241→ 248→ 249→_**Agent (claude-sonnet-4-5-20250929)**_ 250→ 251→ 263→ 264→_**Agent (claude-sonnet-4-5-20250929)**_ 265→ 266→ 273→ 274→_**Agent (claude-sonnet-4-5-20250929)**_ 275→ 276→<think></think> 314→ 315→_**Agent (claude-sonnet-4-5-20250929)**_ 316→ 317→Let me explore the ESP_SR library and check what pin configurations are typically used for speech recognition on ESP32-S3. 318→ 319→_**Agent (claude-sonnet-4-5-20250929)**_ 320→ 321→ 334→ 335→_**Agent (claude-sonnet-4-5-20250929)**_ 336→ 337→ 347→ 348→_**Agent (claude-sonnet-4-5-20250929)**_ 349→ 350→<think></think> 353→ 354→_**Agent (claude-sonnet-4-5-20250929)**_ 355→ 356→ 454→ 455→_**Agent (claude-sonnet-4-5-20250929)**_ 456→ 457→

[AGENT]: 178→ 179→_**Agent (claude-sonnet-4-5-20250929)**_ 180→ 181→

[AGENT]: Now let me read the LLM core, sampler, tokenizer, and TTS modules:

[AGENT]: Excellent! I have rich content from multiple sessions. Let me read a few more focused sessions to capture additional insights:

[AGENT]: 277→ 278→_**Agent (claude-opus-4-5-20251101)**_ 279→ 280→

[AGENT]: Let me read the tokenizer and TTS modules:

[AGENT]: Now let me examine the audio and wakeword prototypes:

[AGENT]: Now let me check the 05_llm_finetuned prototype and look at relevant supporting files:

[AGENT]: Now let me examine the main firmware to understand what was integrated:

[AGENT]: Let me look at some key integrated modules to understand the evolution:

[AGENT]: Let me read the main badge firmware to understand the integration:

[AGENT]: Let me check the README files for more context on what each prototype accomplished:

[AGENT]: Now let me gather information about the audio embedding and wake word modules in the main firmware:

[AGENT]: Perfect! Now I have comprehensive information from multiple sessions. Let me compile the insights summary: ## Summary of Key Insights from Development Journey Based on my exploration of the conversation history from Nov 5 - Dec 1, 2025, here are the most important insights from the OAISYS Badge firmware development: ### **Video Encoding & Compression Optimization (Nov 6)** **Problem**: Initial video encoding at high quality was wasting precious FFat storage space. **Key Discovery**: When downscaling from 1080p to 320×240 (6x reduction per dimension), JPEG compression artifacts are naturally masked because the physical 2-inch display can't resolve them. **Solution Implemented**: - Tested quality settings from `-q:v 5` (highest) to `-q:v 15` (lowest) - Found `q=15` reduces file size by 45% (1.2MB → 664KB) with zero perceptible quality loss at actual display size - Both q=5 and q=15 appear equally pixelated when viewed on a 2-inch display - This technique applies whenever source resolution >> target display resolution **Principle Discovered**: The physical display size is the limiting factor, not JPEG compression quality. Optimization should target perceptual limits, not theoretical metrics. ### **Hardware Audio Configuration - Speech Recognition (Nov 8)** **Challenge**: Needed to set up dual INMP441 microphones for wake word detection while […]

[AGENT]: Perfect! Now let me compile a comprehensive report. Let me create the final document:

[AGENT]: Excellent! I've completed a comprehensive exploration of all the training notebooks and test infrastructure. Let me compile a detailed report on the ML training pipelines, model preparation, and custom techniques used. ## COMPREHENSIVE ML TRAINING PIPELINES REPORT ### EXECUTIVE SUMMARY The OAISYS25 badge project implements a sophisticated multi-stage ML training pipeline using state-of-the-art techniques optimized for ESP32-S3 on-device inference. The system includes 6 major training workflows with custom data augmentation, quantization strategies, and contrastive learning approaches. ## 1. AUDIO EMBEDDING TRAINING PIPELINE ### **Audio Embedding Dataset Generation** (`audio_embedding_dataset.ipynb`) **Scale & Infrastructure:** - 12 GPUs (RTX 4070 SUPER @ 11.6 GB each) running in parallel - 2,008 questions clustered into 1,698 semantic buckets - Target dataset: 32,128 audio samples (2008 × 8 voices × 2 augmentations) - 8 TED speaker samples downloaded from public audio-samples repository **Key Architecture:** - **Audio Branch**: YAMNet (1024-dim) → BatchNorm → Dense(512, relu) → Dense(256) - **Text Branch**: MPNet (768-dim) → BatchNorm → Dense(256) - **Output**: L2-normalized 256-dim embeddings in shared space - **Training**: Contrastive loss with bucketed batch sampling **Custom Training Methodology:** 1. **Bucketed Batch Sampling** (Critical Innovation): - Questions clustered by semantic similarity (threshold 0.85) - Each training batch contains ONE sample per bucket […]

[AGENT]: Excellent! Now I have enough information to create a comprehensive report. Let me compile it: ## COMPREHENSIVE PROTOTYPE EVOLUTION REPORT: OAISYS25 Conference Badge ### Executive Summary The OAISYS25 badge firmware evolved through 6 working prototypes (00-05), each focusing on a specific system component. These prototypes demonstrate a systematic approach to integrating complex ML capabilities on an ESP32-S3 with limited resources. All major techniques developed in prototypes were eventually integrated into the unified main firmware (`local_llm_badge/`). ## PROTOTYPE BREAKDOWN ### **PROTOTYPE 00: Video Loop (Simple Foundation)** **Location:** ` /home/<USER>/project/OAISYS25/badge/workbench/working_protos/00_video_loop/` **Purpose:** Foundation for display system. Plays looping MJPEG video from FFat partition, introducing memory-efficient video playback. **Key Components:** - **MemoryStream class**: Custom Stream wrapper for PSRAM buffer (avoids SD card streaming latency) ```cpp class MemoryStream : public Stream { uint8_t *buf; size_t sz, pos; // implements: read(), peek(), readBytes(), reset() } ``` - **MjpegClass**: JPEG frame extraction and decoding - Searches for SOI (FF D8) and EOI (FF D9) markers - Uses JPEGDEC library with automatic scaling (SCALE_HALF, SCALE_QUARTER, SCALE_EIGHTH) - Supports RGB565 big-endian pixel format **Hardware Integration:** - GPIO 45 (CS), 42 (DC), 1 (BL) for ST7789 240x320 LCD - SPI bus at GPIO 39 (SCK), 38 (MOSI), 40 (MISO) - […]

[AGENT]: Perfect! Now I have read the main firmware thoroughly. Let me compile a comprehensive report documenting all the optimizations and clever techniques. ## COMPREHENSIVE FIRMWARE OPTIMIZATION & IMPLEMENTATION REPORT ### OAISYS25 Badge Main Firmware **Analysis Date:** December 2, 2025 **Firmware Version:** Phase 5 (Video + Gyro + Wake Word + Embedding + LLM + TTS) **Target Hardware:** ESP32-S3-LCD-2 (16MB Flash, 8MB PSRAM) ## EXECUTIVE SUMMARY This firmware demonstrates **production-grade embedded AI optimization** with several innovative approaches: 1. **Dynamic Memory Load/Unload Pattern** - Models sequentially loaded to 6MB shared PSRAM pool 2. **ESP-DSP SIMD Optimization** - PIE vector instructions for matrix multiply & dot products 3. **Multi-Module State Machine** - Clean state transitions with resource management 4. **Dual I2S Audio Pipeline** - Simultaneous mic (16kHz) and speaker (22050Hz) streams 5. **Quantized LLM Inference** - Q8_0 model with inline assembly matmul optimization 6. **MJPEG Video with Rotation** - Low-latency playback with gyro-based display rotation ## MODULE-BY-MODULE ANALYSIS ### 1. DISPLAY MODULE (Video Player) **File:** ` /home/<USER>/project/OAISYS25/badge/local_llm_badge/src/display/video_player.cpp` #### Key Optimizations: **A. Streaming MJPEG Decoder (MjpegClass)** ```cpp // Inline MJPEG decoder - avoids external library overhead // Process: FFD8 (SOI) → ... → FFD9 (EOI) frame markers // Custom frame boundary detection using memcpy […]

[AGENT]: <think></think>

[AGENT]: I've completed comprehensive exploration of the entire codebase. Let me synthesize the findings and propose a multi-part blog series plan. ## Exploration Summary The agents uncovered remarkable depth in this project: ### Key Optimizations Found 1. **PIE Assembly Matmul** (`llm_core.cpp:143-172`) - Inline ESP32-S3 vector assembly achieving 16 int8 MACs per cycle, ~100x faster than scalar code 2. **Dynamic Memory Load/Unload** - Sequential model loading to 6MB shared pool enables running models totaling 10MB+ in 8MB PSRAM 3. **ESP-DSP SIMD** - Used everywhere: FFT for mel-spectrograms, cosine similarity, RMSNorm, softmax 4. **Placement New Interpreter** (`wake_word.cpp`) - Resets TFLite state without reallocation 5. **Bucketed Contrastive Learning** - Training technique ensuring negatives are semantically different 6. **Confusable Negatives** - Wake word trained explicitly on "hey lazy", "hey baby", partial phrases 7. **Three-Phase LLM Training** - Stories → Profile → Q&A instruction tuning ### File Structure Reference ``` badge/ ├── local_llm_badge/ # Main firmware │ ├── local_llm_badge.ino # State machine │ ├── config.h # Pin definitions │ └── src/ │ ├── display/video_player.* # MJPEG + text overlay │ ├── sensors/orientation.* # IMU rotation │ ├── audio/mic_stream.* # Wake word audio │ ├── audio/audio_recorder.* # Recording to PSRAM │ ├── ml/wake_word.* # EdgeNeuron inference │ […]

[AGENT]: <think></think>

[AGENT]: I've created the blog series plan at `workbench/blog_scratch_content/BLOG_SERIES_PLAN.md`. Here's the overview: ## 8-Part Blog Series: "Building an AI Conference Badge: Voice-Activated LLM on ESP32-S3" | Part | Title | Focus | Words | |------|-------|-------|-------| | **1** | Hardware Foundation & Video Display | ESP32-S3-LCD-2, MJPEG playback, gyro rotation | 2000-2500 | | **2** | Dual I2S Audio Pipeline | INMP441 mics, MAX98357A speaker, sample extraction | 1800-2200 | | **3** | Wake Word Detection | EdgeNeuron, mel-spectrogram, confusable negatives | 2500-3000 | | **4** | Audio Embeddings & Contrastive Learning | ESP-DSP FFT, YAMNet-256, SIMD similarity | 3000-3500 | | **5** | Quantized LLM with PIE Assembly | **Flagship** - Q8_0 format, inline assembly matmul | 4000-4500 | | **6** | Robotic TTS with SAM | ESP32-SAM integration, voice tuning | 1500-1800 | | **7** | State Machine & Memory Management | Load/unload pattern, 8MB PSRAM constraint | 2500-3000 | | **8** | Training Infrastructure & Lessons | Multi-GPU, GPT augmentation, hardware quirks | 2500-3000 | ### Highlights Covered - **Assembly optimization** (`llm_core.cpp`) - PIE vector unit doing 16 int8 MACs/cycle - **Memory swapping** - Unload video+embeddings to fit 6MB LLM - **Bucketed contrastive learning** - Novel training technique for […]