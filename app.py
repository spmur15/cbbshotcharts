import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
from plotly.colors import sample_colorscale
import warnings
warnings.filterwarnings("ignore")

# ==================================================
# GLOBAL THEME (single source of truth)
# ==================================================

# THEME = {
#     # ---- Base colors ----
#     "bg_app": "#ededed",
#     "bg_panel": "#f7f8fa",
#     "bg_card": "#ffffff",
#     "bg_chart": "#f8f8f8",
#     "bg_dropdown": "#ffffff",

#     # ---- Text ----
#     "text_primary": "#222222",
#     "text_secondary": "#666666",
#     "text_muted": "#888888",
#     "text_inverse": "#ffffff",

#     # ---- Accents ----
#     "accent_primary": "#222222",
#     "accent_secondary": "#999999",

#     # ---- Borders / dividers ----
#     "border_light": "#e0e0e0",
#     "divider": "rgba(0,0,0,0.15)",

#     # ---- Shadows ----
#     "shadow_sm": "0 6px 16px rgba(0,0,0,0.12)",
#     "shadow_md": "0 6px 18px rgba(0,0,0,0.22)",
#     "shadow_lg": "0 10px 28px rgba(0,0,0,0.25)",

#     # ---- Charts ----
#     "court_line": "#999999",
#     "make": "rgba(40,160,60,0.5)",
#     "miss": "rgba(220,50,50,0.33)",

#     # ---- Frequency bar ----
#     "freq_bg": "#eeeeee",
#     "freq_colors": ["#4CAF50", "#FFC107", "#2196F3"]

# }

THEME = {
    # ---- Base colors ----
    "bg_app": "#121212",
    "bg_panel": "#1a1d21",
    "bg_card": "#1f2328",
    "bg_chart": "#1f2328",
    "bg_dropdown": "#1f2328",

    # ---- Text ----
    "text_primary": "#eaeaea",
    "text_secondary": "#b0b0b0",
    "text_muted": "#888888",
    "text_inverse": "#000000",

    # ---- Accents ----
    "accent_primary": "#ffffff",
    "accent_secondary": "#bbbbbb",

    # ---- Borders / dividers ----
    "border_light": "#2a2a2a",
    "divider": "rgba(255,255,255,0.15)",

    # ---- Shadows ----
    "shadow_sm": "0 6px 16px rgba(0,0,0,0.7)",
    "shadow_md": "0 6px 18px rgba(0,0,0,0.85)",
    "shadow_lg": "0 10px 28px rgba(0,0,0,0.95)",

    # ---- Charts ----
    "court_line": "#dbdbdb",
    "make": "rgba(60,200,120,0.5)",
    "miss": "rgba(240,90,90,0.3)",

    # ---- Frequency bar ----
    "freq_bg": "#2a2a2a",
    "freq_colors": ["#6ddf8c", "#ffd166", "#6fa8ff", "#e36d6d"]
}



logo_path = r'currentSzn.csv'
LOGO_DF = pd.read_csv(logo_path)[['Team', 'Logo']]
LOGO_DF['Team'] = LOGO_DF['Team'].str.replace(' State$', ' St.', regex=True)
LOGO_DF['Team'] = LOGO_DF['Team'].str.replace('St. John\'s', 'St. John\'s (NY)', regex=True)
#color = sample_colorscale("RdYlGn", pct)[0]
#

# --------------------------------------------------
# Zone reconciliation maps (mid <-> three)
# --------------------------------------------------
THREE_TO_MID = {
    "Top 3": "Top Mid",
    "Left Wing 3": "Left Mid",
    "Right Wing 3": "Right Mid",
    "Left Corner 3": "Left Mid Low",
    "Right Corner 3": "Right Mid Low",
}

MID_TO_THREE = {v: k for k, v in THREE_TO_MID.items()}


COURT_LINE_COLOR = THEME["court_line"]
COURT_LINE_WIDTH = 1

COURT_SHADOW_COLOR = "rgba(0,0,0,0.18)"
COURT_SHADOW_OFFSET = 0.6

R_MAX = 25   # must match y-axis max in layout

team_p5 = [
    'Michigan', 'Duke', 'Gonzaga', 'Arizona', 'Iowa St.',
    'BYU', 'Vanderbilt', 'UConn', 'Purdue', 'Michigan St.',
    'Louisville', 'Nebraska', 'Illinois', 'Alabama', 'Houston',
    'Kansas', 'Georgia', 'Arkansas', 'Iowa', 'North Carolina',
    'Virginia', 'Florida', "Saint Mary's (CA)", "St. John's (NY)", 'Texas Tech',
    'Indiana', 'Kentucky', 'Clemson', 'Saint Louis', 'Utah St.',
    'Miami (FL)', 'LSU', 'Auburn', 'Villanova', 'Tennessee',
    'NC State', 'Southern California', 'Seton Hall', 'Boise St.', 'Tulsa',
    'SMU', 'UCLA', 'Butler', 'UCF', 'Yale',
    'McNeese', 'Colorado', 'Wake Forest', 'Ohio St.', 'Oklahoma',
    'Arizona St.', 'UC San Diego', 'Utah Valley', 'Colorado St.', 'Belmont',
    'Akron', 'Santa Clara', 'Virginia Tech', 'California', 'Wyoming',
    'Washington', 'VCU', 'New Mexico', 'George Mason', 'TCU',
    'Baylor', 'Notre Dame', 'Kansas St.', 'Texas', 'Wisconsin',
    'William & Mary', 'Oklahoma St.', 'Missouri', 'Northwestern', 'South Fla.',
    'Sam Houston', 'George Washington', 'Miami (OH)', 'Dayton', 'Richmond',
    'Texas A&M', 'Murray St.', 'San Diego St.', 'Pacific', 'Columbia',
    'Bowling Green', 'Illinois St.', 'UNI', 'Nevada', 'Hofstra',
    'Providence', 'Syracuse', 'UNCW', 'California Baptist', 'Wichita St.',
    'Davidson', 'Ole Miss', 'St. Bonaventure', 'West Virginia', 'ETSU',
    'Xavier', 'Winthrop', 'Rhode Island', 'Penn St.', 'Northern Colo.',
    'Fla. Atlantic', 'Mercer', 'Lipscomb', 'Stanford', 'Seattle U',
    'Idaho St.', 'Creighton', 'SFA', 'South Carolina', 'St. Thomas (MN)',
    'High Point', 'Hawaii', 'Marshall', 'San Francisco', 'Memphis',
    'Grand Canyon', 'Minnesota', 'Southern Ill.', 'UAB', 'Western Ky.',
    'Georgetown', 'Oregon', 'Cincinnati', 'New Mexico St.', 'North Dakota St.',
    'Florida St.', 'Mississippi St.', 'Middle Tenn.', 'UC Irvine', 'Siena',
    'Towson', 'Wright St.', 'Bradley', 'Idaho', 'UT Arlington',
    'Colgate', 'Troy', 'Austin Peay', 'Liberty', 'LMU (CA)',
    'Quinnipiac', 'DePaul', 'Utah', 'Cornell', 'Oakland',
    'Elon', 'Buffalo', 'Stony Brook', 'Youngstown St.', 'Kent St.',
    'Drake', 'South Dakota St.', 'Arkansas St.', 'Marist', 'Iona',
    'Toledo', 'Maryland', 'Robert Morris', 'Marquette', 'UC Santa Barbara',
    'Montana St.', 'Pittsburgh', 'Southern Miss.', 'South Alabama', 'Furman',
    'Fresno St.', 'UC Davis', 'Massachusetts', 'UTRGV', 'Weber St.',
    'Tarleton St.', 'FIU', 'UT Martin', 'Northern Ky.', 'Duquesne',
    'Boston College', 'Lindenwood', 'North Texas', 'Vermont', 'Central Conn. St.',
    'Portland St.', 'Indiana St.', 'Tennessee St.', 'Washington St.', 'Cal St. Fullerton',
    'LIU', 'Kennesaw St.', 'Eastern Mich.', 'Charlotte', 'A&M-Corpus Christi',
    'Ohio', 'USC Upstate', 'Rutgers', 'Oregon St.', 'Temple',
    'Tennessee Tech', 'Georgia Tech', 'Northeastern', 'James Madison', 'UNLV',
    'Navy', 'FGCU', 'Portland', 'Coastal Carolina', 'Southeast Mo. St.',
    'Cal Poly', 'Queens (NC)', 'UIC', 'Col. of Charleston', 'Charleston So.',
    'Abilene Christian', 'Fordham', 'Ga. Southern', 'Harvard', 'Louisiana Tech',
    'Montana', 'Green Bay', 'CSUN', 'Valparaiso', 'Monmouth',
    'North Ala.', 'Lamar University', 'Norfolk St.', 'Utah Tech', 'UC Riverside',
    'UNC Asheville', 'Penn', 'UIW', 'Rice', 'SIUE',
    'Alabama St.', "Saint Joseph's", 'Old Dominion', 'American', 'Central Ark.',
    'New Orleans', 'App State', 'Purdue Fort Wayne', 'Bethune-Cookman', 'East Texas A&M',
    'Wofford', 'Grambling', 'Milwaukee', 'San Jose St.', 'Brown',
    'Alabama A&M', 'Fairfield', 'Omaha', 'Presbyterian', 'Wagner',
    'Campbell', 'Denver', 'Dartmouth', 'Hampton', 'Sacred Heart',
    'Holy Cross', 'Northern Ariz.', 'Tulane', 'Eastern Wash.', 'Sacramento St.',
    'Samford', 'San Diego', 'Southern U.', 'West Ga.', 'Western Mich.',
    'South Dakota', 'Merrimack', 'La Salle', 'Houston Christian', 'Pepperdine',
    'Western Caro.', 'Texas St.', 'Bellarmine', 'Delaware', 'Oral Roberts',
    'UMBC', 'Le Moyne', 'N.C. A&T', 'Nicholls', 'Long Beach St.',
    'Detroit Mercy', 'Howard', 'UNC Greensboro', 'Jacksonville', 'Evansville',
    'UTEP', 'Missouri St.', 'Boston U.', 'Chattanooga', 'Eastern Ky.',
    'Southeastern La.', 'Drexel', 'Ark.-Pine Bluff', 'Morehead St.', 'Princeton',
    'Prairie View', 'Radford', 'Air Force', 'Jacksonville St.', 'Army West Point',
    'East Carolina', 'UTSA', 'Bucknell', 'Lehigh', "Saint Peter's",
    'Bryant', 'Northwestern St.', 'New Haven', 'IU Indy', 'NIU',
    'Manhattan', 'UMass Lowell', 'Southern Ind.', 'CSU Bakersfield', 'Mercyhurst',
    'Longwood', 'Chicago St.', "Mount St. Mary's", 'Central Mich.', 'North Dakota',
    'Alcorn', 'UAlbany', 'Canisius', 'Maine', 'New Hampshire',
    'Georgia St.', 'Eastern Ill.', 'VMI', 'North Florida', 'UMES',
    'Southern Utah', 'Stetson', 'Lafayette', 'Florida A&M', 'NJIT',
    'Texas Southern', 'Stonehill', 'Ball St.', 'Kansas City', 'Cleveland St.',
    'N.C. Central', 'ULM', 'Loyola Chicago', 'Little Rock', 'Loyola Maryland',
    'Jackson St.', 'Delaware St.', 'Western Ill.', 'Louisiana', 'FDU',
    'Niagara', 'Gardner-Webb', 'The Citadel', 'Morgan St.', 'Saint Francis',
    'Binghamton', 'South Carolina St.', 'Rider', 'Coppin St.', 'Mississippi Val.'
]



# ---- Zone geometry (feet, hoop-centered) ----
R_RIM = 5.5
R_PAINT = 10
R_3 = 22

R_RIM = 5.5
R_PAINT_EDGE = R_PAINT + 1
R_PAINT = R_PAINT + 2.6
R_3_EDGE = R_3 + 0.25
R_3 = R_3 + 0.25
R_MAX = 31.5

ZONE_DRAW_ORDER = [
    "Paint (Non-Rim)",
     "Paint (Non-Rim) Right",
     "Paint (Non-Rim) Middle",
     "Paint (Non-Rim) Left",
    "Left Baseline 2", "Right Baseline 2",
    "Top Mid", "Left Mid", "Right Mid",
    "Top 3", "Left Wing 3", "Right Wing 3", "Corner 3",
    "Rim"
]


