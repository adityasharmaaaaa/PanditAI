import matplotlib.pyplot as plt
import io

def draw_north_indian_chart(planet_data, asc_sign_id, title="D1 Rashi Chart"):
    """
    Draws a styled North Indian Vedic Chart matching the user's beige/cream theme.
    """
    # --- STYLE CONFIGURATION ---
    # Colors derived from the screenshot
    BG_COLOR = '#FAF9E6'      # Cream/Beige background
    LINE_COLOR = '#666666'    # Dark Grey lines
    SIGN_COLOR = '#666666'    # Grey for Sign Numbers
    
    # Standard Vedic Planet Colors
    PLANET_COLORS = {
        'Su': '#D95F02',      # Orange/Brown (Sun)
        'Mo': '#1F1F7A',      # Dark Blue (Moon)
        'Ma': '#D62728',      # Red (Mars)
        'Me': '#1B9E77',      # Green (Mercury)
        'Ju': '#B8860B',      # Gold/Mustard (Jupiter)
        'Ve': '#E7298A',      # Pink/Magenta (Venus)
        'Sa': '#000000',      # Black (Saturn)
        'Ra': '#444444',      # Dark Grey (Rahu)
        'Ke': '#555555',      # Brownish Grey (Ketu)
        'As': '#800080',      # Purple (Ascendant)
        'Ur': '#17BECF',      # Cyan/Blue (Uranus)
        'Ne': '#17BECF',      # Cyan/Blue (Neptune)
        'Pl': '#8C564B'       # Brown (Pluto)
    }

    # 1. SETUP PLOT
    fig, ax = plt.subplots(figsize=(6, 6), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title (Optional, can be removed if strictly following screenshot)
    # ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='black')

    # 2. DRAW FRAME (The Diamond Layout)
    # Use a slightly thinner line for that crisp look
    lw = 1.2
    
    # Outer Square
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=LINE_COLOR, linewidth=lw)
    # Diagonals (The Cross)
    ax.plot([0, 1], [0, 1], color=LINE_COLOR, linewidth=lw)
    ax.plot([0, 1], [1, 0], color=LINE_COLOR, linewidth=lw)
    # Inner Diamond
    ax.plot([0.5, 1, 0.5, 0, 0.5], [1, 0.5, 0, 0.5, 1], color=LINE_COLOR, linewidth=lw)

    # 3. COORDINATE SYSTEMS
    
    # A. SIGN NUMBERS (The "Tucked" positions)
    # Based on the screenshot, sign numbers are clustered near the intersections.
    sign_coords = {
        # H1 (Top Diamond): Bottom tip
        1: (0.5, 0.53),
        # H2 (Top-Left Triangle): Bottom-Right corner (near center)
        2: (0.28, 0.73),
        # H3 (Left-Top Triangle): Top-Right corner (near H4)
        3: (0.23, 0.77), # Swapped slightly to match visual "clustering" around diagonal
        # Actually, in the screenshot: 
        # H2 is the top triangle of the left quadrant -> Number is near bottom right of that triangle.
        # H3 is the bottom triangle of the left quadrant -> Number is near top right of that triangle.
        # Let's refine based on the diagonal line y = -x + 1
        
        # Revised Coordinates to match screenshot perfectly:
        1: (0.5, 0.55),     # Center Top
        2: (0.28, 0.78),    # Top Left quadrant, lower right side
        3: (0.22, 0.72),    # Top Left quadrant, upper right side
        4: (0.45, 0.5),     # Center Left
        5: (0.22, 0.28),    # Bottom Left quadrant, lower right side
        6: (0.28, 0.22),    # Bottom Left quadrant, upper right side
        7: (0.5, 0.45),     # Center Bottom
        8: (0.72, 0.22),    # Bottom Right quadrant, upper left side
        9: (0.78, 0.28),    # Bottom Right quadrant, lower left side
        10: (0.55, 0.5),    # Center Right
        11: (0.78, 0.72),   # Top Right quadrant, lower left side
        12: (0.72, 0.78)    # Top Right quadrant, upper left side
    }
    
    # B. PLANET POSITIONS (Centered in the "belly" of the house)
    planet_coords = {
        1: (0.5, 0.8),    # Top
        2: (0.25, 0.9),   # Top Left (High)
        3: (0.1, 0.75),   # Top Left (Low) - shifted left
        4: (0.2, 0.5),    # Left
        5: (0.1, 0.25),   # Bottom Left (High)
        6: (0.25, 0.1),   # Bottom Left (Low)
        7: (0.5, 0.2),    # Bottom
        8: (0.75, 0.1),   # Bottom Right (Low)
        9: (0.9, 0.25),   # Bottom Right (High)
        10: (0.8, 0.5),   # Right
        11: (0.9, 0.75),  # Top Right (Low)
        12: (0.75, 0.9)   # Top Right (High)
    }

    # 4. PREPARE DATA
    house_planets = {i: [] for i in range(1, 13)}
    
    # Add Ascendant specially
    asc_sign = asc_sign_id
    
    # Process Planets
    for p_name, data in planet_data.items():
        if p_name == "Ascendant": 
            # We treat Ascendant as a planet label in House 1 for plotting
            house_planets[1].append(("Asc", PLANET_COLORS['As']))
            continue
            
        p_sign = data["sign_id"]
        # Calculate House Number (1-based)
        house_num = (p_sign - asc_sign) + 1
        if house_num <= 0: house_num += 12
        
        # Format label: Short name + R if retrograde
        raw_label = p_name[:2]
        if p_name == "Mars": raw_label = "Ma" # Fix naming collision if any
        
        # Check Retrograde
        is_retro = data.get("is_retrograde", False)
        label_str = f"{raw_label}®" if is_retro else raw_label
        
        # Get Color
        color = PLANET_COLORS.get(raw_label, 'black')
        
        house_planets[house_num].append((label_str, color))

    # 5. RENDER TEXT
    for h_num in range(1, 13):
        # A. Sign Number (Grey)
        sx, sy = sign_coords[h_num]
        rashi_num = (asc_sign_id + h_num - 1) % 12
        if rashi_num == 0: rashi_num = 12
        
        ax.text(sx, sy, str(rashi_num), fontsize=10, color=SIGN_COLOR, 
                ha='center', va='center', alpha=0.9)
        
        # B. Planets (Colored)
        px, py = planet_coords[h_num]
        p_list = house_planets[h_num]
        
        if not p_list: continue

        # Dynamic positioning for multiple planets
        # We draw them line by line or side by side depending on count
        
        # If crowded, reduce font
        font_size = 11
        if len(p_list) > 3: font_size = 9
        
        # Simple vertical stack logic with colors
        # Calculate total height to center the block
        line_height = 0.06
        total_h = (len(p_list) - 1) * line_height
        start_y = py + (total_h / 2)
        
        for i, (txt, col) in enumerate(p_list):
            current_y = start_y - (i * line_height)
            
            # Special logic for House 2, 3, 5, 6, 8, 9, 11, 12 to ensure they don't hit edge
            # (Simplistic rendering: just print them)
            ax.text(px, current_y, txt, fontsize=font_size, color=col, 
                    ha='center', va='center', fontweight='medium')

    # 6. SAVE
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=False, dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf