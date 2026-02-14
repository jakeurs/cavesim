# UI and Gameplay Design Specification: Bread & Bureaucracy

This is the locked-in technical specification for all 11 screens of the game application.

### **1. Title & Main Menu**

* **`GameLogo`**: Static ASCII block art.
* **`MainMenuOptions`**: Vertical selectable list. "RESUME SHIFT" is disabled if no save exists.
* **`SaveSlotSelector`**: Modal overlay. Displays metadata (Sector, Debt, Status: ACTIVE/ARCHIVED).
* **`NewsTicker`**: Scrolling bottom bar with flavor headlines.
* **`VersionFooter`**: Build/Copyright info.

### **2. Character Creation (The Intake Form)**

* **`PipelineProgressIndicator`**: Top bar tracking the creation steps.
* **`CurrencyWallet`**: Tracks starting Gold/Points for character builds.
* **`NavigationControls`**: Back/Next buttons (conditional on valid input).
* **`ModuleRenderer` (Left Panel)**: Polymorphic input form. Renders Selectors, Sliders, or Markets based on the current step.
* **`ManifestProjection` (Right Panel)**: Live "Ghost Sheet." Visualizes changes (`+STR`, `-CHA`) in real-time when hovering options in the ModuleRenderer.

### **3. Narrative Briefing**

* **`BriefingHeader`**: Displays Sector Name/Transfer Order Title.
* **`NarrativeTextBody`**: Procedural "Memo" generator. Injects sector variables into corporate templates.
* **`StampAnimation`**: Overlay effect ("APPROVED").
* **`ObjectiveList`**: Bulleted list of quotas derived from Sector Config.
* **`ContinueButton`**: Acknowledges orders.

### **4. Map / Traversal (The Mega Dungeon)**

* **`MetaStatsHeader`**: Persistent bar (Debt, Gold, HP, Date).
* **`DungeonMapVisualizer`**: Vertical Slay-the-Spire style node graph. Fog of War obscures future depths.
* **`SectorDetailsPanel`**: Hover inspector. Shows Threat Level, Dominant Culture, and Resource Yield.
* **`BossIntelDisplay`**: Persistent dossier on the Sector Boss. Tracks Approval rating and unlocked "Likes/Dislikes."
* **`TravelControls`**: Input handler for moving player token to connected nodes.

### **5. Bakery Shift (The Management Sim)**

* **`DashboardNav`**: Tab bar (`1-9` hotkeys) to switch main views.
* **`CounterViewport`**: Passive visualizer. Renders `TransactionSummary` objects (Customer sprite + text bubble) from the backend.
* **`OverviewTab`**: Executive summary. Aggregates alerts (Low Stock, Rent Due) from other tabs.
* **`RecipesTab`**: R&D Interface. Composes `Base` + `Ingredients` -> `Product`. Auto-calculates flavor profile.
* **`ContractsTab`**: Futures Market. "Signed Obligations" (Active) vs "Open Market" (Available).
* **`StocksTab`**: Inventory Database. Drill-down: `Category` -> `Batch` -> `Instance Inspector`.
* **`MerchantTab`**: Storefront Manager. Assigns Stocks to Shelf Slots and sets Prices. Unlocks Analytics overlays.
* **`MarketTab`**: High-Frequency Trading. Sets global "Buy Multipliers" (Barter) and "Sell Rules" (Demographic targeting) based on the Item Ontology.
* **`KitchenTab`**: Production Floor. Manages Appliance queues (Ovens, Pots).
* **`CharacterTab`**: RPG Manager. Inventory + Paper Doll Equipment. Reuses `ManifestProjection` for stat diffs.
* **`HistoryTab`**: Scrollable session log (Sales, System, Combat).

### **6. Crisis Encounter (The Minigame)**

* **`AnswerList`**: The "Wall of Text." A dense, scrollable vertical list of 20 options (1 Correct, 19 Distractors). No hotkeys; manual scrolling required.
* **`RageMeter`**: The single resource. Combines Time/Health. Fills passively (Tension) and on mistakes (Spikes). 100% = Game Over (Braining).
* **`CustomerActionLog`**: Text log of "Attacks" (annoyances) that spike Rage during the encounter.
* **`EnemyPortrait`**: ASCII art of the antagonist.

### **7. HR / Settlement (End of Run)**

* **`SettlementInvoice`**: Itemized receipt (Revenue - Taxes/Fees).
* **`DebtTicker`**: The Score. Animates "Interest Accrual" (Up) then "Payment" (Down). Usually results in net loss.
* **`UpgradeTreeRenderer`**: "Professional Development." Tree-list of certificates. Purchasing nodes unlocks children.
* **`NextAssignmentButton`**: Generates map for the next sector.

### **8. Incident Report (Game Over)**

* **`IncidentHeader`**: "TERMINATED" banner.
* **`ViolationLog`**: Procedural text generator. Describes the specific cause of death/violence in dry HR jargon using `Violations.yaml`.
* **`SentencingStamp`**: Visual animation. Slams a random verdict (`LIABILITY`, `REJECTED`) onto the screen.
* **`ReportToHRButton`**: Return to Main Menu.

### **9. ASCII Cutscene Viewer**

* **`SceneCanvas`**: Animation engine. Renders JSON-defined frames at a specific framerate.
* **`SubtitleBox`**: Narrative text overlay.
* **`SkipPrompt`**: Input handler to bypass scene.

### **10. Codex / Encyclopedia**

* **`TopicList`**: Searchable index of Lore/Recipes.
* **`RedactedTextRenderer`**: Text engine. Renders clear text or `█████` blocks based on `Player.Knowledge` tags.

### **11. Settings**

* **`KeybindingMapper`**: Input config. Handles collisions by unbinding the conflicting key (forcing manual resolution).
* **`Audio/DisplayOptions`**: Standard sliders.

---
## Detailed UI Component Specification

### 1. Title & Main Menu

* **`GameLogo`**: Large, static ASCII art block displaying the game title.
* **`MainMenuOptions`**: Vertical selectable list (New Game, Settings, Quit).
* **`SaveSlotSelector`**: Modal displaying metadata for save files (Sector, Debt).
* **`NewsTicker`**: Scrolling single-line flavor text headlines at the bottom.
* **`VersionFooter`**: Static text displaying build number and copyright info.

#### `MainMenuOptions` (Screen 1)

**Specification:**

* **Role:** The primary navigation controller for the application entry point.
* **Visual Structure:**
* Vertical list centered on screen.
* **Active State:** `> [ TEXT ] <` (High contrast/Inverted colors).
* **Inactive State:** ` [ TEXT ] ` (Dimmed).
* **Disabled State:** ` [ TEXT ] ` (Dark Grey/Strikethrough).