ZONE_FAMILY = {
    # Rim / Paint
    "Rim": "paint",
    "Paint (Non-Rim)": "short_mid",

    "Paint (Non-Rim) Left": "short_mid",
    "Paint (Non-Rim) Middle": "short_mid",
    "Paint (Non-Rim) Right": "short_mid",

    # Midrange
    "Top Mid": "mid",
    "Left Mid": "mid",
    "Right Mid": "mid",
    "Left Mid Low": "mid",
    "Right Mid Low": "mid",

    # Threes
    "Top 3": "three",
    "Left Wing 3": "three",
    "Right Wing 3": "three",
    "Left Corner 3": "three",
    "Right Corner 3": "three",
}


ZONE_PCT_RANGES = {
    "three": (0.2, 0.50),   # 25% bad → 40% good
    "short_mid":   (0.3, 0.65),
    "mid":   (0.2, 0.60),   # 35% bad → 50% good
    "paint": (0.3, 0.75),   # 50% bad → 70% good
}



ANGLE_CORNER = 67     # degrees
ANGLE_WING = 22

def rotate_for_display(x, y):
    """
    Rotate coordinates so baseline is at the bottom.
    """
    return x,y

def polar_wedge(r0, r1, a0, a1, n=50):
    a_outer = np.linspace(np.radians(a0), np.radians(a1), n)

    x_outer = r1 * np.sin(a_outer)
    y_outer = r1 * np.cos(a_outer)

    # clip everything below baseline
    y_outer = np.maximum(y_outer, -5.25)

    a_inner = np.linspace(np.radians(a1), np.radians(a0), n)
    x_inner = r0 * np.sin(a_inner)
    y_inner = r0 * np.cos(a_inner)
    y_inner = np.maximum(y_inner, -5.25)

    x = np.concatenate([x_outer, x_inner])
    y = np.concatenate([y_outer, y_inner])

    path = f"M {x[0]:.3f},{y[0]:.3f} "
    for xi, yi in zip(x[1:], y[1:]):
        path += f"L {xi:.3f},{yi:.3f} "
    path += "Z"

    return path

def baseline_rect(x0, x1, y0=0, y1=R_PAINT_EDGE):
    return dict(
        type="rect",
        x0=x0, y0=y0,
        x1=x1, y1=y1,
        line=dict(width=0)
    )



ZONE_SHAPES = {
    # Rim
    "Rim": dict(
        type="circle",
        x0=-R_RIM, y0=-R_RIM,
        x1=R_RIM, y1=R_RIM,
        line=dict(width=0)
    ),

    # Paint non-rim
    "Paint (Non-Rim) Right": dict(
        type="path",
        path=polar_wedge(R_RIM, R_PAINT, ANGLE_CORNER, 180),
        line=dict(width=3)
    ),

    # Paint non-rim
    "Paint (Non-Rim) Middle": dict(
        type="path",
        path=polar_wedge(R_RIM, R_PAINT, -ANGLE_CORNER, ANGLE_CORNER),
        line=dict(width=3)
    ),

    # Paint non-rim
    "Paint (Non-Rim) Left": dict(
        type="path",
        path=polar_wedge(R_RIM, R_PAINT, -ANGLE_CORNER, -180),
        line=dict(width=3)
    ),

    # Midrange
    "Top Mid": dict(
        type="path",
        path=polar_wedge(R_PAINT, R_3, -ANGLE_WING, ANGLE_WING),
        line=dict(width=0)
    ),
    "Left Mid": dict(
        type="path",
        path=polar_wedge(R_PAINT, R_3, ANGLE_WING, ANGLE_CORNER),
        line=dict(width=0)
    ),
    "Right Mid": dict(
        type="path",
        path=polar_wedge(R_PAINT, R_3, -ANGLE_CORNER, -ANGLE_WING),
        line=dict(width=0)
    ),
    "Right Mid Low": dict(
        type="path",
        path=polar_wedge(R_PAINT, R_3, ANGLE_CORNER, 180),
        line=dict(width=0)
    ),
    "Left Mid Low": dict(
        type="path",
        path=polar_wedge(R_PAINT, R_3, -ANGLE_CORNER, -180),
        line=dict(width=0)
    ),

    # Threes
    "Top 3": dict(
        type="path",
        path=polar_wedge(R_3, R_MAX, -ANGLE_WING, ANGLE_WING),
        line=dict(width=0)
    ),
    "Left Wing 3": dict(
        type="path",
        path=polar_wedge(R_3, R_MAX, ANGLE_WING, ANGLE_CORNER),
        line=dict(width=0)
    ),
    "Right Wing 3": dict(
        type="path",
        path=polar_wedge(R_3, R_MAX, -ANGLE_CORNER, -ANGLE_WING),
        line=dict(width=0)
    ),
    "Right Corner 3": dict(
        type="path",
        path=polar_wedge(R_3, R_MAX, ANGLE_CORNER, 180),
        line=dict(width=0)
    ),
    "Left Corner 3": dict(
        type="path",
        path=polar_wedge(R_3, R_MAX, -ANGLE_CORNER, -180),
        line=dict(width=0)
    ),
}

# ZONE_SHAPES.update({
#     "Left Baseline 2": baseline_rect(
#         x0=-22, x1=-8
#     ),
#     "Right Baseline 2": baseline_rect(
#         x0=8, x1=22
#     )
# })



ZONE_LABEL_POS = {
    "Rim": (0, 0),
    "Paint (Non-Rim)": (0,6),

    "Paint (Non-Rim) Right": (0,6),
    "Paint (Non-Rim) Middle": (0,6),
    "Paint (Non-Rim) Left": (0,6),

    "Top Mid": (18,0),
    "Left Mid": (10, 12),
    "Right Mid": (10, -12),
    "Left Mid Low": (-22, -8),
    "Right Mid Low": (-12, 10),

    "Top 3": (0, 30),
    "Left Wing 3": (16, ),
    "Right Wing 3": (-16, ),
    "Corner 3": (22, 8),
}
# ZONE_LABEL_POS.update({
#     "Left Baseline 2": (-18, 6),
#     "Right Baseline 2": (18, 6),
# })




# ----------------------------
# 3PT geometry (hoop-centered)
# ----------------------------
R_3PT = 22.175
BASELINE_X = 5.25
CORNER_Y = 15

theta_max = np.arccos(BASELINE_X / R_3PT)
thetas = np.linspace(-theta_max, theta_max, 500)

ARC_X = -R_3PT * (np.cos(thetas)*1.025)
ARC_Y = R_3PT * (np.sin(thetas)*1.025)

# --------------------------------------------------
# LOAD DATA (loaded once at startup)
# --------------------------------------------------
# DATA_PATH = "Shot Location Data//Wisconsin_shot_data_20.csv"
# df = pd.read_csv(DATA_PATH)
# df['offense_defense'] = np.where(df['team_name']=='Wisconsin', 'Offense', 'Defense')
# df['made'] = np.where(df['result']=='made', 1, 0)

# ---- ASSUMED COLUMN NAMES ----
# Update these if needed
X_COL = "x"
Y_COL = "y"
MADE_COL = "made"              # 1/0 or True/False
PLAYER_COL = "shooter"
TEAM_COL = "team_name"
HALF_COL = "period"
OPP_COL = "opponent"
OFF_DEF_COL = "offense_defense"  # "Offense" / "Defense"

# --------------------------------------------------
# COURT DRAWING FUNCTION
# --------------------------------------------------
def create_half_court_layout():
    """
    Hoop-centered half court in FEET.

    x range: [-41.75, 5.25]  (midcourt to baseline, relative to hoop)
    y range: [-25, 25]
    """
    shapes = []

    # Court bounds (half court)
    # shapes.append(dict(
    #     type="rect",
    #     x0=-25, y0=-5.25, x1=25, y1=41.75,
    #     line=dict(color=, width=COURT_LINE_WIDTH),
    #     fillcolor="rgba(0,0,0,0)"
    # ))


    # Hoop (18" diameter => radius 0.75 ft)
    # shapes.append(dict(
    #     type="circle",
    #     x0=-0.75, y0=-0.75, x1=0.75, y1=0.75,
    #     line=dict(color="#ff8c00", width=1)
    # ))

    # Backboard (4 ft from baseline; baseline is at +5.25, so backboard at +1.25)
    # shapes.append(dict(
    #     type="line",
    #     x0=1.25, y0=-3, x1=1.25, y1=3,
    #     line=dict(color="#111", width=1)
    # ))

    # Paint (lane) - 12 ft wide; FT line is 15 ft from hoop => x = -15
    # Baseline relative is +5.25
    shapes.append(dict(
        type="rect",
        x0=-15.0, y0=-6.0, x1=5.25, y1=6.0,
        line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH)

    ))

    # # Free throw circle (radius 6 ft, centered at FT line)
    # shapes.append(dict(
    #     type="circle",
    #     x0=-21.0, y0=-6.0, x1=-9.0, y1=6.0,
    #     line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH)

    # ))

    # Calculate the arc
    center_y = 15.0  # midpoint of your x0 and x1
    center_x = 0.0    # midpoint of your y0 and y1
    radius = 6.0

    # Create points for the top semi-circle
    theta = np.linspace(0, np.pi, 50)  # 0 to π for top half
    x_points = center_x + radius * np.cos(theta)
    y_points = center_y + radius * np.sin(theta)

    # Create the path
    path = f"M {x_points[0]},{y_points[0]}"
    for x, y in zip(x_points[1:], y_points[1:]):
        path += f" L {x},{y}"

    shapes.append(dict(
        type="path",
        path=path,
        line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH)
    ))

    

    # # Restricted area (approx 4 ft radius)
    # shapes.append(dict(
    #     type="circle",
    #     x0=-4.0, y0=-4.0, x1=4.0, y1=4.0,
    #     line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH)

    # ))

    # ---- 3PT LINE (NCAA, HOOP-CENTERED, CLIPPED TO HALF COURT) ----
    # ---- 3PT ARC AS LINE TRACE (RELIABLE) ----
    R_3PT = 22.15
    BASELINE_X = 5.25

    # angles that correspond to where the arc intersects the baseline
    theta_max = np.arccos(BASELINE_X / R_3PT)
    thetas = np.linspace(-theta_max, theta_max, 200)

    arc_x = R_3PT * np.cos(thetas)
    arc_y = R_3PT * np.sin(thetas)

    shapes.append(dict(
        type="line",  # dummy placeholder so layout still works
        x0=0, y0=0, x1=0, y1=0,
        line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH)

    ))






    rotated_shapes = [rotate_shape(s) for s in shapes]

    layout = go.Layout(
        shapes=rotated_shapes,
        xaxis=dict(
            range=[-32, 32],
            showgrid=False, zeroline=False, showticklabels=False
        ),
        yaxis=dict(
            range=[-3.5, R_MAX],
            showgrid=False, zeroline=False, showticklabels=False,
            scaleanchor="x", scaleratio=1
        ),
        plot_bgcolor=THEME["bg_chart"],
        paper_bgcolor=THEME["bg_chart"],
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["text_secondary"], size=14),
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            itemsizing="constant",
        ),
        margin=dict(l=4, r=4, t=8, b=4),
        # legend=dict(
        #     bgcolor="rgba(0,0,0,0)",  
        #     orientation="v",
        #     yanchor="top",
        #     y=0.98,
        #     xanchor="left",
        #     x=0.02,
        #     font=dict(size=14),
        #     itemsizing="constant",
        #     #valign='center'
        # )

    )

    return layout


COURT_L_FT = 94.0
COURT_W_FT = 50.0
HALF_DIVIDER = 50.0        # in NCAA x-scale units (0..100)
HOOP_FROM_BASELINE_FT = 5.25
HOOP_X_FT = COURT_L_FT - HOOP_FROM_BASELINE_FT   # 88.75 ft from left baseline


# def standardize_to_right_basket(dff, x_col="x", y_col="y"):
#     """
#     NCAA coords are on a 0..100-ish full court for BOTH axes.
#     Shots on the left half (x < 50) are flipped so that all shots end up
#     on the right half (attacking the same basket).

#     We flip both x and y to preserve left/right orientation.
#     """
#     out = dff.copy()
#     x = out[x_col].astype(float).to_numpy()
#     y = out[y_col].astype(float).to_numpy()

#     left_half = x < HALF_DIVIDER

#     # Flip across full-court axes in the 0..100 coordinate system
#     x[left_half] = 100.0 - x[left_half]
#     y[left_half] = 100.0 - y[left_half]

#     out["x_std"] = x
#     out["y_std"] = y
#     return out

