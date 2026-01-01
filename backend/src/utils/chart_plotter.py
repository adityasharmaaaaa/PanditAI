from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io


def draw_north_indian_chart(planet_data, asc_sign_id, title="D1 Rashi Chart"):
    """
    Draws a styled North Indian Vedic Chart matching the user's beige/cream theme.
    Refactored to use Object-Oriented Matplotlib interface for thread safety.
    """
    # --- STYLE CONFIGURATION ---
    BG_COLOR = "#FAF9E6"  # Cream/Beige background
    LINE_COLOR = "#666666"  # Dark Grey lines
    SIGN_COLOR = "#666666"  # Grey for Sign Numbers

    # Standard Vedic Planet Colors
    PLANET_COLORS = {
        "Su": "#D95F02",  # Orange/Brown (Sun)
        "Mo": "#1F1F7A",  # Dark Blue (Moon)
        "Ma": "#D62728",  # Red (Mars)
        "Me": "#1B9E77",  # Green (Mercury)
        "Ju": "#B8860B",  # Gold/Mustard (Jupiter)
        "Ve": "#E7298A",  # Pink/Magenta (Venus)
        "Sa": "#000000",  # Black (Saturn)
        "Ra": "#444444",  # Dark Grey (Rahu)
        "Ke": "#555555",  # Brownish Grey (Ketu)
        "As": "#800080",  # Purple (Ascendant)
        "Ur": "#17BECF",  # Cyan/Blue (Uranus)
        "Ne": "#17BECF",  # Cyan/Blue (Neptune)
        "Pl": "#8C564B",  # Brown (Pluto)
    }

    # 1. SETUP PLOT (Using Figure directly, bypassing pyplot global state)
    fig = Figure(figsize=(6, 6), facecolor=BG_COLOR)
    ax = fig.add_subplot(111)

    ax.set_facecolor(BG_COLOR)
    ax.set_aspect("equal")
    ax.axis("off")

    # 2. DRAW FRAME (The Diamond Layout)
    lw = 1.2

    # Outer Square
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=LINE_COLOR, linewidth=lw)
    # Diagonals (The Cross)
    ax.plot([0, 1], [0, 1], color=LINE_COLOR, linewidth=lw)
    ax.plot([0, 1], [1, 0], color=LINE_COLOR, linewidth=lw)
    # Inner Diamond
    ax.plot([0.5, 1, 0.5, 0, 0.5], [1, 0.5, 0, 0.5, 1], color=LINE_COLOR, linewidth=lw)

    # 3. COORDINATE SYSTEMS
    sign_coords = {
        1: (0.5, 0.55),
        2: (0.28, 0.78),
        3: (0.22, 0.72),
        4: (0.45, 0.5),
        5: (0.22, 0.28),
        6: (0.28, 0.22),
        7: (0.5, 0.45),
        8: (0.72, 0.22),
        9: (0.78, 0.28),
        10: (0.55, 0.5),
        11: (0.78, 0.72),
        12: (0.72, 0.78),
    }

    planet_coords = {
        1: (0.5, 0.8),
        2: (0.25, 0.9),
        3: (0.1, 0.75),
        4: (0.2, 0.5),
        5: (0.1, 0.25),
        6: (0.25, 0.1),
        7: (0.5, 0.2),
        8: (0.75, 0.1),
        9: (0.9, 0.25),
        10: (0.8, 0.5),
        11: (0.9, 0.75),
        12: (0.75, 0.9),
    }

    # 4. PREPARE DATA
    house_planets = {i: [] for i in range(1, 13)}
    asc_sign = asc_sign_id

    for p_name, data in planet_data.items():
        if p_name == "Ascendant":
            house_planets[1].append(("Asc", PLANET_COLORS["As"]))
            continue

        p_sign = data["sign_id"]
        house_num = (p_sign - asc_sign) + 1
        if house_num <= 0:
            house_num += 12

        raw_label = p_name[:2]
        if p_name == "Mars":
            raw_label = "Ma"

        is_retro = data.get("is_retrograde", False)
        label_str = f"{raw_label}®" if is_retro else raw_label
        color = PLANET_COLORS.get(raw_label, "black")

        house_planets[house_num].append((label_str, color))

    # 5. RENDER TEXT
    for h_num in range(1, 13):
        # A. Sign Number
        sx, sy = sign_coords[h_num]
        rashi_num = (asc_sign_id + h_num - 1) % 12
        if rashi_num == 0:
            rashi_num = 12

        ax.text(
            sx,
            sy,
            str(rashi_num),
            fontsize=10,
            color=SIGN_COLOR,
            ha="center",
            va="center",
            alpha=0.9,
        )

        # B. Planets
        px, py = planet_coords[h_num]
        p_list = house_planets[h_num]

        if not p_list:
            continue

        font_size = 11
        if len(p_list) > 3:
            font_size = 9

        line_height = 0.06
        total_h = (len(p_list) - 1) * line_height
        start_y = py + (total_h / 2)

        for i, (txt, col) in enumerate(p_list):
            current_y = start_y - (i * line_height)
            ax.text(
                px,
                current_y,
                txt,
                fontsize=font_size,
                color=col,
                ha="center",
                va="center",
                fontweight="medium",
            )

    # 6. SAVE (Using FigureCanvas)
    # This avoids using the global pyplot state machine
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    # plt.close(fig) # Not needed in pure OO mode as fig is garbage collected

    buf.seek(0)
    return buf
