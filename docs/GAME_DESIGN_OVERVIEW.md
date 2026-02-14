# Game Design Document: Bread & Bureaucracy

**Version:** 1.0
**Date:** February 11, 2026
**Status:** Architecture Locked / Content Pending

---

## 1. Executive Summary

**High Concept**
*Bread & Bureaucracy* is a **TUI-based Roguelike Management Simulator** set in a corporate fantasy mega-dungeon. The player controls a rehabilitated monster (e.g., an Ogre or Troll) working as a baker to pay off legal debts and prove their fitness for society.

**Core Pillars**

1. **The Grind:** A tension-filled management loop of baking, stocking, and haggling, punctuated by "Crisis Encounters" (Minigames).
2. **The Absurdity:** A satirical take on corporate culture ("Human Resources") blended with high-fantasy tropes.
3. **The Science:** A deep "Molecular Gastronomy" cooking system where players manipulate chemical and physical properties (pH, Viscosity, Holiness) to create eldritch delicacies.
4. **The Rules:** Gameplay is governed by "Decrees"—procedurally generated laws that the player must memorize and obey to avoid "Braining" customers.


**Initial Concept**

The _flavor_ of the game is captured should be anchored on the following user description, although the exact details may vary:

```
The game is a TUI-based roguelike bakery management simulator. The player is a vendor NPC in a dungeon that serves adventurers and monsters. The premise is that they are engaged in a rehabilitation program after a work-related injury. For example, they might be an ogre, formerly an elite mob from level 8, who suffered a work related psychological injury and is retraining as a baker merchant npc on level 2. invert common fantasy tropes and subtly make fun of gamers and ttrpg players. Adventurers are the absolute worst but they are also a major source of revenue. They can even be dangerous - trying to steal or randomly attacking. Game setting features isomorphs of labor relations, occupational health and safety, WCB, personal injury litigation but make sure its not obvious.

it's a roguelike that starts each run with you in HR after having violently brained a customer. You have an option to spend points to upgrade things like baking stuff, economics, personality, etc. Then you manage your shop. Most of the interactions run automatically at the bottom of the screen while you do the management sim stuff, but ever now and then, an encounter will maximize the screen and you have to deal with it immediately. It's a minigame that involves answering dungeon trivia that the customer is obsessed with (e.g., Do you even what `MORGOTH`'s fourth tenet is??? a. Crush thine enemies b. Don't eat cave beetle wings c. never wear shoes two days in a row d. goooooold!!!). it is initially extremely absurdly fast and hard, like the player has 1 second to select the right answer from a list of 20. There's a frustration bar that grows with each incorrect answer. When it maxes out, the player brains the customer and the run ends. In the upgrades in HR, the player can invest in upgrades to reduce the number of options, increase frustration tolerance, or get more time to answer. Each of those is specific to one kind of customer e.g., read up on `MORGOTH` -> reduce number of possible responses to `MORGOTH` questions by 50% (stacking upgrade).

There is a company store but it is overpriced. Many supplies come from barter with customers. The game features a contract system for recurring purchases. Much of the gameplay revolves around managing contracts e.g., a contract comes up for six months of really cheap pickled cave spider eggs, so the player switches to recipes that use a lot of them. The menu should consist of isomorphs of real recipes from expensive restaurants (e.g., The Noma Guide to Fermentation - "Grasshopper Garum" (a fermented sauce made from grasshoppers and wax moth larvae)). 

Recipes feature a composition system e.g., donut (generic) = bread (generic) + cream (generic). There is a limited set of archetypal ingredients eg structural agent (i.e., flour), binding agent (e.g., egg), fat, liquid, leavening agent, active bacteria (for fermentation), style (everything else for flavor, texture etc, eg salt, nuts, etc). ingredients implement one or more of those interfaces (e.g., cave beetle flour (structural agent)). Ingredients have a flavor and texture profile for each cooking operation, which includes 5 tastes and a few texture states like mushy, gummy, crunchy, flakey, tender, etc (e.g., murdergrub kidneys are extremely bitter and hard unless pickled, then they become crunchy and sharp). ingredients also have any number of other arbitrary properties which are aggregated upward into the resulting dish e.g., fair trade, organic, favored by the god MORGOTH, etc. There is a limited set of archetypal cooking methods (e.g., baking, frying, deep frying, boiling, steaming, fermenting, quick pickling). There is also a limited set of archetypal recipes e.g., bread, donut, croissant, pie, cake, pudding, etc. These are defined as a composition of abstract ingredients and cooking methods e.g., bread = structural agent + leavening agent + liquid + style. The results of the recipe and the name of the result are computed based on the characteristics of the ingredients, e.g., a pickled murdergrub kidney tart would be sharp, crunchy, flakey. Ingredients have a rarity where the most rare ingredients are used to generate the name of the resulting recipe to avoid listing every ingredient in the name. Should be names with subtitles like on fancy restaurant menus. bakery patrons have preferences like saltiness > 10, 2 ingredients with tag `favored by god MORGOTH`, etc. Amount they will pay, how happy they are, and bakery reputation will depend on maximizing those preferences.

```
---