def standardize_to_right_basket(dff, x_col="x", y_col="y"):
    out = dff.copy()
    x = out[x_col].astype(float).to_numpy()
    y = out[y_col].astype(float).to_numpy()

    x2 = x.copy()
    y2 = y.copy()


    # ✅ flip x
    left_half = x < 50
    x2[left_half] = 100.0 - x2[left_half].copy()

    # flip first half shots on other side of court, mirrored at FT nail line
    first_half = (out['period']=='1st Half')
    y2[first_half] = 100.0 - y2[first_half].copy()

    out2 = out.copy()

    out2["x_std"] = x2.copy()
    out2["y_std"] = y2.copy()


    return out2



def to_feet_hoop_centered(dff):
    """
    Convert standardized NCAA coords (0..100) -> feet, and then shift so:
      hoop is at (0, 0)
      x is distance from hoop toward midcourt (negative)
      baseline is at +5.25 ft
    """
    out = dff.copy()

    # NCAA scale: x in [0,100] maps to 94 ft length
    #            y in [0,100] maps to 50 ft width
    x_ft = out["x_std"] * (COURT_L_FT / 100.0)
    y_ft = (out["y_std"] - 50.0) * (COURT_W_FT / 100.0)  # center at 0

    # hoop-centered
    out["x_plot"] = x_ft - HOOP_X_FT
    out["y_plot"] = y_ft
    return out

def rotate_for_display(x, y):
    """
    Rotate coordinates so baseline is at the bottom.
    """
    return y, -x

def rotate_shape(shape):
    """
    Rotate a Plotly layout shape using the same rotation as the shots.
    """
    shape = shape.copy()

    if shape["type"] == "line":
        x0, y0 = rotate_for_display(shape["x0"], shape["y0"])
        x1, y1 = rotate_for_display(shape["x1"], shape["y1"])
        shape.update(x0=x0, y0=y0, x1=x1, y1=y1)

    elif shape["type"] in ("rect", "circle"):
        x0, y0 = rotate_for_display(shape["x0"], shape["y0"])
        x1, y1 = rotate_for_display(shape["x1"], shape["y1"])
        shape.update(x0=min(x0, x1), y0=min(y0, y1),
                     x1=max(x0, x1), y1=max(y0, y1))

    return shape

def load_team_data(team):
    """
    Load shot data for selected team.
    Expected filename format:
    Shot Location Data/{Team}_shot_data_2026.csv
    """
    path = f"Shot Location Data//{team}_shot_data_2026.csv"
    dff = pd.read_csv(path)

    #lineup_col = [col for col in dff if 'lineup' in col][0]
    #dff['lineup'] = dff[lineup_col]

    import ast
    lineup_col = [col for col in dff if 'lineup' in col][0]
    
    dff["lineup"] = (
        dff[lineup_col]
        .dropna()
        .apply(lambda x: tuple(ast.literal_eval(x)) if isinstance(x, str) else tuple(x))
    )


    #print(team)
    #print(dff["team_name"])

    #dff.loc[dff['team_name']=='St. John&#39;s (NY', 'team_name'] = "St. John's (NY)"
    #dff.loc[dff['team_name']=='Miami (FL', 'team_name'] = "Miami (FL)"

    #print(dff.loc[dff['team_name'].str.contains('\&'), 'team_name'].value_counts())

    dff['team_name'] = dff['team_name'].str.replace('&#39;', "'")
    dff['team_name'] = dff['team_name'].str.replace('&amp;', "&")

    dff['shooter'] = dff['shooter'].str.replace('&#39;', "'")
    dff['shooter'] = dff['shooter'].str.replace('&amp;', "&")

    dff.loc[dff['team_name'].str.contains('\('), 'team_name'] = dff.loc[dff['team_name'].str.contains('\('), 'team_name'] + ')'

    dff["offense_defense"] = np.where(
        dff["team_name"] == team, "Offense", "Defense"
    )
    dff["made"] = np.where(dff["result"] == "made", 1, 0)

    dff['nond1'] = np.where(dff['Quad']=='Non-D1', True, False)
    dff['Quad'] = np.where(dff['Quad']=='Quad', 'Q4', dff['Quad'])

    return dff

def polar_wedge(r0, r1, a0, a1, n=40):
    """
    Build a closed polygon (SVG path) for a radial wedge.
    Angles in degrees.
    """
    a_outer = np.linspace(np.radians(a0), np.radians(a1), n)
    a_inner = np.linspace(np.radians(a1), np.radians(a0), n)

    x = np.concatenate([
        r1 * np.cos(a_outer),
        r0 * np.cos(a_inner)
    ])
    y = np.concatenate([
        r1 * np.sin(a_outer),
        r0 * np.sin(a_inner)
    ])

    path = f"M {x[0]:.3f},{y[0]:.3f} "
    for xi, yi in zip(x[1:], y[1:]):
        path += f"L {xi:.3f},{yi:.3f} "
    path += "Z"
    return path



def zone_label_xy(zone):
    if zone == "Rim":
        return (0, -0.15)

    if zone == "Paint (Non-Rim)":
        return (0, 6.95)

    if zone == "Paint (Non-Rim) Right":
        return (-9,-1)
    if zone == "Paint (Non-Rim) Middle":
        return (0, 8.75)
    if zone == "Paint (Non-Rim) Left":
        return (9, -1)

    if zone == "Top Mid":
        return (0, 17.5)
    if zone == "Left Mid":
        return (12.75, 11.5)
    if zone == "Right Mid":
        return (-12.75, 11.5)

    if zone == "Top 3":
        return (0, 26.5)
    if zone == "Left Wing 3":
        return (19.125, 18.125)
    if zone == "Right Wing 3":
        return (-19.125, 18.125)
    if zone == "Right Corner 3":
        return (26.5, 2)
    if zone == "Left Corner 3":
        return (-26.5, 2)

    # ✅ NEW BASELINE ZONES
    if zone == "Left Mid Low":
        return (-17.5, 0)
    if zone == "Right Mid Low":
        return (17.5, 0)

    # Fallback (never crashes)
    return rotate_for_display(0, 0)


def shooting_summary(dff):
    if dff.empty:
        return {
            "fgm": 0,
            "fga": 0,
            "fg_pct": 0,
            "efg": 0,
            "pps": 0,
            "astd_pct": 0,
        }

    fga = dff["shot_id"].nunique()
    fgm = dff["made"].sum()

    threes = dff["is_three"]
    three_made = dff.loc[threes, "made"].sum()

    fg_pct = fgm / fga if fga else 0
    efg = (fgm + 0.5 * three_made) / fga if fga else 0
    pps = (fgm * 2 + three_made) / fga if fga else 0

    made = dff[dff["made"] == 1]
    astd_pct = made["assisted"].fillna(0).sum() / len(made) if len(made) else 0

    return {
        "fgm": fgm,
        "fga": fga,
        "fg_pct": fg_pct,
        "efg": efg,
        "pps": pps,
        "astd_pct": astd_pct,
    }




def team_title_with_logo(team, subtitle=None, logo_src=None):
    return html.Div(
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "gap": "12px",
        },
        children=[
            html.Img(
                src=logo_src,
                style={
                    "height": "60px",
                    "width": "48px",
                    "objectFit": "contain"
                }
            ),
            html.Div(
                [
                    html.Div(
                        team,
                        style={
                            "fontSize": "24px",
                            "fontWeight": 700,
                            "color": THEME["text_primary"]
                        }
                    ),
                    subtitle and html.Div(
                        subtitle,
                        style={
                            "fontSize": "14px",
                            "color": THEME["text_secondary"]
                        }
                    )
                ]
            )
        ]
    )


def chart_title(team, side, logo):
    return (
        f"<span style='display:flex;align-items:center;gap:8px;'>"
        f"<img src='{logo}' style='height:30px;'>"
        f"<span>{team} <u>{side}</u></span>"
        f"</span>"
    )

def chart_header(team, side, logo):
    return html.Div(
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "gap": "8px",
            "fontFamily": "Funnel Display",
            "fontWeight": 600,
            "fontSize": "18px",
            "color":THEME['text_primary']
        },
        children=[
            html.Img(src=logo, style={"height": "30px"}),
            html.Span(f"{side}")
        ]
    )


def stat_card(label, value, subvalue=None):
    return html.Div(
        [
            html.Div(
                label,
                style={
                    "fontSize": "12px",
                    "color": THEME["text_secondary"],
                    "textTransform": "uppercase",
                    "letterSpacing": "0.04em",
                }
            ),
            html.Div(
                value,
                style={
                    "fontSize": "18px",
                    "fontWeight": 600,
                    "color": THEME["text_primary"],
                }
            ),
            subvalue and html.Div(
                subvalue,
                style={
                    "fontSize": "11px",
                    "color": THEME["text_muted"],
                    "marginTop": "6px",
                }
            ),
        ],
        style={
            "background": THEME["bg_card"],
            "borderRadius": "10px",
            "padding": "10px 12px",
            "boxShadow": THEME["shadow_sm"],
            "textAlign": "center",
        }
    )



def stat_row(cards):
    return dbc.Row(
        [dbc.Col(card, xs=3) for card in cards],
        className="g-2 mb-2"
    )


def shot_breakdown_stats(dff):
    total = len(dff)

    def pct(mask):
        att = mask.sum()
        made = dff.loc[mask, "made"].sum()
        return f"{made/att:.1%}" if att else "—"


    # def efg(mask):
    #     three = dff.loc[mask, "3P_made"].sum()
    #     two = dff.loc[mask, "2P_made"].sum()
    #     att = sum(mask)
    #     return ((three * 1.5 + two) / att)
    


    dff = dff.copy()
    dff["dist"] = np.sqrt(dff["x_plot"]**2 + dff["y_plot"]**2)
    dff["angle"] = np.degrees(np.arctan2(dff["y_plot"], -dff["x_plot"]))
    dff["zone"] = dff.apply(assign_zone, axis=1).astype(str)
    # reconcile ONCE
    if "shot_range" in dff.columns:
        dff = reconcile_zone_with_shot_range(dff)


    debug = dff.assign(
        zone_three = dff["zone"].str.contains("3"),
        range_three = dff["is_three"]
    )
    
    # print(
    #     debug.loc[debug.zone_three != debug.range_three,
    #               ["zone", "shot_range", "x_plot", "y_plot"]]
    #     .head(10)
    # )

    # dff['3P'] = np.where(dff['zone'].str.contains('3'), True, False)
    # dff.loc[dff['3P'] & dff['result']=='made', '3P_made']=True
    # dff.loc[~dff['3P'] & dff['result']=='made', '2P_made']=True

    

    print(dff["zone"].value_counts())

    # Rim / Close = rim + non-rim paint
    rim_close = dff["zone"].isin(["Rim"])

    # Midrange ring
    mid_long = dff["zone"].str.contains("Mid")

    # Midrange ring
    mid_short = dff["zone"].str.contains("Paint")

    # Threes
    #three = dff["zone"].str.contains("3")
    three = dff["is_three"]



    left = dff["angle"] < -22
    middle = dff["angle"].between(-22, 22)
    right = dff["angle"] > 22

    rim_f = rim_close.mean() * 100 if total else 0
    mid_long_f = mid_long.mean() * 100 if total else 0
    mid_short_f = mid_short.mean() * 100 if total else 0
    three_f = three.mean() * 100 if total else 0

    left_f = left.mean() * 100 if total else 0
    midline_f = middle.mean() * 100 if total else 0
    right_f = right.mean() * 100 if total else 0

    def ast_pct(mask):
        made = dff.loc[mask & (dff["made"] == 1)]
        if len(made) == 0:
            return "—"
        assisted = made["assisted"].fillna(0).sum()
        return f"{assisted / len(made):.0%}"


    return {
        "fg": [
            ("Rim FG%", pct(rim_close)),
            ("S-Mid FG%", pct(mid_short)),
            ("L-Mid FG%", pct(mid_long)),
            ("3P FG%", pct(three)),
        ],
        "ast": [
            ("Close Ast%", ast_pct(rim_close)),
            ("S-Mid Ast%", ast_pct(mid_short)),
            ("L-Mid Ast%", ast_pct(mid_long)),
            ("3P Ast%", ast_pct(three)),
        ],
        "freq_vals": (rim_f, mid_short_f, mid_long_f, three_f),
}






