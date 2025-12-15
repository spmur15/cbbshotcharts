import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
from plotly.colors import sample_colorscale
import warnings
warnings.filterwarnings("ignore")

logo_path = r'currentSzn.csv'
LOGO_DF = pd.read_csv(logo_path)[['Team', 'Logo']]

#color = sample_colorscale("RdYlGn", pct)[0]
#

COURT_LINE_COLOR = "#333"
COURT_LINE_WIDTH = 1.5

COURT_SHADOW_COLOR = "rgba(0,0,0,0.18)"
COURT_SHADOW_OFFSET = 0.6

R_MAX = 25   # must match y-axis max in layout


# ---- Zone geometry (feet, hoop-centered) ----
R_RIM = 4
R_PAINT = 8
R_3 = 22

R_RIM = 4.25
R_PAINT_EDGE = R_PAINT + 1
R_PAINT = R_PAINT + 2.75
R_3_EDGE = R_3 + 0.735
R_3 = R_3# + 0.7
R_MAX = 31

ZONE_DRAW_ORDER = [
    "Paint (Non-Rim)",
    "Left Baseline 2", "Right Baseline 2",
    "Top Mid", "Left Mid", "Right Mid",
    "Top 3", "Left Wing 3", "Right Wing 3", "Corner 3",
    "Rim"
]


ZONE_FAMILY = {
    # Rim / Paint
    "Rim": "paint",
    "Paint (Non-Rim)": "paint",

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
    "Paint (Non-Rim)": dict(
        type="path",
        path=polar_wedge(R_RIM, R_PAINT, -180, 180),
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

    "Top Mid": (18,0),
    "Left Mid": (10, 12),
    "Right Mid": (10, -12),
    "Left Mid Low": (-22, -8),
    "Right Mid Low": (-12, 10),

    "Top 3": (0, 30),
    "Left Wing 3": (16, 26),
    "Right Wing 3": (-16, 26),
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
# DATA_PATH = "Shot Location Data//Wisconsin_shot_data_2026.csv"
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
    #     line=dict(color=COURT_LINE_COLOR, width=COURT_LINE_WIDTH),
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

    # Free throw circle (radius 6 ft, centered at FT line)
    shapes.append(dict(
        type="circle",
        x0=-21.0, y0=-6.0, x1=-9.0, y1=6.0,
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
        plot_bgcolor="#FFFFFF",
        margin=dict(l=4, r=4, t=8, b=4),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=14),
            itemsizing="constant",
            #valign='center'
        )

    )

    return layout


COURT_L_FT = 94.0
COURT_W_FT = 50.0
HALF_DIVIDER = 50.0        # in NCAA x-scale units (0..100)
HOOP_FROM_BASELINE_FT = 5.25
HOOP_X_FT = COURT_L_FT - HOOP_FROM_BASELINE_FT   # 88.75 ft from left baseline


def standardize_to_right_basket(dff, x_col="x", y_col="y"):
    """
    NCAA coords are on a 0..100-ish full court for BOTH axes.
    Shots on the left half (x < 50) are flipped so that all shots end up
    on the right half (attacking the same basket).

    We flip both x and y to preserve left/right orientation.
    """
    out = dff.copy()
    x = out[x_col].astype(float).to_numpy()
    y = out[y_col].astype(float).to_numpy()

    left_half = x < HALF_DIVIDER

    # Flip across full-court axes in the 0..100 coordinate system
    x[left_half] = 100.0 - x[left_half]
    y[left_half] = 100.0 - y[left_half]

    out["x_std"] = x
    out["y_std"] = y
    return out


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

    dff["offense_defense"] = np.where(
        dff["team_name"] == team, "Offense", "Defense"
    )
    dff["made"] = np.where(dff["result"] == "made", 1, 0)

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
        return (0, 0)

    if zone == "Paint (Non-Rim)":
        return (0, 6.5)

    if zone == "Top Mid":
        return (0, 17.5)
    if zone == "Left Mid":
        return (12, 12)
    if zone == "Right Mid":
        return (-12, 12)

    if zone == "Top 3":
        return (0, 26.5)
    if zone == "Left Wing 3":
        return (19, 19)
    if zone == "Right Wing 3":
        return (-19, 19)
    if zone == "Right Corner 3":
        return (27, 2)
    if zone == "Left Corner 3":
        return (-27, 2)

    # ✅ NEW BASELINE ZONES
    if zone == "Left Mid Low":
        return (-16, 0)
    if zone == "Right Mid Low":
        return (16, 0)

    # Fallback (never crashes)
    return rotate_for_display(0, 0)


def shooting_summary(dff):
    """
    Returns:
    - FG line: "284/642 – 44.2%"
    - PPS/eFG line: "1.033 pts/shot – 51.6% eFG"
    """

    if dff.empty:
        return ("No shots",'')

    fga = len(dff)
    fgm = int(dff["made"].sum())
    fg_pct = fgm / fga if fga else 0

    # identify 3s using your existing zone logic (works in zone mode)
    threes = dff.get("zone", pd.Series(False, index=dff.index)).isin(
        ["Top 3", "Left Wing 3", "Right Wing 3", "Left Corner 3", "Right Corner 3"]
    )

    three_made = int(dff.loc[threes, "made"].sum())
    two_made = fgm - three_made

    points = two_made * 2 + three_made * 3
    pps = points / fga if fga else 0
    efg = (fgm + 0.5 * three_made) / fga if fga else 0

    fg_line = f"{fgm}/{fga} · {fg_pct:.1%}"
    pps_line = f"{pps:.3f} pts/shot · {efg:.1%} eFG"

    return fg_line, pps_line


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
                    "height": "36px",
                    "width": "36px",
                    "objectFit": "contain"
                }
            ),
            html.Div(
                [
                    html.Div(
                        team,
                        style={
                            "fontSize": "24px",
                            "fontWeight": 700
                        }
                    ),
                    subtitle and html.Div(
                        subtitle,
                        style={
                            "fontSize": "14px",
                            "color": "#666"
                        }
                    )
                ]
            )
        ]
    )


