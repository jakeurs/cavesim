from enum import Enum, auto
from typing import Optional, Dict, Any, Union, List, Set, Literal
from pydantic import BaseModel, Field, computed_field

# ==========================================
# 1. DISPLAY PRIMITIVES
# ==========================================

class RichText(BaseModel):
    """
    A unified text object that handles templating, styling, and metadata.
    """
    template: str
    tags: List[str] = Field(default_factory=list) # Replaces UIStyle enum
    icon: Optional[str] = None
    tooltip: Optional[str] = None 

    def resolve(self, context: Dict[str, Any] = None) -> str:
        if not context:
            return self.template
        try:
            return self.template.format(**context)
        except (KeyError, ValueError):
            return self.template

# ==========================================
# 2. TIME PRIMITIVES
# ==========================================

class CaveCycle(str, Enum):
    DORMANT = "Dormant (Night)"        # 00:00 - 06:00
    SPORE_RISE = "Spore Rise (Morning)" # 06:00 - 10:00
    BLOOM = "Full Bloom (Noon)"         # 10:00 - 14:00
    WITHER = "Wither (Afternoon)"       # 14:00 - 18:00
    DECAY = "Decay (Evening)"           # 18:00 - 24:00

class GameTime(BaseModel):
    total_minutes: int = 0
    
    @computed_field
    def cycle_phase(self) -> CaveCycle:
        day_minute = self.total_minutes % 1440
        if 0 <= day_minute < 360: return CaveCycle.DORMANT
        elif 360 <= day_minute < 600: return CaveCycle.SPORE_RISE
        elif 600 <= day_minute < 840: return CaveCycle.BLOOM
        elif 840 <= day_minute < 1080: return CaveCycle.WITHER
        else: return CaveCycle.DECAY

    def __str__(self):
        day_minute = self.total_minutes % 1440
        return f"{day_minute // 60:02d}:{day_minute % 60:02d}"

# ==========================================
# 3. TAG PRIMITIVES (Identity & Taxonomy)
# ==========================================

class TagPolicy(str, Enum):
    BOOLEAN = "boolean"
    STACK = "stack"
    MAX = "max"
    REFRESH = "refresh"

class TagDefinition(BaseModel):
    """Static definition of a Tag in the registry."""
    id: str
    display: RichText
    parents: List[str] = Field(default_factory=list)
    policy: TagPolicy = TagPolicy.BOOLEAN
    is_visible: bool = True

    def resolve_flattened_tags(self, registry: Dict[str, 'TagDefinition']) -> Set[str]:
        flattened = {self.id}
        visited = set()

        def _recurse(current_id: str):
            if current_id in visited: return
            visited.add(current_id)
            definition = registry.get(current_id)
            if not definition: return
            for parent_id in definition.parents:
                flattened.add(parent_id)
                _recurse(parent_id)

        for parent in self.parents:
            _recurse(parent)
        return flattened

class ActiveTag(BaseModel):
    """Runtime instance of a tag."""
    definition_id: str
    value: int = 1
    
    def apply(self, new_value: int, policy: TagPolicy):
        if policy == TagPolicy.BOOLEAN: self.value = 1
        elif policy == TagPolicy.STACK: self.value += new_value
        elif policy == TagPolicy.MAX: self.value = max(self.value, new_value)
        elif policy == TagPolicy.REFRESH: self.value = new_value

# ==========================================
# 4. ATTRIBUTE PRIMITIVES (Stats & Skills)
# ==========================================

class AttributeDefinition(BaseModel):
    """Static definition of a Stat (Strength, Viscosity)."""
    id: str
    display: RichText
    tags: List[str] = Field(default_factory=list) # Metadata tags
    min_value: int = 0
    max_value: int = 100
    default_value: int = 0
    is_hidden: bool = False

class StatModifier(BaseModel):
    """A temporary or permanent alteration to a stat."""
    source_id: str  # What caused this? (e.g., "spell_haste", "item_ring")
    value: int      # Can be negative
    is_percentage: bool = False
    duration_minutes: Optional[int] = None # None = Permanent