def freq_bar(labels, values, colors=None):
    if colors is None:
        colors = THEME["freq_colors"]

    return html.Div(
        [
            # --- stacked bar ---
            html.Div(
                [
                    html.Div(
                        style={
                            "width": f"{v:.1f}%",
                            "backgroundColor": c,
                            "height": "100%",
                        }
                    )
                    for v, c in zip(values, colors)
                ],
                style={
                    "display": "flex",
                    "height": "12px",
                    "borderRadius": "6px",
                    "overflow": "hidden",
                    "background": THEME["freq_bg"]
                }
            ),

            # --- legend with colored dots ---
            html.Div(
                [
                    html.Span(
                        "% of shots:",
                        style={"fontWeight": 600, "marginRight": "1px"}
                    ),

                    *[
                        html.Span(
                            [
                                # colored dot
                                html.Span(
                                    "●",
                                    style={
                                        "color": c,
                                        "fontSize": "12px",
                                        "marginRight": "1px",
                                        "lineHeight": "1"
                                    }
                                ),
                                f"{l}: {v:.0f}%"
                            ],
                            style={
                                "margin": "0 3px",
                                "whiteSpace": "nowrap"
                            }
                        )
                        for l, v, c in zip(labels, values, colors)
                    ]
                ],
                style={
                    "fontSize": "12px",
                    "color": THEME["text_secondary"],
                    "marginTop": "10px",
                    "marginLeft": "5px",
                    "display": "flex",
                    "justifyContent": "left",
                    "flexWrap": "wrap",
                    "alignItems": "left"
                }
            )
        ],
        style={
            "background": THEME["bg_card"],
            "boxShadow": THEME["shadow_sm"],
            "borderRadius": "10px",
            "padding": "3px 4px"
        }
    )


def empty_shot_figure(message="No shots match the selected filters"):
    fig = go.Figure(layout=create_half_court_layout())

    fig.add_annotation(
        text=message,
        x=0.5, y=0.8,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(
            size=16,
            color=THEME["text_secondary"],
            family="Funnel Display"
        ),
        align="center"
    )

    fig.update_layout(
        plot_bgcolor=THEME["bg_chart"],
        paper_bgcolor=THEME["bg_chart"]
    )


    return fig


def formatNames(ncaa, col='team_name'):

    ncaa[col] = ncaa[col].str.replace(' St.$', ' State', regex=True)
    ncaa[col] = ncaa[col].str.replace(r'Mississippi Val.', 'Mississippi Valley State')
    ncaa[col] = ncaa[col].str.replace("Miami (FL)", "Miami FL")
    ncaa[col] = ncaa[col].str.replace("LIU", "Long Island")
    ncaa[col] = ncaa[col].str.replace("UNI", "Northern Iowa")
    ncaa[col] = ncaa[col].str.replace("Ark.-Pine Bluff", "Arkansas Pine Bluff")
    ncaa[col] = ncaa[col].str.replace("Ky.", "Kentucky", regex=True)
    ncaa[col] = ncaa[col].str.replace("VMI", "Virginia Military", regex=True)
    ncaa[col] = ncaa[col].str.replace("Saint Mary's (CA)", "Saint Mary's", regex=False)
    ncaa[col] = ncaa[col].str.replace("UIW", "Incarnate Word", regex=True)
    ncaa[col] = ncaa[col].str.replace("Ga.", "Georgia", regex=True)
    ncaa[col] = ncaa[col].str.replace("Fla.", "Florida", regex=True)
    ncaa[col] = ncaa[col].str.replace("St. John's (NY)", "St. John's", regex=False)
    ncaa[col] = ncaa[col].str.replace("UTRGV", "UT Rio Grande Valley", regex=True)
    ncaa[col] = ncaa[col].str.replace("Purdue Fort Wayne", "Purdue FW", regex=True)
    ncaa[col] = ncaa[col].str.replace("Ind.", "Indiana", regex=False)
    ncaa[col] = ncaa[col].str.replace("Mo.", "Missouri", regex=False)
    ncaa[col] = ncaa[col].str.replace("Ala.", "Alabama", regex=False)
    ncaa[col] = ncaa[col].str.replace("FGCU", "Florida Gulf Coast", regex=False)
    ncaa[col] = ncaa[col].str.replace("FDU", "Fairleigh Dickinson", regex=False)
    ncaa[col] = ncaa[col].str.replace("Mich.", "Michigan", regex=False)
    ncaa[col] = ncaa[col].str.replace("Miss.", "Mississippi", regex=False)
    ncaa[col] = ncaa[col].str.replace("Ill.", "Illinois", regex=False)
    ncaa[col] = ncaa[col].str.replace("Caro.", "Carolina", regex=False)
    ncaa[col] = ncaa[col].str.replace("Tenn.", "Tennessee", regex=False)
    ncaa[col] = ncaa[col].str.replace("Ark.", "Arkansas", regex=False)
    ncaa[col] = ncaa[col].str.replace("Colo.", "Colorado", regex=False)
    ncaa[col] = ncaa[col].str.replace("So.", "Southern", regex=False)
    ncaa[col] = ncaa[col].str.replace("La.", "Louisiana", regex=False)
    ncaa[col] = ncaa[col].str.replace("Ariz.", "Arizona", regex=False)
    ncaa[col] = ncaa[col].str.replace("Wash.", "Washington", regex=False)
    ncaa[col] = ncaa[col].str.replace("Conn.", "Connecticut", regex=False)
    ncaa[col] = ncaa[col].str.replace("Southern California", "USC", regex=False)
    ncaa[col] = ncaa[col].str.replace("Bethune-Cookman", "Bethune Cookman", regex=False)
    ncaa[col] = ncaa[col].str.replace("Alcorn", "Alcorn State", regex=False)
    ncaa[col] = ncaa[col].str.replace("Gardner-Webb", "Gardner Webb", regex=False)
    ncaa[col] = ncaa[col].str.replace("A&M-Corpus Christi", "Texas A&M CC", regex=False)
    ncaa[col] = ncaa[col].str.replace("SFA", "Stephen F Austin", regex=False)
    ncaa[col] = ncaa[col].str.replace("UT Martin", "Tennessee Martin", regex=False)
    ncaa[col] = ncaa[col].str.replace("SFA", "Stephen F Austin", regex=False)
    ncaa[col] = ncaa[col].str.replace("UT Martin", "Tennessee Martin", regex=False)
    ncaa[col] = ncaa[col].str.replace("Middle Tennessee", "Middle Tennessee State", regex=False)
    ncaa[col] = ncaa[col].str.replace("UNCW", "UNC Wilmington", regex=False)
    ncaa[col] = ncaa[col].str.replace("Grambling", "Grambling State", regex=False)
    ncaa[col] = ncaa[col].str.replace("Lamar University", "Lamar", regex=False)
    ncaa[col] = ncaa[col].str.replace("Miami (OH)", "Miami OH", regex=False)
    ncaa[col] = ncaa[col].str.replace("California Baptist", "Cal Baptist", regex=False)
    ncaa[col] = ncaa[col].str.replace("LMU (CA)", "Loyola Marymount", regex=False)
    ncaa[col] = ncaa[col].str.replace("Sam Houston", "Sam Houston State", regex=False)
    ncaa[col] = ncaa[col].str.replace("FIU", "Florida International", regex=False)
    ncaa[col] = ncaa[col].str.replace("NIU", "Northern Illinois", regex=False)
    ncaa[col] = ncaa[col].str.replace("Mount St. Mary's", "Mount Saint Mary's", regex=False)
    ncaa[col] = ncaa[col].str.replace("CSU Bakersfield", "Cal State Bakersfield", regex=False)
    ncaa[col] = ncaa[col].str.replace("N.C. A&T", "North Carolina A&T", regex=False)
    ncaa[col] = ncaa[col].str.replace("St. Thomas (MN)", "St. Thomas", regex=False)
    ncaa[col] = ncaa[col].str.replace("East Texas A&M", "Texas A&M Commerce", regex=False)
    ncaa[col] = ncaa[col].str.replace("Boston U.", "Boston U", regex=False)
    ncaa[col] = ncaa[col].str.replace("Prairie View", "Prairie View A&M", regex=False)
    ncaa[col] = ncaa[col].str.replace("Loyola Maryland", "Loyola MD", regex=False)
    ncaa[col] = ncaa[col].str.replace("Cal St. Fullerton", "Cal State Fullerton", regex=False)
    ncaa[col] = ncaa[col].str.replace("Army West Point", "Army", regex=False)
    ncaa[col] = ncaa[col].str.replace("UTSA", "UT San Antonio", regex=False)
    ncaa[col] = ncaa[col].str.replace("App State", "Appalachian State", regex=False)
    ncaa[col] = ncaa[col].str.replace("ETSU", "East Tennessee State", regex=False)
    ncaa[col] = ncaa[col].str.replace("Southern Mississippi", "Southern Miss", regex=False)
    ncaa[col] = ncaa[col].str.replace("UIC", "Illinois Chicago", regex=False)
    ncaa[col] = ncaa[col].str.replace("Massachusetts", "UMass", regex=False)
    ncaa[col] = ncaa[col].str.replace("Seattle U", "Seattle", regex=False)
    ncaa[col] = ncaa[col].str.replace("Southern U.", "Southern", regex=False)
    ncaa[col] = ncaa[col].str.replace("N.C. Central", "North Carolina Central", regex=False)
    ncaa[col] = ncaa[col].str.replace("Southeast Missouri State", "Southeast Missouri", regex=False)
    ncaa[col] = ncaa[col].str.replace("UMES", "Maryland Eastern Shore", regex=False)
    ncaa[col] = ncaa[col].str.replace("Purdue FW", "Purdue Fort Wayne", regex=False)
    ncaa[col] = ncaa[col].str.replace("ULM", "Louisiana Monroe", regex=False)
    ncaa[col] = ncaa[col].str.replace("Queens (NC)", "Queens", regex=False)
    ncaa[col] = ncaa[col].str.replace("UAlbany", "Albany", regex=False)
    ncaa[col] = ncaa[col].str.replace("Col. of Charleston", "Charleston", regex=False)
    ncaa[col] = ncaa[col].str.replace("Georgiadner-Webb", "Gardner Webb", regex=False)
    ncaa[col] = ncaa[col].str.replace("Western Georgia", "West Georgia", regex=False)

    return ncaa


# --------------------------------------------------
# SHOT CHART FUNCTION
# --------------------------------------------------
def make_shot_chart(dff, title):
    fig = go.Figure(layout=create_half_court_layout())

    ax, ay = rotate_for_display(ARC_X, ARC_Y)

    fig.add_trace(go.Scatter(
        x=ax,
        y=ay,
        mode="lines",
        line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
        hoverinfo="skip",
        showlegend=False
    ))


    # Bottom corner (left/right)
    cx1, cy1 = rotate_for_display(
        np.array([-BASELINE_X, BASELINE_X]),
        np.array([-ARC_Y.max(), -ARC_Y.max()])
    )

    cx2, cy2 = rotate_for_display(
        np.array([-BASELINE_X, BASELINE_X]),
        np.array([ARC_Y.max(), ARC_Y.max()])
    )

    fig.add_trace(go.Scatter(
        x=cx1, y=cy1,
        mode="lines",
        line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
        hoverinfo="skip",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=cx2, y=cy2,
        mode="lines",
        line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
        hoverinfo="skip",
        showlegend=False
    ))





    made = dff[dff["made"] == 1]
    miss = dff[dff["made"] == 0]

    # Rotate shot coordinates
    mx, my = rotate_for_display(miss["x_plot"], miss["y_plot"])
    gx, gy = rotate_for_display(made["x_plot"], made["y_plot"])

    fig.add_trace(go.Scattergl(
        x=gx, y=gy,
        mode="markers",
        marker=dict(size=7, color=THEME["make"]),
        name="Make",
        hoverinfo="skip"
    ))
    
    fig.add_trace(go.Scattergl(
        x=mx, y=my,
        mode="markers",
        marker=dict(size=7, color=THEME["miss"]),
        name="Miss",
        hoverinfo="skip"
    ))



    fig.update_layout(
        plot_bgcolor=THEME["bg_chart"],
        paper_bgcolor=THEME["bg_chart"]
    )


    # fig.update_layout(
    #     title=dict(
    #         text=title,
    #         x=0.5,
    #         y=0.98,
    #         font=dict(
    #             family="Funnel Display",
    #             size=20,
    #             weight=600
    #         )
    #     ),
    #     legend=dict(
    #         font=dict(
    #             family="Funnel Display",
    #             size=16
    #         )
    #     ),
    #     font=dict(
    #         family="Funnel Display"
    #     ),
    #     plot_bgcolor="#f8f8f8",
    #     paper_bgcolor="#f8f8f8"
    # )

    # ---- add summary stats on shots view too ----
    dff2 = dff.copy()
    dff2.loc[:, "dist"]  = np.sqrt(dff2["x_plot"]**2 + dff2["y_plot"]**2)
    dff2.loc[:, "angle"] = np.degrees(np.arctan2(dff2["y_plot"], -dff2["x_plot"]))
    dff2.loc[:, "zone"]  = dff2.apply(assign_zone, axis=1)

    # reconcile ONCE
    if "shot_range" in dff2.columns:
        dff2 = reconcile_zone_with_shot_range(dff2)

    #print(shooting_summary(dff2))

    # fg_line, pps_line, astd_line = shooting_summary(dff2)
    # add_chart_subtitle(fig, fg_line, pps_line, astd_line)

    summary = shooting_summary(dff2)

    fg_line  = f"{summary['fg_pct']:.1%} FG · {summary['fgm']}/{summary['fga']}"
    pps_line = f"{summary['efg']:.1%} eFG · {summary['pps']:.3f} pts/shot"
    
    add_chart_subtitle(
        fig,
        fg_line,
        pps_line,
        f"{summary['astd_pct']:.1%} Ast'd"
    )
    add_signature(fig)



    return fig