def chart_title(team, side, logo):
    return (
        f"<span style='display:flex;align-items:center;gap:8px;'>"
        f"<img src='{logo}' style='height:22px;'>"
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
            "fontSize": "18px"
        },
        children=[
            html.Img(src=logo, style={"height": "22px"}),
            html.Span(f"{side}")
        ]
    )



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
        x=mx,
        y=my,
        mode="markers",
        marker=dict(size=7, color="rgba(220,50,50,0.55)"),
        name="Miss",
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scattergl(
        x=gx,
        y=gy,
        mode="markers",
        marker=dict(size=7, color="rgba(40,160,60,0.65)"),
        name="Make",
        hoverinfo="skip"
    ))


    fig.update_layout(
        #title=dict(text=title, x=0.5, y=0.98),
        plot_bgcolor='#fafafa',
        paper_bgcolor="#fafafa"
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
    #     plot_bgcolor="#fafafa",
    #     paper_bgcolor="#fafafa"
    # )

    # ---- add summary stats on shots view too ----
    dff2 = dff.copy()
    dff2.loc[:, "dist"]  = np.sqrt(dff2["x_plot"]**2 + dff2["y_plot"]**2)
    dff2.loc[:, "angle"] = np.degrees(np.arctan2(dff2["y_plot"], -dff2["x_plot"]))
    dff2.loc[:, "zone"]  = dff2.apply(assign_zone, axis=1)

    fg_line, pps_line = shooting_summary(dff2)
    add_chart_subtitle(fig, fg_line, pps_line)

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
    # ))s


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

    zs = (
        dff.groupby("zone")
        .agg(att=("made", "count"), made=("made", "sum"))
        .reset_index()
    )
    zs["pct"] = zs["made"] / zs["att"]

    for _, r in zs.iterrows():
        zone_shape = ZONE_SHAPES[r["zone"]].copy()
        #print(zone_shape)
        zone_shape['line'] = {'width':3,'color':'#fafafa'}

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
        fig.add_trace(go.Scatter(
            x=[x_txt],
            y=[y_txt],
            text=[f"{r.made}/{r.att}<br>{r.pct:.0%}"],
            mode="text",
            textfont=dict(size=14, family="Funnel Display"),
            showlegend=False,
            #fillcolor='#777'
        ))

    fig.update_layout(
        #title=dict(text=title, x=0.5),
        plot_bgcolor="#fafafa",
        paper_bgcolor="#fafafa"
    )

    fig.update_layout(showlegend=False)

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
    #     plot_bgcolor="#fafafa",
    #     paper_bgcolor="#fafafa"
    # )

    #add_zone_dividers(fig)
    # 🔹 ADD SUMMARY STATS
    fg_line, pts_line = shooting_summary(dff)
    add_chart_subtitle(fig, fg_line, pts_line)


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
    if d <= R_PAINT_EDGE:
        return "Paint (Non-Rim)"

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




def zone_color(pct, zone):
    """
    Returns a color based on zone-specific shooting percentage ranges.
    Darker = better for that shot type.
    """

    family = ZONE_FAMILY.get(zone)

    # fallback (should never hit, but safe)
    if family not in ZONE_PCT_RANGES:
        return sample_colorscale("BuGn", 0.4)[0]

    lo, hi = ZONE_PCT_RANGES[family]

    # normalize within family range
    t = (pct - lo) / (hi - lo)

    # allow outside range but clip for color stability
    t = np.clip(t, 0.0, 1.0)

    return sample_colorscale("BuGn", t)[0]



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
            line=dict(color="#666", width=3),
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

def add_chart_subtitle(fig, fg_line, pps_line):
    # closer to title (title is at y=0.98)
    y1 = 0.99
    y2 = 0.95

    common_font = dict(
        family="Funnel Display",
        color="#6b6b6b"   # grey for BOTH
    )

    fig.add_annotation(
        x=0.5, y=y1,
        xref="paper", yref="paper",
        text=fg_line,           # no bold
        showarrow=False,
        font=dict(**common_font, size=14),
        align="right"
    )

    fig.add_annotation(
        x=0.5, y=y2,
        xref="paper", yref="paper",
        text=pps_line,
        showarrow=False,
        font=dict(**common_font, size=14),
        align="right"
    )



# --------------------------------------------------
# DASH APP
# --------------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for Render

# --------------------------------------------------
# DROPDOWN OPTIONS
# --------------------------------------------------
# player_options = [{"label": p, "value": p} for p in sorted(df[PLAYER_COL].dropna().unique())]
# half_options = [{"label": h, "value": h} for h in sorted(df[HALF_COL].dropna().unique())]
# opp_options = [{"label": o, "value": o} for o in sorted(df[OPP_COL].dropna().unique())]
team_options = [
    {"label": t, "value": t}
    for t in ["Illinois", "Iowa", "Wisconsin", "Kansas", "Marquette", "Michigan"]
]


# --------------------------------------------------
# LAYOUT (MOBILE-FIRST)
# --------------------------------------------------
app.layout = dbc.Container(
    fluid=True,
    style={
        "backgroundColor": "#f2f3f5",
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
                html.H3(
                    "CBB Shot Charts",
                    className="my-3 text-center",
                    style={"margin": "0",'padding':'0'}
                ),
                style={
                        #"maxWidth": "360px",
                        "margin": "0",
                        #"boxShadow": "0 6px 18px rgba(0,0,0,0.22)",
                        #"borderRadius": "10px",
                        #"fontWeight": "600",
                                            }
            )
        ),
        html.Hr(style={"margin": "0",'padding':'0'}),



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
                        "boxShadow": "0 6px 18px rgba(0,0,0,0.22)",
                        "borderRadius": "10px",
                        "fontWeight": "600",
                                            }
                ),
                width=12
            ),
            className="mb-4"
        ),

        html.Br(),

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
                                                placeholder="Player(s)"
                                            ),
                                            xs=12, md=4
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="half-dd",
                                                multi=True,
                                                placeholder="Half"
                                            ),
                                            xs=6, md=2
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="quad-dd",
                                                options=['Q1A', 'Q1B', 'Q2', 'Q3', 'Q4'],
                                                multi=True,
                                                placeholder="Quad"
                                            ),
                                            xs=6, md=2
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="opp-dd",
                                                multi=True,
                                                placeholder="Opponent"
                                            ),
                                            xs=12, md=4
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
                                "boxShadow": "0 6px 18px rgba(0,0,0,0.22)",
                                "borderRadius": "14px",
                                "backgroundColor": "#f7f8fa",}
                    ),
                    className="filters-wrap mb-3",
                    style={
                        #"maxWidth": "800px",   # mobile default
                        "margin": "0 auto",
                        "boxShadow": "0 6px 18px rgba(0,0,0,0.22)",
                        "borderRadius": "14px",
                        "backgroundColor": "#f7f8fa",
                        #"overflow": "auto",   # 🔴 REQUIRED for rounding to clip children
                    }
                ),
                xs=9, md=9
            ), justify='center'
        ),




        dbc.RadioItems(
            id="view-mode",
            options=[
                {"label": "Shots", "value": "shots"},
                {"label": "Zones", "value": "zones"},
            ],
            value="shots",
            inline=True,
            #button=True,
            className="d-flex justify-content-center mb-2",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-dark px-4 py-2",
            labelCheckedClassName="btn btn-dark shadow"
        ),

        html.Hr(),


        dbc.Row(
                [
                    dbc.Col([
                        html.Div(id="offense-title", className="text-center mb-2"),
                        html.Div(
                            dcc.Graph(
                                id="offense-chart",
                                config={"displayModeBar": False,
                                        "scrollZoom": False},
                                style={
                                    "height": "45vh",
                                    "minHeight": "320px"
                                }
                            ),
                            style={
                                "background": "#fafafa",
                                "borderRadius": "14px",
                                "boxShadow": "0 10px 28px rgba(0,0,0,0.18)",
                                "padding": "6px"
                            }
                        )],
                        xs=12, md=6,
                    ),

                    dbc.Col([
                        html.Div(id="defense-title", className="text-center mb-2"),
                        html.Div(
                            dcc.Graph(
                                id="defense-chart",
                                config={"displayModeBar": False},
                                style={
                                    "height": "45vh",
                                    "minHeight": "320px"
                                }

                            ),
                            style={
                                "background": "#fafafa",
                                "borderRadius": "14px",
                                "boxShadow": "0 10px 28px rgba(0,0,0,0.18)",
                                "padding": "6px"
                            }
                        )],
                        xs=12, md=6,
                    ),
                ],
                className="gy-4"   # 👈 adds vertical spacing on mobile
            )



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

    Input("team-dd", "value"),
    Input("view-mode", "value"),
    Input("player-dd", "value"),
    Input("half-dd", "value"),
    Input("opp-dd", "value"),
)