class AttributeValue(BaseModel):
    """Runtime instance of a Stat."""
    definition_id: str
    base_value: int
    modifiers: List[StatModifier] = Field(default_factory=list)

    @computed_field
    def current_value(self) -> int:
        """Calculates final value after all modifiers."""
        total = self.base_value
        percent_mod = 0.0
        
        for mod in self.modifiers:
            if mod.is_percentage:
                percent_mod += mod.value
            else:
                total += mod.value
        
        if percent_mod != 0:
            total = int(total * (1 + (percent_mod / 100)))
            
        return total

# ==========================================
# 5. RESOURCE PRIMITIVES (Economy & Meters)
# ==========================================

class ResourceDefinition(BaseModel):
    """Static definition of a Currency (Gold) or Meter (Sanity)."""
    id: str
    display: RichText
    tags: List[str] = Field(default_factory=list) # Metadata tags
    min_value: int = 0
    max_value: int = 999999
    default_max: int = 100 # Default 'Cap' for this resource

class ResourceModifier(BaseModel):
    """Modifiers that affect resource GAIN/LOSS (e.g. +20% Gold Gain)."""
    source_id: str
    value: float
    is_percentage: bool = False
    duration_minutes: Optional[int] = None

class ResourceValue(BaseModel):
    """Runtime instance of a Resource."""
    definition_id: str
    current: int
    max_capacity: int # The 'Hard Cap' for this specific entity
    gain_modifiers: List[ResourceModifier] = Field(default_factory=list)

    def add(self, amount: int) -> int:
        """
        Safely adds value with modifiers applied. 
        Returns actual amount added.
        """
        if amount > 0:
            # Apply 'Gain' modifiers
            final_amount = amount
            percent_mod = 0.0
            flat_mod = 0
            
            for mod in self.gain_modifiers:
                if mod.is_percentage:
                    percent_mod += mod.value
                else:
                    flat_mod += mod.value
            
            final_amount = (final_amount + flat_mod) * (1 + (percent_mod / 100))
            final_amount = int(final_amount)
            
            old_current = self.current
            self.current = min(self.current + final_amount, self.max_capacity)
            return self.current - old_current
            
        else:
            # Simple subtraction (could add 'loss mitigation' logic here later)
            old_current = self.current
            self.current = max(self.current + amount, 0) # Assuming 0 is hard floor
            return self.current - old_current

# ==========================================
# 6. LOGIC PRIMITIVES (The Engine Instructions)
# ==========================================

class LogicOperator(str, Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    HAS_TAG = "has_tag"
    MISSING_TAG = "missing_tag"

class Condition(BaseModel):
    """
    A logic gate.
    Example: { target="strength", operator=">", value=10 }
    """
    target_id: str  # The Attribute ID, Tag ID, or Resource ID to check
    operator: LogicOperator
    value: Union[int, str, bool]

class EffectType(str, Enum):
    MODIFY_ATTRIBUTE = "mod_attr"
    MODIFY_RESOURCE = "mod_resource"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    SPAWN_ITEM = "spawn_item"
    TRIGGER_EVENT = "trigger_event"
    DISPLAY_MESSAGE = "msg"

class Effect(BaseModel):
    """
    An atomic instruction to the Game Engine.
    Example: { type="mod_resource", target="hp", value=-5 }
    """
    type: EffectType
    target_id: str 
    value: Union[int, str, float]
    
    # Optional parameters for complex effects
    # e.g., duration for a tag, or quantity for spawning items
    params: Dict[str, Any] = Field(default_factory=dict) 

class TriggerType(str, Enum):
    ON_CONSUME = "on_consume"    # When eaten
    ON_COOK = "on_cook"          # When used as ingredient
    ON_ACQUIRE = "on_acquire"    # When picked up
    ON_TIME_PASS = "on_tick"     # Every minute
    ON_DIALOGUE = "on_dialogue"  # When talked to

class EffectHook(BaseModel):
    """
    A reactive logic block.
    "When [Trigger] happens, if [Condition] is met, do [Effect]."
    """
    trigger: TriggerType
    conditions: List[Condition] = Field(default_factory=list)
    effects: List[Effect]