def make_zone_chart(dff, title):

    fig = go.Figure(layout=create_half_court_layout())

    ax, ay = rotate_for_display(ARC_X, ARC_Y)

    # fig.add_trace(go.Scatter(
    #     x=ax,
    #     y=ay,
    #     mode="lines",
    #     line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
    #     hoverinfo="skip",
    #     showlegend=False
    # )),


    # # Bottom corner (left/right)
    # cx1, cy1 = rotate_for_display(
    #     np.array([-BASELINE_X, BASELINE_X]),
    #     np.array([-ARC_Y.max(), -ARC_Y.max()])
    # )

    # cx2, cy2 = rotate_for_display(
    #     np.array([-BASELINE_X, BASELINE_X]),
    #     np.array([ARC_Y.max(), ARC_Y.max()])
    # )

    # fig.add_trace(go.Scatter(
    #     x=cx1, y=cy1,
    #     mode="lines",
    #     line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
    #     hoverinfo="skip",
    #     showlegend=False
    # ))

    # fig.add_trace(go.Scatter(
    #     x=cx2, y=cy2,
    #     mode="lines",
    #     line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
    #     hoverinfo="skip",
    #     showlegend=False
    # ))

    #dff["dist"] = np.sqrt(dff["x_plot"]**2 + dff["y_plot"]**2)
    #dff["angle"] = np.degrees(np.arctan2(dff["y_plot"], -dff["x_plot"]))
    #dff["zone"] = dff.apply(assign_zone, axis=1)
    dff.loc[:,"dist"] = np.sqrt(dff["x_plot"]**2 + dff["y_plot"]**2)
    dff.loc[:,"angle"] = np.degrees(np.arctan2(dff["y_plot"], -dff["x_plot"]))
    dff.loc[:,"zone"] = dff.apply(assign_zone, axis=1)

    # reconcile ONCE
    if "shot_range" in dff.columns:
        dff = reconcile_zone_with_shot_range(dff)

    zs = (
        dff.groupby("zone")
        .agg(att=("made", "count"), made=("made", "sum"))
        .reset_index()
    )
    zs["pct"] = zs["made"] / zs["att"]

    for _, r in zs.iterrows():
        zone_shape = ZONE_SHAPES[r["zone"]].copy()
        #print(zone_shape)
        zone_shape['line'] = {
            'width': 3,
            'color': THEME["bg_chart"]
        }


        # # Rotate PATH shapes
        # if zone_shape["type"] == "path":
        #     zone_shape["path"] = rotate_path(zone_shape["path"])

        # # Rotate rect / circle using existing helper
        # elif zone_shape["type"] in ("rect", "circle"):
        #     zone_shape = rotate_shape(zone_shape)

        fig.add_shape(
            **zone_shape,
            fillcolor=zone_color(r["pct"], r["zone"]),
            opacity=0.75,
            layer="below"
        )
        
        x_txt, y_txt = zone_label_xy(r["zone"])

        # if r["zone"] != 'Rim':

        #     # Add circle background first
        #     fig.add_trace(go.Scatter(
        #         x=[x_txt],
        #         y=[y_txt],
        #         mode="markers",
        #         marker=dict(
        #             size=48,  # Adjust size to fit your text
        #             color="rgba(255, 255, 255, 0.2)",  # Semi-transparent white
        #             line=dict(
        #                 color=THEME["bg_chart"],  # Border color
        #                 width=1.5  # Border width (thin line)
        #             )
        #         ),
        #         showlegend=False,
        #         hoverinfo='skip'
        #     ))
        
        # Then add text on top
        fig.add_trace(go.Scatter(
            x=[x_txt],
            y=[y_txt],
            text=[f"<span style='line-height: 1.0'>{r.made}/{r.att}<br><span style='font-size: 12px'>{r.pct:.0%}</span></span>"],
            mode="text",
            textfont=dict(
                size=13,
                family="Funnel Display, sans-serif",
                color=THEME["bg_chart"],
                weight=600
            ),
            showlegend=False,
            hoverinfo='skip'
        ))

    fig.update_layout(
        plot_bgcolor=THEME["bg_chart"],
        paper_bgcolor=THEME["bg_chart"]
    )


    fig.update_layout(showlegend=False)

    summary = shooting_summary(dff)

    fg_line  = f"{summary['fg_pct']:.1%} FG · {summary['fgm']}/{summary['fga']}"
    pps_line = f"{summary['efg']:.1%} eFG · {summary['pps']:.3f} pts/shot"
    
    add_chart_subtitle(
        fig,
        fg_line,
        pps_line,
        f"{summary['astd_pct']:.0%} Ast'd"
    )
    add_signature(fig)

    return fig


def assign_zone(row):
    d = row["dist"]      # distance from hoop (ft)
    a = row["angle"]     # angle in degrees
                          # (+ = RIGHT side after rotation)

    # ----------------
    # 1. RIM
    # ----------------
    if d <= R_RIM:
        return "Rim"

    # ----------------
    # 2. PAINT (NON-RIM)
    # ----------------
    #if d <= R_PAINT_EDGE:
    #    return "Paint (Non-Rim)"

    if (d <= R_PAINT_EDGE) & (a < -60):
        return "Paint (Non-Rim) Left"

    if (d <= R_PAINT_EDGE) & (a >= -60) & (a <= 60):
        return "Paint (Non-Rim) Middle"

    if (d <= R_PAINT_EDGE)  & (a > 60):
        return "Paint (Non-Rim) Right"

    # ----------------
    # 3. MIDRANGE (INSIDE 3PT LINE)
    # ----------------
    if d < R_3_EDGE:

        # Baseline midrange (short corner 2s)
        if abs(a) >= ANGLE_CORNER:
            return "Right Mid Low" if a > 0 else "Left Mid Low" # flipped to the other side, which flips both colors and labels. We only want the color to flip

        # Wings
        if abs(a) > ANGLE_WING:
            return "Right Mid" if a > 0 else "Left Mid"

        # Top
        return "Top Mid"

    # ----------------
    # 4. THREES (OUTSIDE 3PT LINE)
    # ----------------
    # Corners
    if abs(a) >= ANGLE_CORNER:
        return "Right Corner 3" if a > 0 else "Left Corner 3"  # flipped to the other side, which flips both colors and labels. We only want the color to flip

    # Wings
    if abs(a) > ANGLE_WING:
        return "Right Wing 3" if a > 0 else "Left Wing 3"

    # Top
    return "Top 3"


def reconcile_zone_with_shot_range(df):
    """
    Ensures mid-range vs 3PT consistency using shot_range.
    Paint/Rim shots are never modified.
    """

    df = df.copy()

    # Normalize shot_range just in case
    df["shot_range"] = (
        df["shot_range"]
        .str.lower()
        .str.replace(" ", "-", regex=False)
    )

    # ----------------------------
    # Case 1: Zone says 3P, range says mid
    # ----------------------------
    mask_false_three = (
        df["zone"].isin(THREE_TO_MID.keys()) &
        (df["shot_range"] == "mid-range")
    )

    df.loc[mask_false_three, "zone"] = (
        df.loc[mask_false_three, "zone"]
        .map(THREE_TO_MID)
    )

    # ----------------------------
    # Case 2: Zone says mid, range says 3P
    # ----------------------------
    mask_false_mid = (
        df["zone"].isin(MID_TO_THREE.keys()) &
        (df["shot_range"] == "3pt")
    )

    df.loc[mask_false_mid, "zone"] = (
        df.loc[mask_false_mid, "zone"]
        .map(MID_TO_THREE)
    )

    return df



def zone_color(pct, zone):
    """
    Returns a color based on zone-specific shooting percentage ranges.
    Darker = better for that shot type.
    """

    family = ZONE_FAMILY.get(zone)

    # fallback (should never hit, but safe)
    if family not in ZONE_PCT_RANGES:
        return sample_colorscale("peach", 0.4)[0]

    lo, hi = ZONE_PCT_RANGES[family]

    # normalize within family range
    t = (pct - lo) / (hi - lo)

    # allow outside range but clip for color stability
    t = np.clip(t, 0.0, 1.0)

    return sample_colorscale("peach", t)[0]



def add_zone_dividers(fig):
    raw_lines = [
        (0, 6, 0, 39),
        (-8, 6, 8, 6),
        (-12, 22, 12, 22),
        (-8, 12, -22, 18),
        (8, 12, 22, 18),
    ]

    for x0, y0, x1, y1 in raw_lines:
        xr0, yr0 = rotate_for_display(x0, y0)
        xr1, yr1 = rotate_for_display(x1, y1)

        fig.add_shape(
            type="line",
            x0=xr0, y0=yr0,
            x1=xr1, y1=yr1,
            line=dict(color=THEME["text_secondary"], width=3),
            layer="above"
        )


import re

def rotate_path(path_str):
    """
    Rotate an SVG path string using rotate_for_display().
    Assumes path consists of M/L/Z commands with x,y pairs.
    """
    tokens = re.findall(r"[MLZ]|-?\d+\.?\d*", path_str)
    out = []

    i = 0
    cmd = None

    while i < len(tokens):
        tok = tokens[i]

        if tok in ("M", "L", "Z"):
            cmd = tok
            out.append(tok)
            i += 1
            continue

        # numeric x,y pair
        x = float(tok)
        y = float(tokens[i + 1])

        xr, yr = rotate_for_display(x, y)
        out.append(f"{xr:.3f}")
        out.append(f"{yr:.3f}")

        i += 2

    return " ".join(out)

def add_chart_subtitle(fig, fg_line, pps_line, astd_line):
    # closer to title (title is at y=0.98)
    y1 = 0.99
    y2 = 0.94
    y3 = 0.89

    common_font = dict(
        family="Funnel Display",
        color=THEME["text_secondary"]
    )

    fig.add_annotation(
        x=0.99, y=y1,
        xref="paper", yref="paper",
        text=fg_line,           # no bold
        showarrow=False,
        font=dict(**common_font, size=13),
        align="right"
    )

    fig.add_annotation(
        x=0.99, y=y2,
        xref="paper", yref="paper",
        text=pps_line,
        showarrow=False,
        font=dict(**common_font, size=13),
        align="right"
    )

    fig.add_annotation(
            x=0.99, y=y3,
            xref="paper", yref="paper",
            text=astd_line,
            showarrow=False,
            font=dict(**common_font, size=13),
            align="right"
        )
    

def add_signature(fig):
    # closer to title (title is at y=0.98)
    y1 = 0
    common_font = dict(
        family="Funnel Display",
        color=THEME["text_secondary"]
    )
    fig.add_annotation(
        x=0, y=y1,
        xref="paper", yref="paper",
        text='cbbshotcharts.com',           # no bold
        showarrow=False,
        font=dict(**common_font, size=11),
        align="left"
    )

SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}

def last_name_clean(name):
    parts = name.replace(",", "").split()
    if parts[-1].lower() in SUFFIXES:
        return parts[-2]
    return parts[-1]

def format_lineup_label(lineup):
    last_names = [last_name_clean(p) for p in lineup]
    return " · ".join(last_names)


def lineup_key(lineup):
    """Stable string key for Dash dropdown"""
    return "|".join(lineup)

def parse_lineup_key(key):
    return tuple(key.split("|"))