* **Logic:**
* On mount, check `SaveManager` for existing run data.
* If `SaveManager.hasRun() == false`, disable "RESUME SHIFT".


* **Inputs:** `UP`/`DOWN` (Navigate), `ENTER` (Select).
* **Signals/Outputs:**
1. `NEW SHIFT` -> Triggers `SaveSlotSelector` (Mode: Create).
2. `RESUME SHIFT` -> Triggers `SaveSlotSelector` (Mode: Load).
3. `CODEX` -> Navigates to **Screen 9**.
4. `SETTINGS` -> Navigates to **Screen 10**.
5. `QUIT` -> Exits application.

#### `SaveSlotSelector` (Screen 1)

**Specification:**

* **Role:** Modal overlay for file management. Differentiates between starting fresh and resuming.
* **Visual Structure:**
* **Layout:** Three vertical panels (Slot 1, Slot 2, Slot 3).
* **Slot State - Empty:** Displays `[ VACANT POSITION ]` - `Open New File?`
* **Slot State - Occupied:**
* **Header:** "FILE #[ID]: [Name]"
* **Metadata:** `Sector: [Name]`, `Debt: -[Amount]`, `Playtime: HH:MM`.
* **Status:** "ACTIVE" (Alive) or "ARCHIVED" (Dead/Completed).

* **Logic:**
* **Mode: NEW SHIFT:**
* Select Empty -> Trigger **Screen 2 (Character Creation)**.
* Select Occupied -> Prompt "Overwrite Data? (Y/N)".

* **Mode: RESUME:**
* Select Occupied -> Load Run -> Go to **Screen 3 (Map)** or **Screen 4 (Shift)** depending on save state.
* Select Empty -> Disabled/Buzz.

* **Inputs:** `LEFT`/`RIGHT` (Select), `ENTER` (Confirm), `DELETE` (Erase Data), `ESC` (Cancel).

---

### 2. CHARACTER CREATION (New Employee Intake)

**Summary:** This screen represents the "Rehabilitation Intake Form." The player defines their specific Ogre's background and starting aptitudes before the first shift. 
wizard-style interface ("The Intake Pipeline") where the player builds their character step-by-step. The sequence of steps is determined by their Meta-Progression level.

**Components:**

* **`PipelineProgressIndicator`**: Top bar showing current step (e.g., "Step 2: Species Classification").
* **`CurrencyWallet`**: Dynamic header strip showing global meta-currencies (Gold, Soul Gems, Favor).
* **`NavigationControls`**: "Back" / "Next" buttons (Next is conditional on valid input).
* **`ModuleRenderer` (Left Panel)**: The polymorphic input form (Selectors, Sliders, Shops).
* **`ManifestProjection` (Right Panel)**: The live character sheet with "Diff" visualization.


#### `ModuleRenderer` (Screen 2)

**Specification:**

* **Role:** The polymorphic input container for the left 50% of the screen. It renders the specific "Form" for the current node in the creation pipeline.
* **Visual Structure:**
* **Header:** Node Title (e.g., "STEP 2: BIOLOGICAL CLASSIFICATION").
* **Description:** Flavor text describing the current choice context.
* **Input Area:** Dynamic widget rendering based on Node Type:
* *Selector:* Vertical list of Radio Buttons (Mutually Exclusive).
* *Allocator:* List of Sliders/Spinners (Point Pool).
* *Market:* Grid of Checkboxes with associated costs (Multi-Select).


* **Footer:** Navigation controls (Back/Next).


* **Logic:**
* **Input:** Receives `NodeConfig` (Options, Costs, Limits) and `GlobalProfile` (Wallet).
* **Validation:** Checks if `GlobalProfile` has sufficient currency for options. Disables "Next" if criteria (e.g., "Spend all points") are unmet.
* **Signaling:**
* `OnHover` -> Emits `PreviewDiff` signal to Right Panel.
* `OnSelect` -> Emits `UpdateDraft` signal to Game State.

#### `ManifestProjection` (Screen 2)

**Specification:**

* **Role:** The "Live Character Sheet" (Right Panel). It visualizes the current draft and provides real-time "Diff" feedback based on hover states in the Left Panel.
* **Visual Structure:**
* **Format:** ASCII "Dossier" or "Rap Sheet" with borders.
* **Sections:** Identity (Name, Race, BG), Attributes (Str, Int, Cha), Traits (Perks/Flaws), Inventory (Starting Gear).
* **Footer:** **Total Cost** (Sum of selections vs. Global Wallet).


* **Logic (The Ghost Layer):**
* **Base State:** Displays committed values in standard color (White/Grey).
* **Preview State:** On `PreviewDiff` signal (Hover):
* **Buffs:** Render value in **GREEN** with `+` (e.g., `STR: 10 [-> 12]`).
* **Nerfs:** Render value in **RED** with `-` (e.g., `CHA: 10 [-> 8]`).
* **additions:** Append new items/traits with `(+)` tag.

* **Inputs:** `CharacterDraft` (Current State), `GlobalProfile` (Currency checks).

---

### 3. Narrative Briefing

* **`BriefingHeader`**: Displays "Transfer Order" title or Sector Name.
* **`NarrativeTextBody`**: Scrollable text area containing story and lore.
* **`StampAnimation`**: Visual effect overlaying "APPROVED" or "URGENT" text.
* **`ObjectiveList`**: Bulleted list of quotas and goals for the sector.
* **`ContinueButton`**: Action prompt to acknowledge orders and begin.

#### `NarrativeTextBody` (Screen 3)

**Specification:**

* **Role:** The procedural "Storyteller" component. It generates a "Memo" or "Transfer Order" based on the upcoming sector's data.
* **Visual Structure:**
* **Header Block:** `TO: [Name] (ID: [ID])` | `FROM: HR (Sector [X])` | `SUBJECT: [Sector_Name]`.
* **Body:** Scrollable text area with typewriter effect.
* **Tone:** "Corporate Bureaucracy" meets "High Fantasy" (e.g., "Synergy with the Undead," "Q3 Soul Harvest Projections").


* **Logic (The Template Engine):**
* **Input:** `SectorData` (Biome, Culture, Boss Name, Hazards).
* **Process:** Selects a random template string and injects variables.
* **Flavor:** Randomly inserts "Corp-Speak" keywords.

* **Interaction:** Pressing any key speeds up the text crawl.

#### `ObjectiveList` (Screen 3)

**Specification:**

