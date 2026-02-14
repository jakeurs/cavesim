from enum import Enum


class FlavorProfile(str, Enum):
    # Standard
    SALTY = "salty"
    SWEET = "sweet"
    SOUR = "sour"
    BITTER = "bitter"
    UMAMI = "umami"
    # Eldritch / High Concept
    HOLLOW = "hollow"  # Absence of flavor
    STATIC = "static"  # Pins and needles
    PETRICHOR = "petrichor"  # Rain on dry earth
    SANGUINE = "sanguine"  # Iron/Blood
    CHROMA = "chroma"  # Synesthetic taste


class Texture(str, Enum):
    FRIABLE = "friable"  # Crumbles (Shortcrust)
    ELASTIC = "elastic"  # Snaps back (Bread)
    VISCOUS = "viscous"  # Slime/Syrup
    AERATED = "aerated"  # Foam/Mousse
    CRYSTALLINE = "crystalline"
    FIBROUS = "fibrous"
    GELATINOUS = "gelatinous"


class CookingMethod(str, Enum):
    # Structural
    LAMINATE = "laminate"  # Folding fat
    SHEER = "sheer"
    AERATE = "aerate"
    DOCK = "dock"

    # Molecular
    SPHERIFY = "spherify"  # Alginate bath
    EMULSIFY = "emulsify"
    NIXTAMALIZE = "nixtamalize"  # Alkali soak
    LYOPHILIZE = "lyophilize"  # Freeze-dry

    # Biological
    INOCULATE = "inoculate"  # Add mold
    CULTIVATE = "cultivate"  # Grow mold
    AUTOLYSE = "autolyse"  # Self-digest

    # Additional
    STERILIZE = "sterilize"
    PHOTO_ACTIVATE = "photo_activate"


class TagPolicy(str, Enum):
    PRESERVE = "preserve"  # Heirloom (Sacred)
    OVERWRITE = "overwrite"  # Material (Texture)
    MIX = "mix"  # Blend (Flavor)
    REMOVE = "remove"  # State (Raw)