# --------------------------------------------------
# DASH APP
# --------------------------------------------------
app = Dash(__name__, 
           title="CBB Shot Charts",
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for Render

# --------------------------------------------------
# DROPDOWN OPTIONS
# --------------------------------------------------
# player_options = [{"label": p, "value": p} for p in sorted(df[PLAYER_COL].dropna().unique())]
# half_options = [{"label": h, "value": h} for h in sorted(df[HALF_COL].dropna().unique())]
# opp_options = [{"label": o, "value": o} for o in sorted(df[OPP_COL].dropna().unique())]
team_options = [
    {"label": t, "value": t}
    for t in sorted(team_p5)
]


# --------------------------------------------------
# LAYOUT (MOBILE-FIRST)
# --------------------------------------------------
app.layout = dbc.Container(
    fluid=True,
    style={
        "backgroundColor": THEME["bg_app"],#"#ededed",
        "minHeight": "100vh",
        "paddingBottom": "40px",
       # "fontFamily": "'Funnel Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    },

    children=[
        
        # html.Link(
        #     rel="stylesheet",
        #     href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&family=Saira+Condensed:wght@100;200;300;400;500;600;700;800;900&display=swap"
        # ),

        dbc.Row(
            dbc.Col(
                [
                    html.H3(
                        [
                            "CBB Shot Charts ",
                            html.Span(
                                "BETA",
                                style={
                                    "backgroundColor": "#a32fba",
                                    "color":THEME['text_primary'],
                                    "fontSize": "11px",
                                    "fontWeight": 700,
                                    "padding": "3px 8px",
                                    "borderRadius": "999px",
                                    "marginLeft": "8px",
                                    "verticalAlign": "middle",
                                    "letterSpacing": "0.06em",
                                }
                            )
                        ],
                        className="text-center",
                        style={
                            "marginBottom": "1px",
                            "marginTop": "4px",
                            "marginLeft": "24px",
                            "display": "flex",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "gap": "6px",
                            "color":THEME['text_primary']
                        }
                    ),
                    html.Div(
                        "Games thru Jan. 25",
                        className="text-center",
                        style={
                            "fontSize": "12.5px",
                            "color": THEME["text_secondary"],
                            "marginTop": "0",
                        }
                    ),
                ],
                #style={
                #    "margin": "0",
                #    "padding": "0",
                #}
            )
        ),

        html.Hr(style={
                "borderColor": THEME["divider"],
                "opacity": 1,
                "margin": "12px 0"
            }),




        dbc.Row(dbc.Col(
            html.Div(id="title-text", className="my-3", style={"margin": "0"}),
            style={"margin": "0"}
        )),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="team-dd",
                    options=team_options,
                    value="Wisconsin",
                    clearable=False,
                    placeholder="Select team",
                    style={
                        "maxWidth": "360px",
                        "margin": "0 auto",
                        "backgroundColor": THEME["bg_dropdown"],
                        "color": THEME["text_primary"],
                        "boxShadow": THEME["shadow_md"],
                        "borderRadius": "10px",
                        "fontWeight": "600",
                                            }
                ),
                width=12
            ),
            className="mb-4"
        ),

        #html.Br(),

        dbc.Row(
            dbc.Col(
                html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="player-dd",
                                                multi=True,
                                                placeholder="Shooter",
                                                style={
                                                    "fontSize": "14px",
                                                    "backgroundColor": THEME["bg_dropdown"],
                                                    "color": THEME["text_primary"],
                                                    "boxShadow": THEME["shadow_md"],
                                                    "borderRadius": "10px",
                                                    "fontWeight": "600",
                                                },
                                            ),
                                            xs=12, md=4
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="half-dd",
                                                multi=True,
                                                placeholder="Half",
                                                style={
                                                    "fontSize": "14px",
                                                    "backgroundColor": THEME["bg_dropdown"],
                                                    "color": THEME["text_primary"],
                                                    "boxShadow": THEME["shadow_md"],
                                                    "borderRadius": "10px",
                                                    "fontWeight": "600",
                                                },
                                            ),
                                            xs=6, md=2
                                        ),
                                        
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="quad-dd",
                                                options=['Q1A', 'Q1B', 'Q2', 'Q3', 'Q4'],
                                                multi=True,
                                                placeholder="Quad",
                                                style={
                                                    "fontSize": "14px",
                                                    "backgroundColor": THEME["bg_dropdown"],
                                                    "color": THEME["text_primary"],
                                                    "boxShadow": THEME["shadow_md"],
                                                    "borderRadius": "10px",
                                                    "fontWeight": "600",
                                                },
                                            ),
                                            xs=6, md=2
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="opp-dd",
                                                multi=True,
                                                placeholder="Opponent",
                                                style={
                                                    "fontSize": "14px",
                                                    "backgroundColor": THEME["bg_dropdown"],
                                                    "color": THEME["text_primary"],
                                                    "boxShadow": THEME["shadow_md"],
                                                    "borderRadius": "10px",
                                                    "fontWeight": "600",
                                                },
                                            ),
                                            xs=6, md=2
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="loc-dd",
                                                options=['Home', 'Away', 'Neutral'],
                                                multi=True,
                                                placeholder="Location",
                                                style={
                                                    "fontSize": "14px",
                                                    "backgroundColor": THEME["bg_dropdown"],
                                                    "color": THEME["text_primary"],
                                                    "boxShadow": THEME["shadow_md"],
                                                    "borderRadius": "10px",
                                                    "fontWeight": "600",
                                                },
                                            ),
                                            xs=6, md=2
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                dbc.Checkbox(
                                                    id="exclude-non-d1",
                                                    label="Exclude games vs non-D1",
                                                    inputStyle={
                                                        "marginRight": "8px",
                                                        
                                                        "transform": "scale(1.25)",   # 🔹 increase checkbox size
                                                        "cursor": "pointer",
                                                        "color":'black'
                                                    },
                                                    labelStyle={
                                                        "cursor": "pointer"
                                                    },
                                                    value=True,   # ✅ default checked
                                                    #inputStyle={"marginRight": "8px"},
                                                ),
                                                style={
                                                    "display": "flex",
                                                    "alignItems": "center",
                                                    "justifyContent": "center",
                                                    "gap": "6px",
                                                    "fontSize": "14px",
                                                    "color": THEME["text_secondary"],
                                                    "marginBottom": "5px",
                                                    "marginTop": "10px",
                                                }
                                            ),
                                            xs=12
                                        ),
                                        dbc.Accordion(
                                                    [
                                                        dbc.AccordionItem(
                                                            dcc.Dropdown(
                                                                id="lineup-dd",
                                                                multi=False,
                                                                placeholder="Select 5-man lineup",
                                                                style={
                                                                    "fontSize": "14px",
                                                                    "backgroundColor": THEME["bg_dropdown"],
                                                                    "color": THEME["text_secondary"],
                                                                    #"boxShadow": THEME["shadow_md"],
                                                                    "borderRadius": "10px",
                                                                    "fontWeight": "600",
                                                                },
                                                                optionHeight=52,
                                                            ),
                                                            title="5-Man Lineups",
                                                        )
                                                    ],
                                                    start_collapsed=True,
                                                    flush=True,
                                                    style={
                                                        "overflow": "visible",
                                                        "marginTop": "6px",
                                                        #"overflow": "visible",
                                                        "backgroundColor": THEME["bg_dropdown"],
                                                        "color": THEME["text_secondary"],
                                                        "boxShadow": THEME["shadow_md"],
                                                        #"borderRadius": "10px",
                                                        "fontWeight": "600",
                                                    }
                                                ),

                                                dbc.Accordion(
                                                    [
                                                        dbc.AccordionItem(
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            html.Div(
                                                                                "Get shots while players are ON or OFF the court",
                                                                                style={
                                                                                    "fontSize": "13px",
                                                                                    "fontWeight": 600,
                                                                                    "color": THEME["text_secondary"],
                                                                                    "marginBottom": "8px",
                                                                                    "textAlign": "center"
                                                                                }
                                                                            ),
                                                                            dcc.Dropdown(
                                                                                id="on-court-dd",
                                                                                multi=True,
                                                                                placeholder="Player(s) ON court",
                                                                                style={
                                                                                    "fontSize": "14px",
                                                                                    "backgroundColor": THEME["bg_dropdown"],
                                                                                    "color": THEME["text_secondary"],
                                                                                    #"boxShadow": THEME["shadow_md"],
                                                                                    "borderRadius": "10px",
                                                                                    "fontWeight": "600",
                                                                                },
                                                                            ),
                                                                        ],
                                                                        xs=12,
                                                                        md=6,
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            # html.Div(
                                                                            #     "",
                                                                            #     style={
                                                                            #         "fontSize": "12px",
                                                                            #         "fontWeight": 600,
                                                                            #         "color": THEME["text_secondary"],
                                                                            #         "marginBottom": "10px",
                                                                            #         "textAlign": "center"
                                                                            #     }
                                                                            # ),
                                                                            dcc.Dropdown(
                                                                                id="off-court-dd",
                                                                                multi=True,
                                                                                placeholder="Player(s) OFF court",
                                                                                style={
                                                                                    "fontSize": "14px",
                                                                                    "backgroundColor": THEME["bg_dropdown"],
                                                                                    "color": THEME["text_primary"],
                                                                                    #"boxShadow": THEME["shadow_md"],
                                                                                    "borderRadius": "10px",
                                                                                    "fontWeight": "600",
                                                                                },
                                                                            ),
                                                                        ],
                                                                        xs=12,
                                                                        md=6,
                                                                    ),
                                                                ],
                                                                className="g-2",
                                                            ),
                                                            title="On / Off",
                                                        )
                                                    ],
                                                    start_collapsed=True,
                                                    flush=True,
                                                    style={
                                                        "overflow": "visible",
                                                        "marginTop": "12px",
                                                        #"overflow": "visible",
                                                        "backgroundColor": THEME["bg_dropdown"],
                                                        "color": THEME["text_secondary"],
                                                        "boxShadow": THEME["shadow_md"],
                                                        #"borderRadius": "10px",
                                                        "fontWeight": "600",
                                                    }
                                                ),


                                        html.Br(),
                                    ],
                                    className="g-2"
                                ),
                                title="Filters",
                            )
                        ],
                        start_collapsed=True,
                        flush=True,
                        className="filters-accordion",
                        style={# "maxWidth": "300px",   # mobile default
                                "margin": "0 auto",
                                #"borderRadius": "10px",
                                "boxShadow": "0 6px 18px rgba(0,0,0,0.22)",
                                "borderRadius": "14px",
                                "backgroundColor": THEME['bg_panel'],}
                    ),
                    className="filters-wrap mb-3",
                    style={
                        #"maxWidth": "800px",   # mobile default
                        "margin": "0 auto",
                        "boxShadow": THEME["shadow_md"],#"0 6px 18px rgba(0,0,0,0.22)",
                        "borderRadius": "14px",
                        "backgroundColor": THEME['bg_panel'],
                         #"borderRadius": "10px",
                        #"overflow": "auto",   # 🔴 REQUIRED for rounding to clip children
                    }
                ),
                xs=9, md=9
            ), 
            
            justify='center'
        ),




        dbc.RadioItems(
            id="view-mode",
            options=[
                {"label": "Zones", "value": "zones"},
                {"label": "Shots", "value": "shots"},
            ],
            value="zones",
            inline=True,
            #button=True,
            className="d-flex justify-content-center mb-2",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-dark px-4 py-2",
            labelCheckedClassName="btn btn-dark shadow"
        ),

        #html.Br(),

        # html.Div(
        #     dbc.Checkbox(
        #         id="show-shot-stats",
        #         label="Show shot stats",
        #         value=True,
        #         inputStyle={
        #             "marginRight": "10px",
        #             "transform": "scale(1.5)",   # 🔹 increase checkbox size
        #             "cursor": "pointer",
        #             "color":'black'
        #         },
        #         labelStyle={
        #             "cursor": "pointer"
        #         }
        #     ),
        #     style={
        #         "display": "flex",
        #         "alignItems": "center",
        #         "justifyContent": "center",
        #         "gap": "6px",
        #         "fontSize": "16px",
        #         "color": THEME["text_secondary"],
        #         "marginBottom": "2px",
        #         "marginTop": "18px",

        #     }
        # ),




        html.Hr(style={
            "borderColor": THEME["divider"],
            "opacity": 1,
            "margin": "12px 0"
        }),



        dbc.Row(
                [
                    dbc.Col([
                        html.Div(id="offense-title", className="text-center mb-2"),
                        html.Div(
                            dcc.Loading(
                                id="loading-2",
                                type="cube",             # Spinner type
                                color="#a32fba",       # Spinner color (can use your THEME colors)
                                fullscreen=False,        # Set to True for fullscreen overlay
                                parent_style={},         # Style the loading container
                                style={},                # Style the spinner itself
                                className="",            # Add custom CSS class
                                debug=False,             # Show loading state in console
                                children=[
                                dcc.Graph(
                                    id="offense-chart",
                                    config={"displayModeBar": False,
                                            "scrollZoom": False},
                                    style={
                                        "height": "40vh",
                                        "minHeight": "270px",
                                        #"paper_bgcolor":"#f8f8f8",
                                        #"plot":"#f8f8f8",
                                    }
                                )]
                            ),
                            style={
                                "background": THEME["bg_panel"],
                                "borderRadius": "14px",
                                "boxShadow": THEME["shadow_lg"],
                                "padding": "5px"
                            }
                        ),
                        html.Div(id="offense-shot-stats", className="mt-2"),
                        ],
                        xs=12, md=6,
                    ),

                    dbc.Col([
                        html.Div(id="defense-title", className="text-center mb-2"),
                        html.Div(
                            dcc.Loading(
                                id="loading-1",
                                type="cube",             # Spinner type
                                color="#a32fba",       # Spinner color (can use your THEME colors)
                                fullscreen=False,        # Set to True for fullscreen overlay
                                parent_style={},         # Style the loading container
                                style={},                # Style the spinner itself
                                className="",            # Add custom CSS class
                                debug=False,             # Show loading state in console
                                children=[
                                    dcc.Graph(
                                    id="defense-chart",
                                    config={"displayModeBar": False},
                                    style={
                                        "height": "40vh",
                                        "minHeight": "270px",
                                    # "paper_bgcolor":"#f8f8f8",
                                        #"plot":"#f8f8f8",
                                    }
                                    )
                                ],  
                                
                            ),
                            style={
                                "background": THEME["bg_panel"],
                                "borderRadius": "14px",
                                "boxShadow": THEME["shadow_lg"],
                                "padding": "5px"
                            }
                        ),
                        html.Div(id="defense-shot-stats", className="mt-2"),
                        ],
                        xs=12, md=6,
                    ),
                ],
                className="gy-4"   # 👈 adds vertical spacing on mobile
            ),

            html.Br(),
            html.Hr(style={
                "borderColor": THEME["divider"],
                "opacity": 1,
                "margin": "12px 0"
            }),

            html.Div(
                [
                    html.Span(
                        "Data source: ",
                        style={"marginRight": "4px"}
                    ),
                    html.A(
                        "stats.ncaa.org",
                        href="https://stats.ncaa.org/",
                        target="_blank",
                        style={"marginRight": "4px"}
                    ),

                    html.Span("•", style={"margin": "0 8px"}),

                    html.Span(
                        "Built by ",
                        style={"marginRight": "4px"}
                    ),
                    html.A(
                        "@smur_cbb",
                        href="https://x.com/smur_cbb",
                        target="_blank"
                    )
                ],
                style={
                    "textAlign": "center",
                    "fontSize": "12px",
                    "color": THEME["text_muted"],
                    "paddingBottom": "12px"
                }
            ),

            html.Br(),



])