* **Role:** The "Mission Quota" display. It translates the abstract goals of the sector into concrete, trackable metrics.
* **Visual Structure:**
* **Format:** Bulleted list or Grid.
* **Entries:** `[ ] Goal Text (Progress: 0 / Target)`.
* **Difficulty Indicators:** Color-coded or Icon-tagged (e.g., 💀 for Hard/Optional).

* **Logic:**
* **Input:** `SectorConfig` (The rules/goals for the current node).
* **State:** Static preview (Values are 0).
* **Persistence:** This list is passed to the **Screen 5 (Bakery Shift)** Dashboard later.

---

### 4. Map / Traversal

* **`MetaStatsHeader`**: Persistent bar showing Debt, Gold, HP, and Shift.
* **`DungeonMapVisualizer`**: Branching node tree representing dungeon sectors (Slay the Spire style).
* **`NodeIcon`**: Visual marker for sector status (Locked, Visited, Boss).
* **`PlayerToken`**: Avatar indicating the player's current map position.
* **`TravelControls`**: Interface to select destination and pay travel costs.
* **`SectorDetailsPanel`**: Info panel for selected node (Resources, Threat Level).
* **`BossIntelDisplay`**: Tracks Boss approval rating and unlocked "Likes/Dislikes."


#### `DungeonMapVisualizer` (Screen 4)

**Specification:**

* **Role:** The primary interactive view for dungeon navigation. Renders a branching node graph (Bottom-to-Top orientation) using ASCII/NerdFont glyphs.
* **Visual Structure:**
* **Layout:** Vertical scrolling canvas.
* **Nodes:**
* *Current:* `[@]` (Player Token)
* *Available:* `[  ]` (Blinking/Highlighted)
* *Locked/Future:* `[  ]` (Dimmed)
* *Boss:* `[  ]` (Large Icon at top)
* *Unknown:* `[ ? ]` (Fog of War)

