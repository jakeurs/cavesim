# Technical Design Specification: Bread & Bureaucracy

---

## 1. High-Level Architecture

The game operates on a **Data-Driven Pipeline**. The engine (C#/Python) is a generic processor that ingests "Bureaucracy" (Data) to create Gameplay.

### The Pipeline

1. **Source of Truth (Static Data):** Large, hand-authored (or LLM-generated) JSON/YAML files define the universe (Ingredients, Decrees, Monster Prefabs).
2. **Ingestion (Load Time):** The game parses Static Data and hydrates an in-memory **SQLite** database.
3. **Runtime State (The ECS):** Game objects (Entities) are rows in SQLite tables. Logic queries SQL to find "all items with `tag:flammable`" or "current gold count."
4. **Persistence (Save/Load):** The active SQLite tables are dumped to a `save.db` file.

---

## 2. Database Schema (SQLite)

We utilize a hybrid **Entity-Attribute-Value (EAV)** model to allow for infinite flexibility without altering the schema.

### A. The Entity Index

Who exists in the current sector?

```sql
CREATE TABLE WorldInstances (
    instance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    definition_id TEXT,  -- Link to Static Data (e.g., 'goblin_grunt_01')
    entity_type TEXT,    -- 'ITEM', 'ACTOR', 'PROJECTILE'
    name TEXT,           -- Procedural Name (e.g., "Morgoth-Blessed Scone")
    location_id TEXT     -- 'player_inventory', 'shelf_slot_4'
);

```

### B. The Component Tables

**1. Stats (Continuous Capabilities)**
Defines *effectiveness* (e.g., Flavor Intensity, Strength).

```sql
CREATE TABLE InstanceStats (
    instance_id INTEGER,
    stat_id TEXT,        -- 'flavor_bitter', 'durability'
    base_value REAL,
    FOREIGN KEY(instance_id) REFERENCES WorldInstances(instance_id)
);

```

**2. Tags (Boolean Identity)**
Defines *nature* (e.g., Is it Holy? Is it raw?).

```sql
CREATE TABLE InstanceTags (
    instance_id INTEGER,
    tag_id TEXT,         -- 'blessed_by_morgoth', 'texture_crunchy'
    FOREIGN KEY(instance_id) REFERENCES WorldInstances(instance_id)
);

```

**3. Resources (Transactional State)**
Defines *quantities* (e.g., Health, Gold, Stress).

```sql
CREATE TABLE InstanceResources (
    instance_id INTEGER,
    resource_id TEXT,    -- 'hp', 'gold', 'stress'
    current_value REAL,
    max_value REAL,
    FOREIGN KEY(instance_id) REFERENCES WorldInstances(instance_id)
);

```

**4. Composition (The Nesting)**
Links ingredients to the final product.

```sql
CREATE TABLE CompositeComponents (
    parent_instance_id INTEGER, -- The Donut
    child_instance_id INTEGER,  -- The Pickle inside
    slot_id TEXT                -- 'filling_slot'
);

```

---

## 3. The Ontology (YAML Schemas)

The complexity of the game is authored here.

### A. Material Science (`materials.yaml`)

Defines how matter transforms. This is a **State Machine**.

```yaml
murder_grub_kidney:
  type: ingredient
  state: raw
  # Base Properties
  tags: [organ, meat, texture_hard]
  stats: { flavor_bitter: 10 }
  
  # The State Transitions
  transforms:
    process_pickle: "kidney_pickled"      # Becomes new Item ID
    process_fry: "kidney_burnt"           # Fail state
    process_boil: "generic_mush"          # Default fail state

```

### B. Tag Inheritance Policies (`tags.yaml`)

Defines what survives a transition.

```yaml
tag_categories:
  texture: { policy: "overwrite" } # Pickling replaces 'Hard' with 'Crunchy'
  flavor:  { policy: "mix" }       # Sauce blends flavors
  sacred:  { policy: "preserve" }  # 'Blessed' tags survive cooking (Heirloom)
  state:   { policy: "remove" }    # 'Raw' tag is deleted upon cooking

```

### C. The Decree System (`decrees.yaml`)

The "Single Source of Truth" for Logic and Trivia.

```yaml
decree_morgoth_04:
  # Scope
  target_tag: "blessed_by_morgoth"
  operation_type: "sauce_reduction"
  
  # The Logic (Predicates)
  requirements:
    - type: "includes_ingredient"
      value: "pink_mushroom_desiccated"
      token_key: "catalyst"  # Variable for Trivia Text
      
    - type: "heat_level"
      value: "low"
      token_key: "temp"

  # The Trivia (Text Template)
  text_template: >
    "Compliance with Section 4 requires that {catalyst} be introduced 
    at {temp} heat to preserve the Blessing."
  
  # The Outcome
  success_effect: "preserve_tag"
  failure_effect: "strip_tag"

```

---

## 4. The Logic Systems

### A. The Cooking Resolver

When a Recipe is executed:

1. **Instantiate:** Create new `WorldInstance` (The Output).
2. **Transform:** Convert inputs based on `materials.yaml` (Raw -> Pickled).
3. **Inherit:** Copy tags from inputs to Output based on `tags.yaml` policy (Preserve Sacred, Overwrite Texture).
4. **Validate:** Run **Decree Checks**.
5. **Update Metrics Table**
* *Check:* Is `decree_morgoth_04` active?
* *If Fail:* Strip `blessed_by_morgoth` tag from Output.


5. **Commit:** Save Output to `WorldInstances`. Delete Inputs (or mark consumed).

### B. The Crisis Generator (Trivia)

When a Crisis occurs:

1. **Fetch:** Pick a random Decree (e.g., `decree_morgoth_04`).
2. **Parse:** Read `text_template`.
3. **Lie (Distractor Generation):**
* Identify `token_key: catalyst`. Real value: "Pink Mushroom".
* Query DB for other Items with tag `fungus`.
* *Distractor 1:* Replace `{catalyst}` with "Blue Toadstool".
* *Distractor 2:* Replace `{catalyst}` with "Dried Kelp".
4. **Render:** Display Question and the list of answers (1 True, 19 False).
5. **Update Metrics Table**

---

## 5. UI/UX Summary (The "Kafkaesque" TUI)

* **Visual Style:** Monospaced, ASCII/NerdFont, High Contrast (Black/White/Red).
* **Input:** Keyboard centric (`UP/DOWN/ENTER`). Intentional friction (manual scrolling).
* **The 11 Screens:**
1. **Menu:** Resume/New Shift.
2. **Intake:** Character Creator (Point Buy).
3. **Briefing:** Mission Orders & Quotas.
4. **Map:** Node-based Dungeon Traversal.
5. **Bakery Shift:** The core management loop (9 Tabs).
6. **Crisis:** The Trivia Minigame (Panic/Rage Meter).
7. **Settlement:** Upgrades & Debt Payment.
8. **Incident Report:** Game Over (Procedural HR Violations).
9. **Cutscene:** ASCII Animation Player.
10. **Codex:** Encyclopedia with Redacted Text.
11. **Settings:** Keybindings.


## 6. Implementation of `decrees`
This is the **"Single Source of Truth" (SSOT)** holy grail. You want to define a logic rule *once* in data, and have the game engine automatically derive both:

1. **The Code:** A executable function that checks if the sauce is actually blessed.
2. **The Content:** A coherent English sentence for the Trivia Minigame (and its wrong answers).

We can do this using a **Templated Predicate System**. We define the rule not as code, but as a set of **Assertions** mapped to **Language Tokens**.

Here is the architecture for the **"Decree System."**

### 1. The Schema: `decrees.yaml`

Instead of writing a generic "mix" policy, we write specific **Bureaucratic Decrees**. These override the default physics.

```yaml
# THE LAW OF MORGOTH'S SAUCE
decree_morgoth_04:
  # 1. SCOPE: When does this law trigger?
  target_tag: "blessed_by_morgoth"
  operation_type: "sauce_reduction"
  
  # 2. THE LOGIC (The Predicates)
  # The engine checks these against the inputs.
  requirements:
    - type: "includes_ingredient"
      value: "pink_mushroom_desiccated"
      # The Token ensures we can swap this value for wrong answers later
      token_key: "required_additive" 
      
    - type: "heat_level"
      value: "low"
      token_key: "temperature"

  # 3. THE TEXT (The Trivia Generator)
  # Uses the tokens defined above.
  text_template: >
    Per Section 4, the sanctity of a {target_tag} may only be preserved 
    in a reduction if catalyzed by {required_additive} applied at {temperature} heat.

  # 4. THE OUTCOME
  success_effect: "preserve_tag"
  failure_effect: "remove_tag" # The blessing is lost!

```

---

### 2. The Logic Path (Cooking)

When the player tries to make a sauce using a `Blessed Murder Grub`, the **Recipe Engine** runs the **Compliance Check**:

1. **Detect Trigger:** The input has `blessed_by_morgoth`. The operation is `sauce_reduction`.
2. **Fetch Decree:** The engine loads `decree_morgoth_04`.
3. **Evaluate Predicates:**
* *Check 1:* Does the pot contain `pink_mushroom_desiccated`?
* *Check 2:* Is the oven set to `low`?


4. **Apply Outcome:**
* If **True**: The final Sauce Item gets the `blessed_by_morgoth` tag.
* If **False**: The tag is stripped. The sauce is just "Grub Sauce" (Unblessed).



---

### 3. The Trivia Path (The Minigame)

This is the cool part. When the player enters the **Crisis Encounter**, the system generates a question based on this exact data.

**The Question Generation Algorithm:**

1. **Select a Rule:** Pick `decree_morgoth_04`.
2. **Generate the Question:**
* *"Regarding the preservation of Morgoth's Blessing in reductions: Which procedure is compliant?"*


3. **Generate the CORRECT Answer:**
* Fill the `text_template` with the *actual* values from the YAML.
* **Result:** "Per Section 4... catalyzed by **desiccated pink mushroom** applied at **low** heat."


4. **Generate WRONG Answers (Procedural Lying):**
* The engine looks at the `token_key` ("required_additive").
* It queries the Item Database for *other* ingredients that are valid but incorrect (e.g., `blue_toadstool`, `dried_kelp`).
* It swaps the variable in the template.
* **Distractor A:** "...catalyzed by **dried kelp** applied at low heat."
* **Distractor B:** "...catalyzed by **desiccated pink mushroom** applied at **searing** heat." (Swapped temperature).

### Why this fits the "Comedy"

You can make the rules arbitrarily specific and weird because the system just parses the predicates.

**Example: The "Counter-Clockwise" Rule**

```yaml
decree_goblin_stew_12:
  target_tag: "goblin_approved"
  operation_type: "stewing"
  requirements:
    - type: "stir_direction"
      value: "counter_clockwise"
      token_key: "direction"
  text_template: "Goblins will only consume stew if the ladle was agitated in a {direction} motion."

```

* **Logic:** If the player clicks "Stir Clockwise," the stew loses the `goblin_approved` tag. The Goblin customer spits it out.
* **Trivia:** "True or False: Clockwise stirring retains the Goblin Seal of Approval." -> **False**.

### 4. Integration with UI

* **The Codex:** The player can actually *read* these rules in the Codex (Screen 10). The Codex simply renders the `text_template` with the correct values.
* **The Crisis:** The player is tested on what they read in the Codex.

## 7. Implementation of Schemas

This is the **Core Schema Definition**. It enforces the "Pretentious Vocabulary" and structure for all future content generation.

## **COMPONENT: `core/models.py` (The Validator)**

This Python file defines the strict shapes of your YAML/JSON data. It acts as the "Gatekeeper" for the game engine.

### **1. The Controlled Vocabulary (Enums)**

```python
from enum import Enum
from typing import List, Dict, Union, Optional, Literal
from pydantic import BaseModel, Field, conint, confloat

# --- THE "MODERNIST" VOCABULARY ---

class FlavorProfile(str, Enum):
    # Standard
    SALTY = "salty"
    SWEET = "sweet"
    SOUR = "sour"
    BITTER = "bitter"
    UMAMI = "umami"
    # Eldritch / High Concept
    HOLLOW = "hollow"        # Absence of flavor
    STATIC = "static"        # Pins and needles
    PETRICHOR = "petrichor"  # Rain on dry earth
    SANGUINE = "sanguine"    # Iron/Blood
    CHROMA = "chroma"        # Synesthetic taste

class TextureProfile(str, Enum):
    FRIABLE = "friable"      # Crumbles (Shortcrust)
    ELASTIC = "elastic"      # Snaps back (Bread)
    VISCOUS = "viscous"      # Slime/Syrup
    AERATED = "aerated"      # Foam/Mousse
    CRYSTALLINE = "crystalline"
    FIBROUS = "fibrous"
    GELATINOUS = "gelatinous"

class CookingMethod(str, Enum):
    # Structural
    LAMINATE = "laminate"    # Folding fat
    SHEER = "sheer"
    AERATE = "aerate"
    DOCK = "dock"
    
    # Molecular
    SPHERIFY = "spherify"    # Alginate bath
    EMULSIFY = "emulsify"
    NIXTAMALIZE = "nixtamalize" # Alkali soak
    LYOPHILIZE = "lyophilize"   # Freeze-dry
    
    # Biological
    INOCULATE = "inoculate"  # Add mold
    CULTIVATE = "cultivate"  # Grow mold
    AUTOLYSE = "autolyse"    # Self-digest

class TagPolicy(str, Enum):
    PRESERVE = "preserve"    # Heirloom (Sacred)
    OVERWRITE = "overwrite"  # Material (Texture)
    MIX = "mix"              # Blend (Flavor)
    REMOVE = "remove"        # State (Raw)

```

### **2. The Entity Models**

```python
# --- THE DATA SHAPES ---

class StatBlock(BaseModel):
    """The continuous variables for physics/failure logic."""
    # Rheology
    elasticity: Optional[conint(ge=0, le=100)] = None
    plasticity: Optional[conint(ge=0, le=100)] = None
    friability: Optional[conint(ge=0, le=100)] = None
    
    # Chemistry
    ph_level: Optional[confloat(ge=0, le=14)] = None
    water_activity: Optional[confloat(ge=0, le=1)] = None
    
    # Flavor Intensity (0-100)
    flavor_intensity: Dict[FlavorProfile, int] = {}

class Ingredient(BaseModel):
    kind: Literal['ingredient'] = 'ingredient'
    id: str
    name: str
    description: str  # Flavour text
    
    # State Machine
    state_tags: List[str]  # ['raw', 'organ', 'sacred']
    stats: StatBlock
    
    # The Transformation Graph
    # Key: CookingMethod -> Value: Resulting Ingredient ID
    transforms: Dict[CookingMethod, str] = {}

class Decree(BaseModel):
    kind: Literal['decree'] = 'decree'
    id: str
    target_tag: str  # e.g., "sacred"
    operation: CookingMethod
    
    # The Logic (Predicates)
    # We use a flexible dict here for the "Absurd Rules"
    requirements: List[Dict[str, Union[str, int, float]]] 
    
    # The Trivia Generation
    text_template: str 
    token_keys: Dict[str, str] # Maps template vars to requirement keys

# --- THE MASTER UNION ---
# This allows a single YAML file to contain diverse objects
ContentObject = Union[Ingredient, Decree]

class Manifest(BaseModel):
    domain: str  # e.g., "morgoth_swamp"
    content: List[ContentObject]

```

### **3. Example Output (What the LLM will generate)**

Here is how a valid **"Morgoth Ingredient"** looks under this schema:

```yaml
domain: morgoth_swamp
content:
  - kind: ingredient
    id: "cave_cricket_flour"
    name: "Milled Cave Cricket"
    description: "High-chitin powder with significant water-binding potential."
    state_tags: ["powder", "raw", "insectoid"]
    stats:
      friability: 85
      water_activity: 0.2
      flavor_intensity:
        sanguine: 15
        petrichor: 60
    transforms:
      nixtamalize: "cricket_dough_mass"
      laminate: "cricket_puff_sheet"

```

## 8. Example data: **Vertical Slice** of **Goblin Slums**
This is the **Vertical Slice** for the **Goblin Slums**.

This file (`data/content/goblin_slums/manifest.yaml`) demonstrates every complex mechanic we discussed: **Opposing Gods**, **Long-Chain Refining**, **Selective Toxicity**, and **Custom Methods**.

### **The Manifest: `goblin_slums.yaml**`

```yaml
domain: goblin_slums

# ------------------------------------------------------------------
# 1. EXTENDING THE VOCABULARY (The Custom Method)
# ------------------------------------------------------------------
# We inject a new method specific to this biome's glowing fungi.
custom_methods:
  - id: "photo_activate"
    name: "Photo-Activation"
    description: "Bombarding bioluminescent matter with UV radiation to stabilize toxins."
    difficulty_mod: 1.5

# ------------------------------------------------------------------
# 2. THE INGREDIENTS (The Raw Materials)
# ------------------------------------------------------------------
content:
  # A. THE TOXIN (Selective Toxicity)
  # Safe for Goblins (who have 'iron_gut'), deadly for Elves.
  - kind: ingredient
    id: "sewer_eel_liver"
    name: "Hepatic Lobe of Blind Eel"
    description: "A filter organ rich in heavy metals and despair."
    state_tags: ["raw", "organ", "toxic_to_elves", "sanguine"]
    stats:
      ph_level: 4.5
      water_activity: 0.9
      flavor_intensity:
        bitter: 80
        sanguine: 40
        petrichor: 20
    transforms:
      nixtamalize: "eel_liver_cured" # Neutralizes toxin
      fry: "eel_liver_crisp"         # Still toxic!

  # B. THE BASE (The Long Chain Step 1)
  # Disgusting raw sludge.
  - kind: ingredient
    id: "bio_slurry_raw"
    name: "Raw Bio-Aggregate"
    description: "Unfiltered run-off from the Alchemy District."
    state_tags: ["liquid", "waste", "unstable"]
    stats:
      viscosity: 80
      flavor_intensity:
        hollow: 50
        sour: 30
    transforms:
      emulsify: "bio_slurry_stabilized" # Step 2

  # C. THE INTERMEDIATE (The Long Chain Step 2)
  # Stabilized, but bland. Needs mold.
  - kind: ingredient
    id: "bio_slurry_stabilized"
    name: "Stabilized Protein Matrix"
    state_tags: ["gel", "neutral"]
    stats:
      plasticity: 60
    transforms:
      inoculate: "myco_bloom_cake" # Step 3 (The Rot-Mother's favorite)

  # D. THE DELICACY (The Long Chain Step 3 - Final)
  # The glow-up. Literally.
  - kind: ingredient
    id: "myco_bloom_cake"
    name: "Photoluminescent Myco-Cake"
    description: "A spongy, glowing cake created by fungal colonization of sludge."
    state_tags: ["solid", "aerated", "biomorphic", "sacred_rot"]
    stats:
      friability: 40
      flavor_intensity:
        umami: 70
        chroma: 90 # Tastes like 'Green Light'
    transforms:
      photo_activate: "luminous_caviar" # The Ultra-Rare finish

# ------------------------------------------------------------------
# 3. THE DIVINE CONFLICT (Decrees)
# ------------------------------------------------------------------
  # GOD A: THE ROT-MOTHER (Loves Decay)
  # Demands inoculation (mold) for all soft foods.
  - kind: decree
    id: "decree_rot_01"
    target_tag: "sacred_rot"
    operation: "inoculate"
    requirements:
      - type: "texture_is"
        value: "soft"
        token_key: "texture_state"
      - type: "temperature_below"
        value: 20 # Celsius (Mold likes cool)
        token_key: "max_temp"
    
    # TRIVIA GENERATION
    text_template: >
      "The Rot-Mother blesses only those {texture_state} offerings which have 
      been inoculated below {max_temp} degrees, ensuring the bloom is vibrant."
    
    success_effect: "add_tag:blessed_by_rot"
    failure_effect: "add_tag:cursed_by_rot"

  # GOD B: THE STERILE ONE (Hates Decay)
  # Forbids the 'inoculate' step entirely if the food is meant to be 'Pure'.
  - kind: decree
    id: "decree_sterile_01"
    target_tag: "sacred_purity"
    operation: "sterilize" # Conflicting operation
    requirements:
      - type: "has_no_tag"
        value: "myco_bloom" # Hates the cake from Step 3
        token_key: "forbidden_contaminant"
    
    # TRIVIA GENERATION
    text_template: >
      "Purity is achieved only by the total absence of {forbidden_contaminant}. 
      Any trace of fungal life is an abomination."

# ------------------------------------------------------------------
# 4. THE RECIPE (Putting it together)
# ------------------------------------------------------------------
  - kind: recipe
    id: "neon_gut_bomb"
    name_pattern: "{Adjective} Sludge-Sphere"
    
    # The Conflict: You CANNOT please both gods with this dish.
    # It uses 'inoculate' (Rot-Mother happy) but contains 'myco_bloom' (Sterile One mad).
    inputs:
      - slot: "base"
        tag_filter: "aerated" # Accepts Myco-Cake
        mass_ratio: 0.8
      - slot: "garnish"
        tag_filter: "organ"   # Accepts Eel Liver
        mass_ratio: 0.2
    
    process: "spherify" # Modernist technique
    
    # The result
    base_stats:
      flavor_intensity:
        chroma: 50
        sanguine: 20

```

---

### **Test Scenarios (Verification)**

This data allows you to run the following **Integration Tests** in your CDD:

1. **Test: The Toxin Check**
* *Action:* Feed `eel_liver_crisp` (Fried) to an **Elf**.
* *Expected:* **Sickness**. (Fried does not remove `toxic_to_elves`).
* *Action:* Feed `eel_liver_cured` (Nixtamalized) to an **Elf**.
* *Expected:* **Safe**. (Nixtamalization removes toxin).


2. **Test: The Divine Conflict**
* *Action:* Present `Neon Gut-Bomb` to a follower of **The Sterile One**.
* *Logic:* Recipe contains `myco_bloom_cake`. Decree `sterile_01` forbids `myco_bloom`.
* *Expected:* **Rage Spike**. (Sacrilege).


3. **Test: The Long Chain**
* *Action:* Attempt to make `Luminous Caviar` from raw sludge.
* *Steps:* `Emulsify` -> `Inoculate` -> `Photo-Activate` -> `Spherify`.
* *Expected:* Success. Skipping any step results in `Generic Mush`.


4. **Test: Custom Method**
* *Action:* Attempt `Photo-Activation` without the upgrade module.
* *Expected:* **Menu Lock**. (Method not available in base kitchen).