# --------------------------------------------------
# CALLBACK
# --------------------------------------------------
@app.callback(
    Output("offense-chart", "figure"),
    Output("defense-chart", "figure"),
    Output("title-text", "children"),
    Output("offense-title", "children"),
    Output("defense-title", "children"),
    Output("offense-shot-stats", "children"),
    Output("defense-shot-stats", "children"),
    

    Input("team-dd", "value"),
    Input("view-mode", "value"),
    Input("player-dd", "value"),
    Input("half-dd", "value"),
    Input("opp-dd", "value"),
    Input("loc-dd", "value"),
    Input("quad-dd", "value"),
    #Input("show-shot-stats", "value"),
    Input("exclude-non-d1", "value"),
    Input("lineup-dd", "value"),
    Input("on-court-dd", "value"),
    Input("off-court-dd", "value"),



)

def update_charts(team, view_mode, players, halves, opps, loc, quad,
                  #show_stats,
                  exclude_non_d1, lineup,
                  on_players, off_players):

    off_title = "Offense"
    def_title = "Defense"

    # Load correct team file
    dff = load_team_data(team)
    #print("players input:", players)


    
    # exclude non-D1 opponents if checked
    if exclude_non_d1:
        dff = dff[dff["nond1"] == False]

    if lineup:
        lineup_tuple = set(parse_lineup_key(lineup))
        dff = dff[
            dff["lineup"].apply(lambda x: isinstance(x, tuple) and set(x) == lineup_tuple)
        ]

    # --------------------------------------------------
    # ON / OFF COURT FILTER
    # --------------------------------------------------
    if on_players:
        on_set = set(on_players)
        dff = dff[
            dff["lineup"].apply(
                lambda lu: isinstance(lu, tuple) and on_set.issubset(set(lu))
            )
        ]
    
    if off_players:
        off_set = set(off_players)
        dff = dff[
            dff["lineup"].apply(
                lambda lu: isinstance(lu, tuple) and off_set.isdisjoint(set(lu))
            )
        ]







    # REMOVE FREE THROWS
    if "shot_range" in dff.columns:
        #print("Dup shot id", dff['shot_id'].duplicated().sum())
        dff = dff[~dff["shot_range"].str.lower().isin(["freethrow"])]
        dff = dff.drop_duplicates(subset=['shot_id'])
        # after FT removal & dedupe
        dff["is_three"] = dff["shot_range"].str.lower().eq("3pt")
        #dff = dff.drop_duplicates(subset=['shooter', 'clock', 'game_id'])
        #print("Dup shot id", dff[['shooter', 'clock', 'game_id']].duplicated().sum())


    

    


    #print("Missing quad 1:", dff['Quad'].isna().sum())

    dff.loc[dff['Quad'].isna(), 'Quad'] = 'Q4'
    dff.loc[dff['Quad'].str.strip()=='', 'Quad'] = 'Q4'

    #print("Missing quad 2:", dff['Quad'].isna().sum())

    dff['opponent'] = dff['opponent'].fillna('Non-D1')

    LOGO_DF['Team'] = LOGO_DF['Team'].str.strip()
    temp = pd.DataFrame([team], columns=['tm'])
    temp2 = formatNames(ncaa=temp, col='tm')

    team_logo_str = temp2['tm'].iloc[0]
    #print(team_logo_str)

    team_logo_str = re.sub(' State$', ' St.', team_logo_str)
    #team_logo_str = re.sub('West Georgia', ' St.', team_logo_str)


    team_logo = LOGO_DF.loc[LOGO_DF["Team"] == team_logo_str, "Logo"]

    


    
    try: team_logo = team_logo.iloc[0]
    except: team_logo = "logos/unknown.png"

    if team == 'Miami (FL)': team_logo = "logos/Miami-FL-Hurricanes.png"
    elif team == 'Boston U.': team_logo = "logos/Boston-U-Terriers.png"
    elif team == 'California Baptist': team_logo = "logos/Cal-Baptist-Lancers.png"
    elif team == 'FIU': team_logo = "logos/Florida-International-Panthers.png"
    elif team == 'West Virginia': team_logo = "logos/west-virginia-mountaineers.png"
    elif team == 'Southeast Mo. St.': team_logo = "logos/southeast-missouri-state-redhawks.png"
    elif team == 'Purdue Fort Wayne': team_logo = "logos/Purdue-FW-Mastodons.png"
    elif team == 'Saint Francis': team_logo = "logos/saint-francis-pa-red-flash.png"
    elif team == 'Little Rock': team_logo = "logos/little-rock-trojans.png"
    elif team == 'San Diego': team_logo = "logos/San-Diego-Toreros.png"
    elif team == 'George Washington': team_logo = "logos/George-Washington-Revolutionaries.png"
    elif team == 'New Haven': team_logo = "logos/new-haven-chargers.png"
    elif team == 'St. Bonaventure': team_logo = "logos/Saint-Bonaventure-Bonnies.png"
    elif team == 'Hawaii': team_logo = "logos/Hawaii-Rainbow-Warriors.png"
    elif team == 'Southern Ind.': team_logo = "logos/Southern-Indiana-Screaming-Eagles.png"
    elif team == 'Lindenwood': team_logo = "logos/Lindenwood-Lions.png"
    elif team == 'Le Moyne': team_logo = "logos/Le-Moyne-Dolphins.png"
    elif team == 'St. Thomas \(MN\)': team_logo = "logos/st-thomas-mn-tommies.png"
    elif team == "Mount St. Mary's": team_logo = "logos/mount-saint-marys-mountaineers.png"
    elif team == 'Lehigh': team_logo = "logos/lehigh-mountain-hawks.png"
    elif team == 'West Ga.': team_logo = "logos/west-georgia-wolves.png"
    elif team == 'NC State': team_logo = "logos/NC-State-Wolfpack.png"
    elif team == 'UC San Diego': team_logo = "logos/UC-San-Diego-Tritons.png"
    elif team == 'UAB': team_logo = "logos/UAB-Blazers.png" 
    elif team == 'St. Bonaventure': team_logo = "logos/St.-Bonaventure-Bonnies.png"
    elif team == 'UMass Lowell': team_logo = "logos/UMass-Lowell.png"
    elif team == 'UIC': team_logo = "logos/Illinois-Chicago-Flames.png"
    elif team == 'UNC Greensboro': team_logo = "logos/UNCG.png"
    elif team == 'Loyola Maryland': team_logo = "logos/Loyola-Maryland-Greyhounds.png"
    elif team == 'UNCW': team_logo = "logos/UNC-Wilmington-Seahawks.png"
    elif team == 'UC Davis': team_logo = "logos/UC-Davis-Aggies.png"
    elif team == 'CSUN': team_logo = "logos/Cal-State-Northridge-Matadors.png"
    elif team == 'Milwaukee': team_logo = "logos/UW-Milwaukee-Panthers.png"
    elif team == 'Nicholls': team_logo = "logos/Nicholls-State-Colonels.png"
    elif team == 'Kansas City': team_logo = "logos/Kansas-City-Roos.png"
    elif team == 'IU Indy': team_logo = "logos/IU-indy-jaguars.png"
    elif team == 'Michigan': team_logo = "logos/michigan-wolverines.png"
    elif team == 'McNeese': team_logo = "logos/Mcneese-State-Cowboys.png"
    elif team == 'Miami (OH)': team_logo = "logos/Miami-Ohio-Redhawks.png"
    #elif team == 'St. John\'s \(NY\)': team_logo = "logos/St.-John's-Red-Storm.png"
    elif team == 'App State': team_logo = "logos/app-state-mountaineers.png"
    elif team == 'SIUE': team_logo = "logos/SIUE.png"
        
    if pd.isna(team_logo) or team_logo == "": team_logo = "/assets/logos/unknown.png"
    else: team_logo = f"/assets/{team_logo}"

    #print(team_logo)
    #print('\n---\n')

    # if players: 
    #     dff = dff[dff[PLAYER_COL].isin(players)]
    #     off_title = off_title + ' - ' + ', '.join(players)
    #     def_title = def_title + ' - ' + ', '.join(players)

    
    if halves: 
        dff = dff[dff[HALF_COL].isin(halves)]
        off_title = off_title + ' | ' + ', '.join(halves)
        def_title = def_title + ' | ' + ', '.join(halves)

    
    if opps: 
        dff = dff[dff[OPP_COL].isin(opps)]
        off_title = off_title + ' | Against: ' + ', '.join(opps)
        def_title = def_title + ' | Against: ' + ', '.join(opps)

    
    if loc: 
        dff = dff[dff['loc'].isin(loc)]
        off_title = off_title + ' | ' + ', '.join(loc) + ' games'
        def_title = def_title + ' | ' + ', '.join(loc) + ' games'

    
    if quad: 
        dff = dff[dff['Quad'].isin(quad)]
        off_title = off_title + ' | ' + ', '.join(quad) + ' games'
        def_title = def_title + ' | ' + ', '.join(quad) + ' games'
            
        off_title = re.sub('Q1A, Q1B', 'Q1', off_title)
        def_title = re.sub('Q1A, Q1B', 'Q1', def_title)
        off_title = re.sub('Q1A, Q2, Q1B', 'Q1, Q2', off_title)
        def_title = re.sub('Q1A, Q2, Q1B', 'Q1, Q2', def_title)

        off_title = re.sub('Q1B, Q1A', 'Q1', off_title)
        def_title = re.sub('Q1B, Q1A', 'Q1', def_title)
        off_title = re.sub('Q1B, Q2, Q1A', 'Q1, Q2', off_title)
        def_title = re.sub('Q1B, Q2, Q1A', 'Q1, Q2', def_title)


    if on_players:
        off_title += f" | ON: {', '.join(on_players)}"
        def_title += f" | ON: {', '.join(on_players)}"

    if off_players:
        off_title += f" | OFF: {', '.join(off_players)}"
        def_title += f" | OFF: {', '.join(off_players)}"

    # --------------------------------------------------
    # LINEUP TITLE ANNOTATION
    # --------------------------------------------------
    if lineup:
        lineup_tuple = parse_lineup_key(lineup)
        lineup_label = format_lineup_label(lineup_tuple)
    
        off_title += f" | Lineup: {lineup_label}"
        def_title += f" | Lineup: {lineup_label}"


    

    # --------------------------------------------------
    # 🚨 SAFEGUARD: no shots after filtering
    # --------------------------------------------------
    if dff.empty:
        empty_fig = empty_shot_figure()

        return (
            empty_fig,
            empty_fig,
            team_title_with_logo(team, "Shot Charts", team_logo),
            chart_header(team, "Offense", team_logo),
            chart_header(team, "Defense", team_logo),
            [],   # no offense stats
            []    # no defense stats
        )



    dff = standardize_to_right_basket(dff, x_col="x", y_col="y")
    dff = to_feet_hoop_centered(dff)

    off_df = dff[dff[OFF_DEF_COL] == "Offense"]
    def_df = dff[dff[OFF_DEF_COL] == "Defense"]

    # --------------------------------------------------
    # SHOOTER FILTER (apply per-side)
    # --------------------------------------------------
    if players:
        # normalize just in case
        players = [p.strip() for p in players if isinstance(p, str)]
    
        off_players = [p for p in players if p in set(off_df[PLAYER_COL].dropna().unique())]
        def_players = [p for p in players if p in set(def_df[PLAYER_COL].dropna().unique())]
    
        if off_players:
            off_df = off_df[off_df[PLAYER_COL].isin(off_players)]
            off_title += " | Shots by " + ", ".join(off_players)
    
        if def_players:
            def_df = def_df[def_df[PLAYER_COL].isin(def_players)]
            def_title += " - " + ", ".join(def_players)


        if off_df.empty and def_df.empty:
            empty_fig = empty_shot_figure()
            return (
                empty_fig,
                empty_fig,
                team_title_with_logo(team, "Shot Charts", team_logo),
                chart_header(team, "Offense", team_logo),
                chart_header(team, "Defense", team_logo),
                [],
                []
            )
        
        if off_df.empty:
            fig_off = empty_shot_figure("No OFFENSE shots match filters")
        else:
            fig_off = make_shot_chart(off_df, chart_title(team, "Offense", team_logo)) if view_mode=="shots" else make_zone_chart(off_df, chart_title(team, "Offense", team_logo))
        
        if def_df.empty:
            fig_def = empty_shot_figure("No DEFENSE shots match filters")
        else:
            fig_def = make_shot_chart(def_df, chart_title(team, "Defense", team_logo)) if view_mode=="shots" else make_zone_chart(def_df, chart_title(team, "Defense", team_logo))

        # If they picked only team shooters, don't change defense title at all
        # If they picked only opponent shooters, offense title stays unchanged


    if view_mode == "shots":
        fig_off = make_shot_chart(off_df, chart_title(team, "Offense", team_logo))
        fig_def = make_shot_chart(def_df, chart_title(team, "Defense", team_logo))
    else:
        fig_off = make_zone_chart(off_df, chart_title(team, "Offense", team_logo))
        fig_def = make_zone_chart(def_df, chart_title(team, "Defense", team_logo))

    fig_off.update_layout(
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        dragmode=False
    )
    fig_def.update_layout(
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        dragmode=False
    )

    # if not show_stats:
    #     # if players:

    #     #     return (
    #     #         fig_off,
    #     #         fig_def,
    #     #         team_title_with_logo(team, "Shot Charts", team_logo),
    #     #         chart_header(team, "Offense" + ' - ' + ', '.join(players), team_logo),
    #     #         chart_header(team, "Defense" + ' - ' + ', '.join(players), team_logo),
    #     #         [],
    #     #         []
    #     #     )
    #     # else:
    #     #     return (
    #     #     fig_off,
    #     #     fig_def,
    #     #     team_title_with_logo(team, "Shot Charts", team_logo),
    #     #     chart_header(team, "Offense", team_logo),
    #     #     chart_header(team, "Defense", team_logo),
    #     #     [],
    #     #     []
    #     #     )
    #     return (
    #         fig_off,
    #         fig_def,
    #         team_title_with_logo(team, "Shot Charts", team_logo),
    #         chart_header(team, off_title, team_logo),
    #         chart_header(team, def_title, team_logo),
    #         [],
    #         []
    #         )


    stats = shot_breakdown_stats(off_df)

    show_stats_out_off = [

        html.Div(
            "Shot Range",
            style={
                "textAlign": "center",
                "fontSize": "13px",
                "fontWeight": 600,
                "color": THEME["text_secondary"],
                "marginBottom": "6px",
                "letterSpacing": "0.04em",
                "textTransform": "uppercase"
            }
        ),

        # stat_row([stat_card(*s) for s in stats["fg"]]),
        # html.Div(style={"height": "6px"}),
        # stat_row([stat_card(*s) for s in stats["ast"]]),

        stat_row(
            [
                stat_card(
                    label=fg_label,
                    value=fg_val,
                    subvalue=f"{ast_val} Ast'd" if ast_val != "—" else "—"
                )
                for (fg_label, fg_val), (_, ast_val)
                in zip(stats["fg"], stats["ast"])
            ]
        ),


        

        freq_bar(
            ["Rim", "S-Mid","L-Mid", "3P"],
            stats["freq_vals"]
        ),

        html.Hr(style={
            "borderColor": THEME["divider"],
            "opacity": 1,
            "margin": "12px 0"
        }),
        # html.Div(
        #     "Court Thirds",
        #     style={
        #         "textAlign": "center",
        #         "fontSize": "13px",
        #         "fontWeight": 600,
        #         "color": THEME["text_secondary"],
        #         "marginBottom": "6px",
        #         "letterSpacing": "0.04em",
        #         "textTransform": "uppercase"
        #     }
        # ),


        # stat_row([stat_card(*s) for s in stats["side_fg"]]),

        # html.Div(style={"height": "6px"}),

        # freq_bar(
        #     ["Left", "Middle", "Right"],
        #     stats["side_freq_vals"]
        # ),
    ]

    
    # show_stats_out_off =[
    #         stat_row([stat_card(*s) for s in stats["fg"]]),
    #         stat_row([stat_card(*s) for s in stats["freq"]]),
    #         stat_row([stat_card(*s) for s in stats["side_fg"]]),
    #         stat_row([stat_card(*s) for s in stats["side_freq"]]),
    #         ]

    stats = shot_breakdown_stats(def_df)

    show_stats_out_def = [

        html.Div(
            "Shot Range",
            style={
                "textAlign": "center",
                "fontSize": "13px",
                "fontWeight": 600,
                "color": THEME["text_secondary"],
                "marginBottom": "6px",
                "letterSpacing": "0.04em",
                "textTransform": "uppercase"
            }
        ),

        # stat_row([stat_card(*s) for s in stats["fg"]]),
        # html.Div(style={"height": "6px"}),
        # stat_row([stat_card(*s) for s in stats["ast"]]),

        stat_row(
            [
                stat_card(
                    label=fg_label,
                    value=fg_val,
                    subvalue=f"{ast_val} Ast'd" if ast_val != "—" else "—"
                )
                for (fg_label, fg_val), (_, ast_val)
                in zip(stats["fg"], stats["ast"])
            ]
        ),



        freq_bar(
            ["Rim", "S-Mid", "L-Mid", "3P"],
            stats["freq_vals"]
        ),

        html.Div(style={"height": "10px"}),


        # html.Hr(style={
        #     "borderColor": THEME["divider"],
        #     "opacity": 1,
        #     "margin": "12px 0"
        # }),
        # html.Div(
        #     "Court Thirds",
        #     style={
        #         "textAlign": "center",
        #         "fontSize": "13px",
        #         "fontWeight": 600,
        #         "color": THEME["text_secondary"],
        #         "marginBottom": "6px",
        #         "letterSpacing": "0.04em",
        #         "textTransform": "uppercase"
        #     }
        # ),

        # stat_row([stat_card(*s) for s in stats["side_fg"]]),

        # html.Div(style={"height": "6px"}),

        # freq_bar(
        #     ["Left", "Middle", "Right"],
        #     stats["side_freq_vals"]
        # ),
    ]


    # if players:

    #     return (
    #         fig_off,
    #         fig_def,
    #         team_title_with_logo(team, "Shot Charts", team_logo),
    #         chart_header(team, "Offense" + ' - ' + '- '.join(players), team_logo),
    #         chart_header(team, "Defense" + ' - ' + '- '.join(players), team_logo),
    #         show_stats_out_off,
    #         show_stats_out_def
    #     )
    # else:
    #     return (
    #     fig_off,
    #     fig_def,
    #     team_title_with_logo(team, "Shot Charts", team_logo),
    #     chart_header(team, "Offense", team_logo),
    #     chart_header(team, "Defense", team_logo),
    #     show_stats_out_off,
    #     show_stats_out_def
    #     )

    return (
        fig_off,
        fig_def,
        team_title_with_logo(team, "Shot Charts", team_logo),
        chart_header(team, off_title, team_logo),
        chart_header(team, def_title, team_logo),
        show_stats_out_off,
        show_stats_out_def
        )