* **Edges:** ASCII connectors (`/`, `\`, `|`) linking ranks.

* **Logic:**
* **Input:** `DungeonGraph` (JSON structure).
* **Fog of War:** Ranks > `Current + 1` are obscured (Icon = `?`, Name = "Unknown").
* **Navigation:** Cursor-based inspection. Only connected nodes in the *immediate next rank* are valid travel targets.

####  `SectorDetailsPanel` (Screen 4)

**Specification:**

* **Role:** The "Inspector" panel. It displays tactical data for the currently selected Map Node to inform travel decisions.
* **Visual Structure:**
* **Header:** Sector Name & Biome (e.g., "The Fungal Caverns").
* **Vitals:**
* *Threat:* `[..]` (1-5 Scale).
* *Cost:* `-50g` (Travel Fee).

* **Intel:**
* *Dominant Culture:* (e.g., "Goblins").
* *Resource Yield:* (e.g., "High: Mushrooms", "Low: Flour").
* *Hazards:* (e.g., "Anti-Magic").

* **Logic:**
* **State:** Updates instantly on `CursorHover` over a map node.
* **Obfuscation:** If node is under "Fog of War" (Depth > 1), displays "NO DATA AVAILABLE."
* **Boss Link:** If the *Boss Node* is selected, displays a summary of the **BossIntelDisplay**.


#### `BossIntelDisplay` (Screen 4)

**Specification:**

* **Role:** The persistent "Dossier" on the Sector Boss. It tracks the player's progress in understanding and appeasing the sector's ruler.
* **Visual Structure:**
* **Portrait:** ASCII/NerdFont art. Hidden (`?`) until encountered/scouted.
* **Approval Bar:** Horizontal progress bar (0-100%).
* *Markers:* Visual indicators for "Pass/Fail" thresholds.


* **The Dossier:**
* *Likes:* List of revealed tags (e.g., `[Crunchy]`, `[Sweet]`).
* *Hates:* List of revealed tags (e.g., `[Holy]`, `[Spicy]`).


* **Tribute Log:** Scrollable history of items gifted and their effect (e.g., *"Rock Scone: -5% Approval"*).


* **Logic:**
* **Input:** `RunState.BossIntel` (Persistent across the sector).
* **Unlocks:** Bartering/Scouting reveals hidden Tags.
* **Feedback:** Sending tributes updates the Approval Bar and logs the result.

---

### 5. Bakery Shift (Main Game Loop)

* **`ShiftHeader`**: Top bar with real-time clock, gold, and buffs.
* **`DashboardNav`**: Tab bar to switch the main management view.
* **`DashboardViewport`**: Dynamic container rendering the active tab's content.
* **`NotificationLog`**: Scrolling feed of sales, system alerts, and chatter.
* **`CounterViewport`**: Live ASCII view of customer, counter, and patience.

#### `DashboardNav` (Screen 5)

**Proposed Design:**
This is the navigation bar for the management dashboard. It needs to clearly indicate which "Department" is currently active.

* **Role:** Controls the view of the main dashboard area.
* **Visual Structure:**
* **Layout:** Horizontal strip at the top of the dashboard area.
* **Tabs:**
* `[ OVERVIEW ]` (Active: Highlighted/Inverted)
* `[ RECIPES ]`
* `[ CONTRACTS ]`
* `[ STOCKS ]`
* `[ MERCHANT ]`
* `[ MARKET ]`
* `[ KITCHEN ]`
* `[ CHARACTER ]`
* `[ HISTORY ]`

* **Hotkeys:** Display small numbers (`1`-`9`) next to names for quick access.

* **Logic:**
* **Input:** `LEFT`/`RIGHT` (Cycle), `1-9` (Direct Select).
* **Output:** Emits `ChangeView(TabID)` signal to the **DashboardViewport**.
* **Alerts:** Displays small notification icons (e.g., `(!)`) on tabs requiring attention (e.g., "Low Stock" on Stocks tab).

#### `CounterViewport` (Screen 5)

**Specification:**

* **Role:** A passive visualizer for the automatic backend transactions. It adds flavor and feedback to the math happening in the background.
* **Visual Structure:**
* **Customer Sprite:** ASCII art of the patron (from `TransactionSummary.customerType`).
* **Action Log:** A dedicated area for the "receipt" of the last transaction.
* **Feedback Bubble:** Templated text based on result (e.g., "The Goblin grunts approvingly.").


* **Logic:**
* **Input:** `TransactionSummary` object (received from Backend).
* Contains: `CustomerType`, `ItemSold`, `GoldEarned`, `ReputationChange`, `FlavorText`.


* **Process:**
1. **Queue Animation:** Customer enters -> Item appears -> Customer eats.
2. **Display Feedback:** Show `FlavorText` in speech bubble.
3. **Update Stats:** Float `+5g` or `+XP` markers visually.

* **State:** Idle until a new `TransactionSummary` arrives.

#### `OverviewTab` (Screen 5)

**Specification:**

* **Role:** The "Executive Dashboard." Aggregates critical status alerts from all other departments into a single view.
* **Visual Structure:**
* **Financial Summary:** `Current Gold`, `Projected Daily Revenue`, `Next Rent Due` (Countdown).
* **Production Monitor:** Condensed status lines for appliances (e.g., `[OVEN 1: IDLE]`, `[CROCK 2: 50%]`).
* **Inventory Alerts:** Warnings for "Critical Low" ingredients.
* **Reputation/Heat Map:** Current Global Frustration level and Dominant Customer Demographic.


* **Logic:**
* **Read-Only:** Primarily for display.
* **Hotlinks:** Pressing `ENTER` on an alert jumps to the relevant tab (e.g., Low Flour -> `StocksTab`).


#### `RecipesTab` (Screen 5)

**Specification:**

* **Role:** The R&D interface. Allows the player to design new products by combining Base types with specific Ingredients.
* **Visual Structure:**
* **Left Panel (Template List):** Scrollable list of unlocked Bases (e.g., Bread, Ale). Includes "Create New" option.
* **Right Panel (The Designer):**
* **Header:** Recipe Name (Auto-generated procedural text).
* **Slot Interface:** Dynamic list of required slots for the selected Base.
* *Interaction:* Selection opens an Ingredient Picker Modal filtered by interface type (e.g., `Liquid`).


* **Stats Rendering Area (Flavor Profile):**
* *Continuous Attributes:* Horizontal Bar Graphs for values defined in YAML (e.g., `[Salt Icon] Salty: ||||||....`).
* *Boolean Tags:* Icon + Text badges for binary states (e.g., `[Crunchy Icon] Crunchy`, `[Holy Icon] Holy`).
* *Cost:* Sum of ingredient costs.
* *Projected Appeal:* "Goblins: HIGH / Elves: LOW".


* **Action Bar:** `[ SAVE ]` / `[ DISCARD ]`.


* **Logic:**
* **Data-Driven:** All stats/tags are loaded from external JSON/YAML definitions (Icon, Color, Name).
* **Auto-Naming:** Generates names based on the Rarity tier of ingredients used.
* **Validation:** Prevents saving if essential slots are empty.


#### `ContractsTab` (Screen 5)

**Specification:**

* **Role:** The "Futures Market" interface. Displays available and active obligations with a focus on risk/reward assessment.
* **Visual Structure:**
* **Layout:** Split vertically into two sections: **SIGNED OBLIGATIONS** (Top) and **OPEN MARKET** (Bottom).
* **Contract Row (The Card):**
* **Header:** Contract Title & Requirement (e.g., "Order #404: Supply 50x 'Spicy' Loaves").
* **Outcome Split (The "Fine Print"):**
* *Success (Left):* `[+] 500g`, `[+] Guild Favor`, `[?]` (Hidden Bonus).
* *Failure (Right):* `[-] 200g`, `[-] Broken Kneecaps`, `[?]` (Hidden Penalty).

* **Progress Bar (Active Only):** `[|||||||......] (35/50 Delivered)` | `Deadline: 2 Days`.

* **Logic:**
* **State:**
* *Available:* No Progress Bar. Action: `[ SIGN ]`.
* *Active:* Has Progress Bar. Action: None (Auto-updates).

* **Obfuscation:** Renders `[?]` or `[REDACTED]` for specific rewards/penalties based on the player's `Legal` or `Intel` stats.


#### `StocksTab` (Screen 5)

**Specification:**

* **Role:** The Inventory Database Viewer. It aggregates individual item instances into high-level categories with a two-stage drill-down capability.
* **Visual Structure:**
* **Level 0 (Main Aggregator):**
* **Format:** Sortable Data Table.
* **Columns:** `Item Name` | `Total Qty` | `Status Breakdown` (e.g., "5 Fresh, 2 Stale").
* **Logic:** Aggregates SQL count results based on Item Type ID.

* **Level 1 (Batch Modal):** *Triggered by selecting an Item Type.*
* **Header:** "[Item Name] Manifest".
* **List:** Rows representing individual database entries (instances).
* **Columns:** `Instance ID` | `Age/Timestamp` | `Current Tags` (Fresh/Stale).

* **Level 2 (Instance Inspector Modal):** *Triggered by selecting a specific Instance.*
* **Header:** "Item #[ID] Details".
* **Body:** Full render of the specific item's YAML attributes (Flavor Profile, Texture, Expiration Date).

* **Logic:**
* **Data Source:** SQLite queries.
* **Tagging:** Relies on backend logic to compute state (Fresh/Rotten) before display.
* **Rendering:** Uses the standard Attribute/Tag icon system for all stats.


#### `MerchantTab` (Screen 5)

**Specification:**

* **Role:** The "Front of House" Storefront Manager. Assigns specific inventory items (Baked Goods or Ingredients) to physical shelf slots and sets their "Sticker Price."
* **Visual Structure:**
* **Inventory Source (Left Panel):** Scrollable list of `Stocks` (Ingredients & Finished Goods).
* **The Shelves (Center/Right Panel):** A dynamic Grid of Slots.
* *Capacity:* Determined by `ShopUpgrades.ShelfSpace` (starts small, expands).
* *Slot State:*
* **Empty:** `[ VACANT SHELF ]`
* **Occupied:** `[Icon] Item Name (Qty: X) @ [Price]g`.

* **Pricing Control (Overlay/Panel):**
* **Input:** `Base Ask Price` (Effective Gold).
* **Unlockable Analytics:**
* *Demand Curve:* Graph showing Price vs. Sales Volume. (Hidden if `MarketResearch < 1`).
* *Customer Match:* Icons of target demographics (e.g., Peasants, Nobles). (Hidden if `MarketResearch < 2`).

* **Logic:**
* **Assignment:** Moves items from `Stocks` (Warehouse) to `Shelves` (Sales Floor).
* **Pricing:** Sets the visual price tag. (Note: Actual transactions use this as a baseline for Gold or Barter value).
* **Conditional Rendering:** Analytics widgets are present but hidden/disabled until specific upgrades are purchased in the `MarketTab`.

#### `MarketTab` (Screen 5)

**Core Mechanics:**

1. **The Ontology:** A massive, hierarchical database of every item in the game (e.g., `Liquid > Milk > Rat Milk`).
2. **Barter Logic (Inbound):** You define "Buy Orders." You set multipliers for items you want to acquire from customers (e.g., "I accept `[Category: Milk]` at 200% value").
3. **Targeted Pricing (Outbound):** You define "Sell Rules" based on Customer Identity tags. (e.g., "Sell `Sweet Tarts` to `[Tag: Human]` at 50% price").
4. **The Goal:** Strategic pricing manipulates **Global Reputation**. Giving a "Good Deal" to a specific demographic boosts your standing with *all* their associated tags (Race, Job, Religion).
5. 
**Specification:**

* **Role:** The High-Frequency Trading Terminal. Allows the player to browse the global item hierarchy and set granular automated trade rules to farm resources and reputation.
* **Visual Structure:**
* **Filter/Search Bar (Top):**
* *Text Input:* fuzzy search (e.g., "Milk").
* *Tag Toggles:* `[Raw]`, `[Baked]`, `[Magical]`.

* **Ontology Tree (Left Panel):**
* *Format:* Collapsible directory tree.
* *Nodes:* `[+] Liquid` -> `[+] Milk` -> `Rat Milk (Base Value: 5g)`.
* *Indicators:* Visual markers for categories with active custom rules.

* **Trade Rule Editor (Right Panel):** *Active when a Node (Category or Item) is selected.*
* **Header:** Item/Category Name & Market Base Price.
* **Inbound Settings (Barter/Buying):**
* *Control:* "Acquisition Multiplier" (Slider/Input).
* *Example:* "We accept this item at [ 2.0x ] Market Value."

* **Outbound Settings (Selling/Discounts):**
* *Target Selector:* Dropdown of known Entity Tags (e.g., `Human`, `Miner`, `Morgoth`).
* *Control:* "Price Multiplier" (Slider/Input).
* *Example:* "For [ Human ], price is [ 0.5x ]."

* **Projected Impact:**
* *Reputation:* `[ Human: ++ ]`, `[ Miner: ++ ]`.
* *Profit:* `[ Low Margin ]`.

* **Logic:**
* **Inheritance:** Rules set on a Parent Node (e.g., "Milk") apply to all Children (e.g., "Rat Milk") unless manually overridden.
* **Data Source:** Parses the massive Item/Entity YAML definitions.
* **Unlock State:** Advanced filtering or specific demographic targeting may be hidden if the Meta-Progression (Prestige) level is too low.


#### `KitchenTab` (Screen 5)

**Specification:**

* **Role:** The Production Floor. Manages appliances and crafting queues.
* **Visual Structure:**
* **Appliance Grid:** List of hardware (e.g., `[ Stone Oven ]`, `[ Iron Pot ]`).
* *Status:* `[ IDLE ]`, `[ COOKING ]`, `[ CLEANING ]`.
* *Progress:* ASCII Progress Bar `[|||||.....]`.


* **Job Queue (Per Appliance):**
* *Slots:* List of recipes waiting to be baked.
* *Controls:* `[ + Add Job ]` (Opens Recipe Picker), `[ Cancel ]`, `[ Rush ]` (Cost: Stress).

* **Logic:**
* **Input:** Recipes selected from the database.
* **Process:** Tick-based timer.
* **Output:** Finished goods move to `StocksTab` database with `Fresh` tag.

#### `CharacterTab` (Screen 5)

**Specification:**

* **Role:** The RPG Management Screen. Reuses the visual language of the Character Creator to manage the Ogre's personal equipment and stats.
* **Visual Structure:** Three-Column Layout.
* **Column 1: Personal Inventory (The Bag):**
* Scrollable list of items currently carried by the Ogre (distinct from Bakery Stocks).
* *Context:* Weapons, Clothing, Magical Trinkets.


* **Column 2: The Paper Doll (Equipment):**
* Vertical arrangement of slots: `[ HEAD ]`, `[ BODY ]`, `[ MAIN HAND ]`, `[ OFF HAND ]`, `[ ACCESSORY ]`.
* *State:* Empty slots show placeholder; Filled slots show Item Name.


* **Column 3: Status & Stats (The Reuse):**
* **Top:** **Active Effects List** (New). Live tracker of buffs/debuffs with countdowns (e.g., `[ Caffeine Rush: 4m ]`).
* **Bottom:** **`ManifestProjection`** (Reused from Screen 2). Displays the full stat block.

* **Logic:**
* **Interaction:** Selecting an item in Inventory and hovering a Paper Doll slot triggers the **Diff System**.
* **Diff Visualization:** The `ManifestProjection` renders potential changes in **GREEN** (Upgrade) or **RED** (Downgrade) just like in Character Creation.
* **Equip/Unequip:** Updates the `CurrentCharacterState` and recalculates derived stats.


#### `CharacterTab` (Screen 5)

**Specification:**

* **Role:** The RPG Management Interface.
* **Visual Structure:** Three-Column Layout.
* **Column 1: Personal Inventory:** Scrollable list of *Equippable Items* (distinct from Bakery Stocks).
* **Column 2: The Paper Doll:**
* Slots: `[HEAD]`, `[BODY]`, `[HAND_1]`, `[HAND_2]`, `[ACC]`.
* *Interaction:* Drag-and-drop or Select-to-Equip.


* **Column 3: Status & Stats:**
* **Top:** **Active Effects** (Buffs/Debuffs with timers).
* **Bottom:** **`ManifestProjection`** (Reused from Screen 2).

* **Logic:**
* **Reuse:** Implements the same **Diff Visualization** logic as Character Creation. Hovering an item in the Inventory shows stat changes (Green/Red) on the `ManifestProjection` before equipping.
* **State:** Modifications here update the global `CharacterInstance`.

#### `HistoryTab` (Screen 5)

**Specification:**

* **Role:** The Session Log. A persistent record of events for review/debugging.
* **Visual Structure:**
* **Filters:** `[ALL]`, `[SALES]`, `[COMBAT]`, `[SYSTEM]`.
* **List:** Timestamped text entries.

* **Logic:**
* **Input:** Appends `LogEntry` objects from the backend event bus.
* **Format:** `[HH:MM] [TYPE] Message string`.


### 6. Crisis Encounter
**Context:** High-stress, time-sensitive trivia minigame. The UX must induce panic but remain responsive.

* **`EncounterHeader`**: Static text labels (Name, Level, Title).
* **`EnemyPortrait`**: Standard ASCII fetch based on Entity ID.
* **`QuestionDisplay`**: Read-only text wrapper.
* **`AnswerList**
* **`RageMeter`**
* **`CustomerActionLog`**

#### **Component: `AnswerList` (Screen 6)**

**Specification:**

* **Role:** The primary interactive element of the Crisis Encounter. A scrollable list of text options designed to create friction and panic through sheer volume and visual density.
* **Visual Structure:**
* **Layout:** Vertical stack occupying the center 60% of the screen.
* **Density:** Tight line spacing. No dividers between items.
* **Selection Cursor:** `> [ TEXT ] <` (High Contrast / Inverted Background).
* **Scroll Indicator:** ASCII scrollbar on the right edge (e.g., `|#|` moving down a track `| |`).
* **Viewport:** Shows only 8-10 items at a time. The player *must* scroll to see the rest.

* **Logic:**
* **Inputs:** `UP` / `DOWN` (Navigate one item), `HELD UP/DOWN` (Fast Scroll), `ENTER` (Commit).
* **Behavior:**
* **No Wrapping:** Reaching the bottom does *not* loop to the top. The player must physically scroll back up.
* **Randomized Start:** The cursor does *not* start at the top. It starts at a random index, forcing orientation.

* **Content Generation (The "Bureaucracy" Algorithm):**
* **Base Pool:** 20 Items.
* **Modifier:** `Player.Knowledge[Topic]` (0-3).
* **Reduction Formula:** `Count = 20 - (Knowledge * 5)`. (Min 5 items).
* **Distractor Engine:** Fetches "False" answers that share the *exact same* syntax and keywords as the correct answer (e.g., if the answer is "Regulation 4B", distractors are "Regulation 4A", "Regulation 4C", "Regulation 14B").

* **Outcome:**
* *Correct:* Emits `EncounterSuccess` signal.
* *Incorrect:* Emits `EncounterStrike` signal.
* *Time Out:* Treated as Incorrect.

#### **Component: `RageMeter` (Screen 6)**

**Specification:**

* **Role:** The singular resource for the encounter. It combines the functions of a Time Limit and a Health Bar into a "Sanity" gauge.
* **Visual Structure:**
* **Location:** Prominent horizontal bar at the top or bottom of the screen.
* **Style:**
* *Low Rage (0-30%):* `[====....................]` (Green/White)
* *Medium Rage (30-70%):* `[########................]` (Yellow)
* *High Rage (70-99%):* `[!!!!!!!!!!!!!!!!!!!!....]` (Red/Blinking)
* *Critical (100%):* `[########################]` (Explosion Animation)

* **Labels:** "COMPOSURE" or "SELF-CONTROL".


* **Logic:**
* **Passive Gain (The "Tension"):** Increases by `X` per second (Tick rate). Represents the sheer annoyance of the interaction.
* **Spike Gain (The "Abuse"):**
* *Wrong Answer:* `+20% Rage`.
* *Enemy Attack/Theft:* `+15% Rage` (Triggered by RNG events during the question).

* **Reduction (The "Coping"):**
* *Correct Answer:* `-15% Rage` (A moment of relief).

* **Failure State:** If `Rage >= 100%`, trigger `GameOver` (Scenario: "You brained the customer with a baguette").

#### **Component: `CustomerActionLog` (Screen 6)**

**Specification:**

* **Role:** Displays the "Attacks" (annoyances) happening in real-time while the player tries to read the answers.
* **Visual Structure:**
* **Location:** Small text area near the `EnemyPortrait`.
* **Format:** Scrolling log of status messages.
* **Tone:** Passive-aggressive dungeon interactions.
* *Example:* "The Goblin spits on the counter." (`+Rage`)
* *Example:* "The Karen-Lich demands to see the manager." (`+Rage`)
* *Example:* "The Adventurer tries to steal the tip jar." (`+Rage`)

* **Logic:**
* **Trigger:** Random interval based on `EnemyAgitationLevel`.
* **Effect:** Sends `AddRage(Amount)` signal to the `RageMeter`.

### **SCREEN 7: HR / SETTLEMENT (Meta-Game)**

**Context:** The "End of Run" summary. This is where the player sees the financial consequences of their shift and buys permanent upgrades.

* **`SettlementInvoice`**: A standard itemized list (Revenue, Taxes, Fees, Net Profit).
* **`NextAssignmentButton`**: Standard "Continue" action.
* **`DebtVisualizer`**: Large, animated counter tracking Total Cumulative Debt.
* **`PerformanceReview`**: XP calculation based on compliance and speed metrics.
* **`UpgradeTreeRenderer`**: Reusable tree component for purchasing permanent skills/upgrades.

#### **Component: `UpgradeTreeRenderer` (Screen 7)**

**Specification:**

* **Role:** The progression interface. Allows the player to spend "Compliance Points" (XP) or Gold on permanent stat boosts and unlockables.
* **Visual Structure:**
* **Layout:** Two-column "Split Pane" design (resembling a Windows 95 file explorer).
* **Left Panel (The Directory):**
* **Format:** Collapsible Tree List (`[+]` / `[-]`).
* **Root Categories:** Drawn from Data (e.g., `[+] CULTURAL_SENSITIVITY`, `[+] FLAVOR_THEORY`, `[+] DISPUTE_RESOLUTION`).
* **Leaf Nodes:** Individual Certificates.
* *Locked:* `[ ] Module 101: Intro to Goblins (Req: Lvl 1)` (Dimmed).
* *Available:* `[ ] Module 102: Goblin Gift Theory` (Bright/White).
* *Certified:* `[x] Module 101: Intro to Goblins` (Green/Strike-through).

* **Right Panel (The Syllabus):**
* **Header:** "CERTIFICATE OF COMPLETION: [Selected Node Name]".
* **Body:**
* *Abstract:* Flavor text describing the training (e.g., *"Learn to distinguish between a grimace of pain and a smile of gratitude."*).
* *Effect:* Technical description (e.g., *"Reduces Rage gain from Goblin customers by 15%."*).
* *Cost:* `[ XP: 500 ]` or `[ Gold: 150 ]`.

* **Action:** `[ ENROLL ]` Button (Active only if affordable and unlocked).

* **Logic:**
* **Data Source:** Parses the global `Upgrades.yaml` file.
* **Dependency Check:** Purchasing a node unlocks its children in the tree.
* **Currency:** Deducts from `Player.XP` (Compliance) or `Player.Gold` (Tuition).
* **State Update:** Emits `UpgradeUnlocked(ID)` which modifies the persistent `SaveFile`.

#### **Component: `DebtTicker` (Screen 7)**

**Specification:**

* **Role:** The "High Score" and the central antagonist. It visualizes the futility of the player's labor.
* **Visual Structure:**
* **Location:** Top Center, Large Font.
* **Format:** `OUTSTANDING BALANCE: [ 9,999,999 G ]` (Red Text).
* **Animation Sequence (On Load):**
1. **Interest Accrual:** The number *increases* rapidly (`+ 5% Daily Compound`). *Sound: Ticking up.*
2. **Garnishment:** A chunk is removed (`- Payment`). *Sound: Heavy Thud.*
3. **Net Result:** The number settles. (Usually barely lower, or higher than before).

* **Tooltip:** Hovering reveals the breakdown (Principal, Interest, Fees, Fines).

* **Logic:**
* **Input:** `RunResult.NetProfit`, `Global.TotalDebt`.
* **Calculation:** `NewDebt = (OldDebt * InterestRate) - (NetProfit * GarnishmentRate)`.
* **GameOver Condition:** If `Debt > DebtLimit` (optional mode) or `Debt <= 0` (Victory).


### **SCREEN 8: INCIDENT REPORT (Game Over)**

**Context:** The player has "Brained" a customer (Rage 100%) or died. This is the death screen.

* **`IncidentHeader`**: "EMPLOYMENT TERMINATED" banner.
* **`ReportToHRButton`**: "Process Separation Paperwork" (Restart/Menu).
* **`ViolationLog`**: We need a procedural text generator that describes *exactly* what happened in "HR Speak."
* **`SentencingStamp`**: The visual flair. A literal stamp animation slamming onto the report.
* **`SessionMetrics`**: Stats summary for the failed run only.

#### **Component: `ViolationLog` (Screen 8)**

**Specification:**

* **Role:** The procedural "Cause of Death" generator. It recontextualizes the player's violent outburst or failure into dry, litigious HR jargon.
* **Visual Structure:**
* **Format:** A typewriter-style text block within a "Notice of Termination" form.
* **Style:** `[ ERROR: 0xDEAD ]` - Red monospaced font.

* **Logic:**
* **Input:** `RunState.EndReason` (e.g., `Violence`, `Theft`, `Incompetence`), `RunState.LastTarget` (Enemy ID), `RunState.HeldItem` (Weapon).
* **Data Source:** `Violations.yaml`.
* **Template Injection:**
* *Pattern:* `"{ComplianceCode}: {Subject} initiated {ActionVerb} regarding {Victim} utilizing {Tool}."`
* *Example (Violence):* "Violation 404: Employee initiated *unauthorized percussive maintenance* regarding *Grand Matriarch (Elf)* utilizing *Stale Baguette*."
* *Example (Incompetence):* "Violation 500: Employee failed to maintain *minimum thermodynamic standards* resulting in *Catastrophic Scone Fusion*."

#### **Component: `SentencingStamp` (Screen 8)**

**Specification:**

* **Role:** The visual punctuation of the Game Over screen.
* **Visual Structure:**
* **Graphic:** ASCII Art box with heavy borders.
* **Text:** Randomly selected from a pool: `[ TERMINATED ]`, `[ LIABILITY ]`, `[ REJECTED ]`.
* **Animation:**
1. **Scale:** Starts 2x size (invisible).
2. **Drop:** Shrinks rapidly to 1x.
3. **Impact:** Screen shake effect + "Dust" particles (ASCII `.` and `,` scattering).
4. **Color:** Stamp turns Deep Red on impact.

#### **Component: `SessionMetrics` (Screen 8)**
the "Event Sourcing" pattern.

##### 1. The Philosophy: "The Paper Trail"

**The Problem:** Spaghetti code happens when you have global variables like `run_stats.goblins_served` and try to increment them from 50 different scripts.
**The Solution:** **Don't count. Just log.**
We create a write-only `SessionLog` table. Every time *anything* happens, we insert a row. When the run ends, we run SQL queries to generate the report.

---

##### 2. Database Schema (The Log)

We add one high-throughput table to our SQLite architecture.

**Table: `SessionLog**`
*Records the "Tick-by-Tick" history of the shift.*

```sql
CREATE TABLE SessionLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tick INTEGER,           -- The game time (Turn/Second)
    event_type TEXT,        -- The broad category ('TRANSACTION', 'COOK', 'VIOLENCE')
    event_subtype TEXT,     -- Specific action ('SALE', 'THEFT', 'BRAINING')
    
    -- The Actors
    actor_id TEXT,          -- Who did it? ('player', 'goblin_04')
    target_id TEXT,         -- To whom? ('customer_05', 'donut_99')
    
    -- The Quantities
    value_primary REAL,     -- Main metric (Gold amount, Rage % added)
    value_secondary REAL,   -- Side metric (Reputation change, Item Quality score)
    
    -- The Context (Critical for filtering)
    tags_snapshot TEXT      -- JSON string of relevant tags at that moment
                            -- e.g., "{'customer_race': 'goblin', 'item_tag': 'sacred'}"
);

```

---

##### 3. The Implementation (The "Firehose")

**The Logger Service (Python)**

Instead of injecting a `MetricsManager` into every class, we use a static/global **Event Bus**.

```python
class GameLogger:
    @staticmethod
    def log(event_type: str, subtype: str, value: float, **kwargs):
        """
        Fire-and-forget method.
        Constructs the SQL INSERT statement and sends it to the DB queue.
        """
        cursor.execute("""
            INSERT INTO SessionLog (tick, event_type, event_subtype, value_primary, tags_snapshot)
            VALUES (?, ?, ?, ?, ?)
        """, (
            Game.current_tick, 
            event_type, 
            subtype, 
            value, 
            json.dumps(kwargs) # Context tags
        ))

```

**Usage Examples (No Spaghetti)**

* **In `MerchantSystem.py`:**
```python
# Logic handles the trade...
GameLogger.log(
    event_type="TRANSACTION", 
    subtype="SALE", 
    value=50, # Gold
    customer_race="elf", 
    item_id="croissant"
)

```


* **In `CrisisSystem.py`:**
```python
# Player gets a question wrong...
GameLogger.log(
    event_type="COMPLIANCE", 
    subtype="VIOLATION", 
    value=15, # Rage added
    decree_id="morgoth_04"
)

```



---

##### 4. The Aggregation (The "End of Run" Report)

When the player finishes a shift (or dies), the `SessionMetrics` component instantiates. It runs these **ReadOnly SQL Queries** to build the display data.

###### A. Financials (The Audit)

* **Gross Revenue:**
`SELECT SUM(value_primary) FROM SessionLog WHERE event_subtype = 'SALE'`
* **Losses (Theft/Refunds):**
`SELECT SUM(value_primary) FROM SessionLog WHERE event_subtype IN ('THEFT', 'REFUND')`
* **Tip Rate:**
`SELECT AVG(value_primary) FROM SessionLog WHERE event_subtype = 'TIP'`

###### B. Operations (The Grind)

* **Throughput:**
`SELECT COUNT(*) FROM SessionLog WHERE event_subtype = 'SALE'`
* **Quality Control (Avg. Donut Quality):**
`SELECT AVG(value_secondary) FROM SessionLog WHERE event_type = 'COOK' AND event_subtype = 'FINISH'`

###### C. Demographics (The "Bureaucracy")

* **Most Frequent Customer:**
```sql
SELECT json_extract(tags_snapshot, '$.customer_race') as race, COUNT(*) as count
FROM SessionLog 
WHERE event_type = 'TRANSACTION'
GROUP BY race 
ORDER BY count DESC LIMIT 1

```


* **Racial Satisfaction Gap:**
*Compare AVG(Satisfaction) of Goblins vs. Elves to see who hates you.*

---

##### 5. The UI Component: `SessionMetrics`

This component renders the results of the queries above. It uses the "End of Shift Report" aesthetic.

**Visual Structure:**

```text
+-------------------------------------------------------+
|  SHIFT PERFORMANCE REVIEW - SECTOR 7G                 |
+-------------------------------------------------------+
|  [ FINANCIALS ]                                       |
|  > Gross Revenue:      1,250 G                        |
|  > Inventory Shrink:     -40 G  (Theft: 2)            |
|  > Net Profit:         1,210 G                        |
|                                                       |
|  [ OPERATIONS ]                                       |
|  > Customers Served:      42                          |
|  > Avg. Wait Time:       14s  (Target: 10s) [FAIL]    |
|  > Most Sold Item:       "Sludge Tart" (Qty: 18)      |
|                                                       |
|  [ COMPLIANCE ]                                       |
|  > Decrees Violated:       1  (Morgoth's 4th Law)     |
|  > Rage Spikes:            3                          |
|  > Braining Incidents:     0  [PASS]                  |
+-------------------------------------------------------+
|  RATING:  B-  (ADEQUATE)                              |
+-------------------------------------------------------+

```

### Logic Class: `ReportGenerator`

```python
class ReportGenerator:
    def generate(self) -> dict:
        return {
            "revenue": self._query_revenue(),
            "shrink": self._query_shrink(),
            "top_item": self._query_top_item(),
            "compliance_score": self._calculate_grade()
        }

    def _calculate_grade(self):
        # Complex logic lives here, not in the game loop.
        # e.g., Grade = (Revenue / Target) - (Violations * 10)
        pass

```


### **SCREEN 9: ASCII CUTSCENE VIEWER**

**Context:** Used for the Intro, Major Boss Interactions, and Endings.

* **`SubtitleBox`**: Bottom-aligned text overlay.
* **`SkipPrompt`**: Standard "Hold [Space] to Skip".
* **`SceneCanvas`**: This is the engine. It needs to render a sequence of ASCII frames at a specific framerate.

#### **Component: `SceneCanvas` (Screen 9)**

**Specification:**
* **Role:** The cinematic player. Renders sequences of ASCII art frames to tell the story.
* **Visual Structure:**
* **Viewport:** Fixed aspect ratio (e.g., 80x25 chars).
* **Render Layer:** Pre (space) formatted text block.


* **Logic:**
* **Input:** `SceneID` (e.g., `Intro_01`).
* **Data Source:** `Scenes.json`.
* *Structure:*
```json
{
  "id": "Intro_01",
  "framerate": 12,
  "frames": [
    "String_Frame_1",
    "String_Frame_2"
  ],
  "audio_cues": [ { "frame": 10, "sfx": "crash" } ]
}

```

* **Playback Engine:**
* Uses a `requestAnimationFrame` loop or `setInterval` matching the JSON `framerate`.
* Updates the `innerText` of the container every tick.
* **Optimization:** Only re-renders characters that changed (Diffing) OR brute-force replaces the whole block (likely fine for text).

### **SCREEN 10: CODEX (The Archive)**

**Context:** The repository of all discovered lore, recipes, and entities. It serves as the player's progress tracker for "Cultural Competency."

#### **Component: `RedactedTextRenderer` (Screen 10)**

**Specification:**

* **Role:** The dynamic text engine that obfuscates information the player acts "not cleared" to know. It visually reinforces the theme of clearance levels and bureaucratic compartmentalization.
* **Visual Structure:**
* **Clear Text:** Standard font (White/Grey).
* **Redacted Text:**
* *Style A (Hard Redaction):* Solid blocks `████████` (Dark Grey).
* *Style B (Soft Redaction):* `[ REDACTED ]` or `[ CLEARANCE REQUIRED ]` (Red).
* *Style C (Glitch):* Garbled characters `k#^&@!aa` (fluctuating).

* **Logic:**
* **Input:** `LoreEntry` object (from YAML) + `Player.KnowledgeProfile`.
* **Markup Parsing:** The raw text contains tags defining knowledge thresholds.
* *Source:* `"The Great Baker used <tag:morgoth_lvl_2>blood</tag> in the dough."`

* **Evaluation:**
* *Check:* `if (Player.Knowledge['morgoth'] >= 2)` -> Render "blood".
* *Else:* -> Render `█████`.

* **Progress Tracking:** Calculates `% Revealed` for the completion bar based on the ratio of clear vs. redacted characters.

### **SCREEN 11: SETTINGS (Control Panel)**

**Context:** Functional configuration. Kept utilitarian.

#### **Component: `KeybindingMapper` (Screen 11)**

**Specification:**

* **Role:** Allows remapping of the keyboard-centric control scheme. Handles input collisions.
* **Visual Structure:**
* **Layout:** Two-column table.
* *Left:* **Action** (e.g., `[ NAVIGATE UP ]`, `[ INTERACT ]`).
* *Right:* **Key** (e.g., `[ W ]`, `[ SPACE ]`).

* **State Indicators:**
* *Active:* `> [ W ] <` (Blinking).
* *Conflict:* `[ ! ] [ W ]` (Red/Warning).

* **Logic:**
* **Input:** Listens for the *next* keypress when a slot is selected.
* **Validation (The "Bureaucracy"):**
* *Check:* Is the new key already bound to another action?
* *Conflict Resolution:*
* *Option A (Swap):* Automatically swaps the keys.
* *Option B (Unbind):* Unbinds the *old* action, leaving it empty (requiring attention).
* *Decision:* **Option B**. It forces the user to manually resolve the "paperwork" error.

* **Persistence:** Saves to `user_settings.json` immediately on change.