def update_charts(team, view_mode, players, halves, opps):

    # Load correct team file
    dff = load_team_data(team)


    team_logo = LOGO_DF.loc[LOGO_DF["Team"] == team, "Logo"].iloc[0]

    if pd.isna(team_logo) or team_logo == "":
        team_logo = "/assets/logos/west-virginia-mountaineers.png"
    else:
        team_logo = f"/assets/{team_logo}"





    if players:
        dff = dff[dff[PLAYER_COL].isin(players)]

    if halves:
        dff = dff[dff[HALF_COL].isin(halves)]

    if opps:
        dff = dff[dff[OPP_COL].isin(opps)]

    dff = standardize_to_right_basket(dff, x_col="x", y_col="y")
    dff = to_feet_hoop_centered(dff)

    off_df = dff[dff[OFF_DEF_COL] == "Offense"]
    def_df = dff[dff[OFF_DEF_COL] == "Defense"]

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

        



    return (
        fig_off,
        fig_def,
        team_title_with_logo(team, "Shot Charts", team_logo),
        chart_header(team, "Offense", team_logo),
        chart_header(team, "Defense", team_logo),
    )


@app.callback(
    Output("player-dd", "options"),
    Output("half-dd", "options"),
    Output("opp-dd", "options"),
    Input("team-dd", "value")
)
def update_filter_options(team):

    dff = load_team_data(team)

    size = dff.groupby('shooter', as_index=False).size()
    #print(dff.groupby('shooter').size())
    dff = dff.merge(size, on='shooter',how='left')
    dff = dff.sort_values('size', ascending=False)
    dff = dff.drop('size', axis=1)

    name_team = dff.loc[dff['team_name']==team, 'shooter'].unique()
    names_opp = dff.loc[dff['team_name']!=team,  'shooter'].unique()

    player_opts = [
        {"label": p, "value": p}
        #for p in (dff[PLAYER_COL].dropna().unique())
        for p in list(name_team) + [' ------ Opponents↓ ----- '] + list(names_opp)
    ]

    half_opts = [
        {"label": h, "value": h}
        for h in sorted(dff[HALF_COL].dropna().unique())
    ]

    opp_opts = [
        {"label": o, "value": o}
        for o in sorted(dff[OPP_COL].dropna().unique())
    ]

    return player_opts, half_opts, opp_opts


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
