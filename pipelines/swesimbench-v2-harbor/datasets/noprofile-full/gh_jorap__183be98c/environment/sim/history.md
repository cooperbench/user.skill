[DEVELOPER]: i want a jorap.com/randomizer page where I can select a specific category of a database of questions of the ff board games: ito wavelength fun facts the categories are renamed on the description of the type of questions in the collection to ensure there is no copyright issue. once i select the category, it leads to the randmoizer. i want an option to save as an html for offline use.

[AGENT]: <think></think>

[AGENT]: Exploring the site structure and any existing question data for the randomizer feature.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Building the randomizer from scratch: a Hugo data file for questions, a category-picker page, play mode, and offline HTML export.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: The randomizer is live at **`/randomizer/`** (e.g. `https://www.jorap.com/randomizer/`). ### How it works 1. **Pick a collection** — three copyright-safe names for the game types: - **Scale clues** (Ito-style: rank 1–100 without saying the number) - **Spectrum clues** (Wavelength-style: clue between two poles) - **Quick facts** (open trivia prompts) 2. **Pick a category** — titles describe the question type (e.g. “How expensive is it?”, “How hot is this food?”), not branded deck names. 3. **Shuffle** — large prompt card, **Shuffle** for the next random item. 4. **Save offline HTML** — downloads a self-contained `.html` file with embedded prompts and shuffle logic (no network needed). ### Files added | File | Purpose | |------|---------| | `data/randomizer.yaml` | Question database (9 categories, 5 prompts each as starter content) | | `content/english/pages/randomizer.md` | Page at `/randomizer/` | | `layouts/randomizer.html` | Template | | `assets/js/randomizer.js` | Picker, play mode, offline export | | `assets/css/custom.css` | Tile and card styles | ### Adding your own questions Edit `data/randomizer.yaml`. Structure: ```yaml collections: - id: scale-clues # URL: ?set=scale-clues title: Scale clues categories: - id: how-expensive # URL: ?set=scale-clues&cat=how-expensive title: How expensive is it? items: - Your prompt here - id: spectrum categories: - id: food-temperature left: Served […]