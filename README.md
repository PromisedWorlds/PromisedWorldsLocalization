# Contributing to Promised Worlds Localization 

Thank you for helping improve [**Promised Worlds**](https://github.com/PromisedWorlds/PromisedWorlds) by contributing translations.  
This guide explains the simplest ways to add or update localization: either directly on the GitHub website or using GitHub Desktop.

---

## How Localization Works
- All the translations are in the `GameData/PromisedWorlds/Misc/Localization` folder. 
- Each language has its own `.cfg` file, for example:  
  - `en-us.cfg` (English)  
  - `de-de.cfg` (German)  

Entries look like this:
```cfg
#LOC_PW_PlanetName = Debdeb
```
Only change the text after `=`.

---

## Option 1: Using the GitHub Website (easiest)
1. Go to the repository on GitHub.  
2. Open `GameData/PromisedWorlds/Misc/Localization` and select the file for your language.  
   - If your language doesn’t exist yet, copy `en-us.cfg` and rename it (e.g. `es-es.cfg`).  
3. Click the **pencil icon** to edit the file.  
4. Add or update translations.  
5. Scroll down, write a short description of your changes, and click **Propose changes**.  
6. GitHub will guide you to open a **pull request**.

---

## Option 2: Using GitHub Desktop
1. Fork the repository on GitHub.  
2. Open GitHub Desktop and **clone your fork**.  
3. Create a new branch for your work.  
4. Edit or add the `.cfg` files in `GameData/PromisedWorlds/Misc/Localization`.  
5. Commit your changes in GitHub Desktop and **push** them to your fork.  
6. On GitHub, open a **pull request** from your branch.

---

## Testing your localizations
- Download LanguageChanger by averageksp from CKAN or [GitHub](https://github.com/averageksp/LanguageChanger)
- Launch the game, change it to the correct language you have translated to.
- Restart the game, and test your changes.
- If something didn't go right ideally join our [discord server](https://discord.gg/CDbjJgTjXC) or open a Pull Request with your changes and we'll fix it.

---

## Translation Guidelines:
- Translations should be grammatically correct and use proper punctuation and capitalization.
- Please be serious in translation - no jokes / easter eggs. Users should have as close to the same experience as possible, regardless of what language they play.
- Be mindful of sensitivities - keep translations PG and avoid swearing / offensive language.
- Try to stick to the meaning and tone of the original English writing where possible.
- If you have an issue, such as a word that you can't translate, or need help, contact me @levitato on Discord
- Jokes are also hard to translate - a literal translation of the English text may not be funny in your language! I will work with you for that, where there are jokes in the English text.
- Please be open to criticism and review from other translators - we want to make sure all translations are as high quality as possible, which means checking each other's work for mistakes - we all make them!
- Likewise, please review other translators' work in the same language, and offer helpful and constructive criticism.

---

## Review
- Pull requests will be reviewed. If something needs fixing, you’ll get feedback.  
- Once approved, your changes will be merged.  

---

## License
By contributing, you agree that your contributions will be licensed under the Attribution-NonCommercial-ShareAlike 4.0 International license. See https://github.com/PromisedWorlds/PromisedWorlds/blob/main/LICENSE.md for more.
