# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
TOGGLE_BTN_ID = "toggle-btn"
OVERLAY_ID = "overlay"
SIDEBAR_ID = "sidebar"

NAV_ITEMS = [
    ("Accueil", "#hero"),
    ("L’effet du prix sur le succès", "#scatter"),
    ("Le rôle du mode de jeu", "#box"),
    ("Quels genres dominent dans le temps ?", "#line"),
    ("Visibilité ou satisfaction ?", "#bubble"),
    ("Le temps de jeu compte-t-il ?", "#dot"),
    ("Qui sont les leaders du marché ?", "#violin"),
]

# ---------------------------------------------------------------------------
# Viz 1 - Scatter 
# ---------------------------------------------------------------------------
SCATTER_SLIDER_ID = "scatter-price-slider"
SCATTER_GRAPH_ID = "scatter-price-graph"
SCATTER_SLIDER_MIN = 0
SCATTER_SLIDER_MAX = 1000
SCATTER_SLIDER_STEP = 10

COL_ESTIMATED_OWNERS = "Estimated owners"
COL_ESTIMATED_OWNERS_AVG = "Estimated owners (average)"
COL_PRICE = "Price"
COL_TYPE = "Type de jeu"

# ---------------------------------------------------------------------------
# Viz 2 - Box 
# ---------------------------------------------------------------------------
GAME_TYPE_ORDER = ["Multijoueur", "Hybride", "Solo"]
CATEGORY_CENTER = {"Multijoueur": 0, "Hybride": 1, "Solo": 2}
SAMPLE_PER_CATEGORY = 600
LOG_BIN_WIDTH = 0.030
Y_STEP = 0.048
HALF_WIDTH = 0.42
COLORS = {
    "Solo": "#6678E8",
    "Hybride": "#D98A6C",
    "Multijoueur": "#52B788",
}
COL_CATEGORIES = "Categories"
COL_GAME_TYPE = "game_type"
SOLO_KEYWORDS = ["Single-player"]
MULTI_KEYWORDS = [
    "Multi-player", "Online PvP", "Online Co-op",
    "Co-op", "PvP", "Cross-Platform Multiplayer",
]

# ---------------------------------------------------------------------------
# Viz 3 - Line 
# ---------------------------------------------------------------------------
LINE_CHECKLIST_ID = "line-genre-checklist"
LINE_GRAPH_ID = "line-genre-graph"
LINE_ALL_ID = "line-all-toggle"

MAIN_GENRES = ["Action", "Adventure", "Indie", "Massively Multiplayer", "Free To Play", "RPG"]

COL_YEAR = "Release date"
COL_GENRES = "Genres"

YEAR_MIN = 1997
YEAR_MAX = 2025

GENRE_COLORS = {
    "Action": "#F4A535",
    "Adventure": "#E91E8C",
    "Indie": "#9C27B0",
    "Massively Multiplayer": "#B71C1C",
    "Free To Play": "#43A047",
    "RPG": "#1565C0",
}

OTHERS_COLOR = "#B0BAC9"
CHECKLIST_GENRES = MAIN_GENRES + ["Others"]

MILLIONS = 1_000_000.0

# ---------------------------------------------------------------------------
# Viz 4 - Bubble 
# ---------------------------------------------------------------------------
BUBBLE_SLIDER_MIN = 0
BUBBLE_SLIDER_MAX = 10000000
BUBBLE_SLIDER_STEP = 100000
BUBBLE_SLIDER_HEIGHT = 350

SAT_SLIDER_MIN = 0
SAT_SLIDER_MAX = 1
SAT_SLIDER_STEP = 0.1

BUBBLE_GRAPH_ID = "bubble-graph"
BUBBLE_Y_SLIDER_ID = "bubble-slider-y"
BUBBLE_X_SLIDER_ID = "bubble-slider-x"

# ---------------------------------------------------------------------------
# Viz 5 - Dot 
# ---------------------------------------------------------------------------
DOT_GRAPH_ID = "dot-graph"
DOT_SLIDER_ID = "dot-slider"
DOT_SLIDER_MIN = 0
DOT_SLIDER_MAX = 6000
DOT_SLIDER_STEP = 100
DOT_SLIDER_HEIGHT = 340

COL_SAT_ROUNDED = "Satisfaction rounded"
COL_X_PLOT = "_viz5_x_beeswarm"
BEESWARM_HALF_SPAN = 0.044
BEESWARM_MAX_PER_STRIP = 110
COL_PLAYTIME = "Playtime hours"
COL_PLAYTIME_FOREVER = "Average playtime forever"

# ---------------------------------------------------------------------------
# Viz 6 - Violin 
# ---------------------------------------------------------------------------
VIOLIN_GRAPH_ID = "violin-graph"
VIOLIN_SLIDER_ID = "violin-slider"
VIOLIN_SLIDE_SLIDER_VALUES = [50, 5, 50]

VIOLIN_SLIDER_MIN = 1
VIOLIN_SLIDER_MAX = 50
VIOLIN_SLIDER_STEP = 1
VIOLIN_SLIDER_HEIGHT = 320

# ---------------------------------------------------------------------------
# Commons
# ---------------------------------------------------------------------------
COL_NAME = "Name"
COL_OWNERS = "Estimated owners"
COL_OWNERS_AVG = "Estimated owners (average)"

COL_POS = "Positive"
COL_NEG = "Negative"
COL_SAT = "Satisfaction"
COL_VIS = "Visibility"