## 2. Narrative & Setting

### 2.1 The Premise: "Return to Work"

**The Protagonist:** A former Dungeon Boss (Minion Class) diagnosed with "Acute Aggression Dysregulation."
**The Situation:** You are on a **Probationary Rotation**. You cannot kill adventurers (customers) without incurring massive legal fees. You must serve them high-end pastries to pay off your **Debt** and avoid termination (permanent death).
**The Antagonists:**

* **HR (The Liches):** Enforce compliance and issue "Write-Ups."
* **Adventurers (The Karens):** Entitled, dangerous customers who demand loot and discounts.

### 2.2 The World: "Dungeon Management, Inc."

* **Structure:** A for-profit mega-dungeon run by an unseen Board of Directors.
* **Aesthetic:** "Corporate Brutalist High Fantasy." Beige forms, flickering fluorescent torches, and magical bureaucracy.
* **Tone:** *The Office* meets *Dark Souls*. Terrifying monsters are reduced to weeping over spreadsheets.

---

## 3. Gameplay Systems

### 3.1 The Macro Loop (The Rotation)

* **Traversal:** Navigate a Slay-the-Spire style node map representing **Dungeon Sectors** (e.g., Goblin Slums, High Elf Spire).
* **Progression:** Earn "Compliance Points" (XP) to buy certificates in the **Skill Tree** (e.g., "Diversity Training: Undead").
* **Failure State:** **Debt Default** or **Braining a Customer** (Rage Meter hits 100%).

### 3.2 The Micro Loop (The Shift)

1. **Prep:** Buy ingredients, set menu prices, arrange shelves.
2. **Service:** Real-time management. Customers enter, browse, and transact.
3. **Crisis:** Random "Karen" encounters trigger a high-stress Trivia Minigame.
4. **Closing:** Audit revenue, pay daily interest, restock.

### 3.3 The Crisis Encounter (Trivia Minigame)

* **Trigger:** Customer dissatisfaction or random event.
* **Mechanic:** A timed trivia quiz based on active **Decrees**.
* *Question:* "Per Section 4, how must one stir a goblin stew?"
* *Input:* Select the correct answer from a list of 20 options (1 Correct, 19 Distractors).


* **Resource:** **Rage Meter**. Wrong answers increase Rage. At 100%, the player attacks the customer, ending the run.

---

## 4. User Interface (UI) Architecture

**Visual Style:** Text-based User Interface (TUI) using ASCII/NerdFonts. High contrast, keyboard-centric navigation.

### 4.1 Screen Manifest

1. **Main Menu:** Resume/New Shift.
2. **Intake (Character Creation):** Point-buy system for starting stats/species.
3. **Briefing:** Mission orders and quotas for the current sector.
4. **Map:** Node traversal and sector selection.
5. **Bakery Dashboard (Main Game):**
* `Overview`: Alerts and Financials.
* `Recipes`: R&D Interface.
* `Stocks`: Inventory Database.
* `Merchant`: Shelf assignment and Pricing.
* `Kitchen`: Appliance management.


6. **Crisis Encounter:** The Trivia Minigame view.
7. **Settlement:** End-of-run upgrades and debt payment.
8. **Incident Report:** Game Over screen with procedural "Violation Logs."
9. **Cutscene Viewer:** ASCII animation player.
10. **Codex:** Encyclopedia with redacted text based on clearance level.
11. **Settings:** Keybindings and audio.

---

## 5. Technical Architecture

### 5.1 The Data Pipeline