@app.callback(
    Output("player-dd", "options"),
    Output("half-dd", "options"),
    Output("opp-dd", "options"),
    Output("lineup-dd", "options"),
    Output("on-court-dd", "options"),
    Output("off-court-dd", "options"),
    Input("team-dd", "value"),
    Input("exclude-non-d1", "value"),
)
def update_filter_options(team, exclude_non_d1):

    dff = load_team_data(team)

    size = dff.groupby('shooter', as_index=False).size()
    #print(dff.groupby('shooter').size())
    dff = dff.merge(size, on='shooter',how='left')
    dff = dff.sort_values('size', ascending=False)
    dff = dff.drop('size', axis=1)

    name_team = dff.loc[dff['team_name']==team, 'shooter'].unique()

    dff = load_team_data(team)

    if exclude_non_d1:
        dff = dff[dff["nond1"] == False]
    names_opp = dff.loc[dff['team_name']!=team,  'shooter'].unique()

    player_opts = (
        [{"label": p, "value": p} for p in list(name_team)]
        + [{"label": "------ Opponents ↓ ------", "value": "__sep__", "disabled": True}]
        + [{"label": p, "value": p} for p in list(names_opp)]
    )


    half_opts = [
        {"label": h, "value": h}
        for h in sorted(dff[HALF_COL].dropna().unique())
    ]

    opp_opts = [
        {"label": o, "value": o}
        for o in sorted(dff[OPP_COL].dropna().unique())
    ]

    # ---- lineup options ----
    lineups = dff["lineup"].dropna().unique()

    
    # ---- lineup options ----
    # Count shots per lineup
    lu_counts = (
        dff.loc[dff["team_name"] == team].dropna(subset=["lineup"])
           .assign(lu_size=lambda x: x["lineup"].apply(len))
           .query("lu_size == 5")              # ✅ remove bad lineups
           .groupby("lineup")
           .size()
           .reset_index(name="shots")
    )
    
    # Shot counts per player (team only)
    player_shots = (
        dff[dff["team_name"] == team]
        .groupby("shooter")
        .size()
        .to_dict()
    )
    
    def order_lineup_players(lineup):
        return tuple(
            sorted(
                lineup,
                key=lambda p: player_shots.get(p, 0),
                reverse=True
            )
        )
    
    # Apply ordering
    lu_counts["lineup_ord"] = lu_counts["lineup"].apply(order_lineup_players)
    
    # Sort lineups by shots
    lu_counts = lu_counts.sort_values("shots", ascending=False)
    
    lineup_opts = [
        {
            "label": f"{format_lineup_label(lu)}  ({shots} shots)",
            "value": lineup_key(lu)
        }
        for lu, shots in zip(lu_counts["lineup_ord"], lu_counts["shots"])
    ]


    # team_players = (
    #     dff.loc[dff["team_name"] == team, "shooter"]
    #     .dropna()
    #     .sort_values()
    #     .unique()
    # )
    
   # on_off_opts = [{"label": p, "value": p} for p in team_players]

    on_off_opts = [
        {"label": p, "value": p}
        #for p in (dff[PLAYER_COL].dropna().unique())
        for p in list(name_team)
    ]




    return (
    player_opts,
    half_opts,
    opp_opts,
    lineup_opts,
    on_off_opts,
    on_off_opts,
)



# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