The engine uses a **Data-Driven** architecture where logic is defined in external files.

1. **Source:** `YAML` files (Hand-authored or LLM-generated).
2. **Validation:** `Pydantic` models enforce strict schemas and types at build time.
3. **Ingestion:** Data is flattened and inserted into an in-memory **SQLite** database.
4. **Runtime:** The game engine queries SQLite for all game state.

### 5.2 Database Schema (EAV Model)

* **`WorldInstances`**: The master table of all active entities (Items, Actors).
* **`InstanceStats`**: Continuous variables (Flavor, Elasticity, pH).
* **`InstanceTags`**: Boolean flags (Sacred, Raw, Toxic).
* **`CompositeComponents`**: Tracks the ingredient hierarchy of crafted dishes.

---

## 6. Content & Systems Design

### 6.1 Molecular Gastronomy (The Cooking Engine)

Cooking is not a predefined list of recipes. It is a **State Machine** governed by **Material Science**.

* **Attributes:** We use a controlled vocabulary of "Modernist" terms.
* *Methods:* `Nixtamalize`, `Spherify`, `Lyophilize`, `Inoculate`.
* *Properties:* `Friability`, `Viscosity`, `Water Activity`.


* **Tag Inheritance:**
* *Physical:* Overwritten by process (e.g., `Raw` -> `Cooked`).
* *Heirloom:* Preserved through process (e.g., `Cursed` -> `Cursed Sauce`).



### 6.2 The Decree System (Logic & Trivia)

Rules are defined in `decrees.yaml`. A single entry generates both the **Game Logic** and the **Trivia Question**.

* **Structure:**
* **Predicate:** `Target: Sauce`, `Requires: Low Heat`.
* **Template:** "Section 4 requires {temperature} heat for sauces."


* **Runtime:** The engine enforces the predicate during cooking.
* **Crisis:** The engine fills the template to create a trivia question.

---

## 7. Data Manifest: The Goblin Slums (Vertical Slice)

**File:** `data/content/goblin_slums/manifest.yaml`

### 7.1 Custom Method

* **`Photo-Activation`**: Bombarding bioluminescent matter with UV radiation.

### 7.2 Key Ingredients

1. **`Sewer Eel Liver`**: Toxic to Elves unless *Nixtamalized*.
2. **`Raw Bio-Aggregate`**: Waste sludge. Must be *Emulsified* -> *Inoculated*.
3. **`Myco-Bloom Cake`**: The result of inoculated sludge. Glowing, Umami-rich.

### 7.3 Divine Conflict (Decrees)

* **The Rot-Mother:** Demands `Inoculation` (Mold) for all soft foods.
* **The Sterile One:** Forbids `Myco-Bloom` (Mold) entirely.
* *Conflict:* You cannot please both gods with the same dish.

### 7.4 Signature Recipe

* **`Neon Gut-Bomb`**: A *Spherified* ball of *Myco-Cake* and *Eel Liver*.
* *Tags:* `Glowing`, `Umami`, `Toxic_to_Elves`, `Sacred_Rot`.



---

## 8. Quality Assurance & Testing Strategy

### 8.1 Tier 1: Static Analysis (The Gatekeeper)

* **Tool:** `pytest` + `pydantic`.
* **Objective:** Validate every YAML file against the strict schema.
* **Checks:** Type mismatches, missing fields, invalid Enums, dead reference links.

### 8.2 Tier 2: The Simulation (The Kitchen Sink)

* **Tool:** Headless Python Script.
* **Objective:** Verify the "Physics" of the cooking engine.
* **Tests:**
* **Long Chain Verify:** Ensure `Sludge` -> `Cake` -> `Caviar` chain retains `Glowing` tag.
* **Toxicity Check:** Feed `Raw Liver` to Elf (Expect Sickness). Feed `Cured Liver` to Elf (Expect Safety).
* **Tag Inheritance:** Verify `Sacred` tags survive `Pickling`.



### 8.3 Tier 3: The Trivia Solver (Logic Check)

* **Tool:** Solver Bot.
* **Objective:** Ensure Text matches Code.
* **Method:**
1. Generate 1,000 Trivia Questions from Decrees.
2. Parse the "Correct Answer" string.
3. Run the Game Engine with the variables from the answer.
4. **Fail Condition:** If the Engine returns `Failure` when the Text says `Success`.