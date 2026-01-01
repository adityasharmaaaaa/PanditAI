from datetime import datetime, timedelta

class VimshottariDasha:
    def __init__(self):
        # 1. Standard Dasha Durations (Years)
        self.DASHA_YEARS = {
            "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
            "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
        }
        
        # 2. Fixed Zodiac Sequence
        self.DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        
        # 3. Nakshatra Mapping (1 to 27)
        self.NAKSHATRA_RULERS = [
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", # 1-9
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", # 10-18
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"  # 19-27
        ]

    def add_time(self, start_date, years):
        """
        Precise date addition converting astrological years to calendar time.
        1 Astro Year = 365.2425 Days (Gregorian Average)
        """
        total_days = years * 365.2425
        return start_date + timedelta(days=total_days)

    def generate_sub_periods(self, start_date, parent_lord, parent_duration_years, level_depth):
        """
        Recursive function to generate nested Dasha tree.
        level_depth: 1=Antar, 2=Pratyantar, 3=Sookshma
        """
        # STOP CONDITION: We only want up to Sookshma (Level 3)
        # Level 0 = Mahadasha (Handled in main loop)
        # Level 1 = Antar
        # Level 2 = Pratyantar
        # Level 3 = Sookshma
        if level_depth > 3:
            return None

        sub_periods = []
        current_date = start_date
        
        # Sub-periods always start with the Lord of the Parent Period
        start_idx = self.DASHA_ORDER.index(parent_lord)
        
        for i in range(9):
            idx = (start_idx + i) % 9
            planet_name = self.DASHA_ORDER[idx]
            planet_years = self.DASHA_YEARS[planet_name]
            
            # KEY FORMULA: (ParentDuration * PlanetYears) / 120
            # Example: In Sun Mahadasha (6 yrs), Sun Antar = (6 * 6) / 120 = 0.3 years
            duration_in_this_level = (parent_duration_years * planet_years) / 120.0
            
            end_date = self.add_time(current_date, duration_in_this_level)
            
            node = {
                "lord": planet_name,
                "start": current_date,
                "end": end_date,
                "duration": duration_in_this_level,
                "type": ["Mahadasha", "Antardasha", "Pratyantardasha", "Sookshmadasha"][level_depth]
            }
            
            # RECURSIVE CALL: Generate children for this node
            # (e.g., inside this Antardasha, generate Pratyantars)
            children = self.generate_sub_periods(current_date, planet_name, duration_in_this_level, level_depth + 1)
            if children:
                node["sub_periods"] = children
                
            sub_periods.append(node)
            current_date = end_date
            
        return sub_periods

    def calculate_dashas(self, moon_long, birth_date):
        """
        Generates the full life timeline tree.
        """
        # 1. FIND STARTING POINT
        nakshatra_span = 360.0 / 27.0
        nakshatra_idx = int(moon_long / nakshatra_span)
        degree_in_nak = moon_long % nakshatra_span
        
        percent_passed = degree_in_nak / nakshatra_span
        percent_remaining = 1.0 - percent_passed
        
        start_lord = self.NAKSHATRA_RULERS[nakshatra_idx]
        full_years = self.DASHA_YEARS[start_lord]
        balance_years = full_years * percent_remaining
        
        timeline = []
        current_date = birth_date
        
        # 2. FIRST MAHADASHA (The Balance Period)
        # Note: Calculating accurate sub-periods for the balance period is mathematically complex 
        # because we are starting in the *middle* of a cycle. 
        # For V1.0 Simplicity: We calculate the end date, but we don't generate the 
        # retrospective sub-periods for the past. We generate sub-periods moving forward if possible.
        
        end_date = self.add_time(current_date, balance_years)
        
        # We skip recursion for the balance dasha in V1 to avoid "negative time" logic complexity
        # or we treat it as a partial block. Let's add it as a flat block for safety.
        timeline.append({
            "lord": start_lord,
            "start": current_date,
            "end": end_date,
            "duration": balance_years,
            "type": "Mahadasha (Balance)",
            "sub_periods": [] # Empty for balance to prevent errors
        })
        current_date = end_date
        
        # 3. GENERATE FULL CYCLES FOR REMAINING PLANETS
        start_idx = self.DASHA_ORDER.index(start_lord)
        
        # Generate next 9 Mahadashas (covering 120 years of life)
        for i in range(1, 10):
            idx = (start_idx + i) % 9
            lord = self.DASHA_ORDER[idx]
            duration = self.DASHA_YEARS[lord]
            
            md_end = self.add_time(current_date, duration)
            
            md_node = {
                "lord": lord,
                "start": current_date,
                "end": md_end,
                "duration": duration,
                "type": "Mahadasha"
            }
            
            # GENERATE TREE (Antar -> Pratyantar -> Sookshma)
            # Level 1 call (Antardasha)
            md_node["sub_periods"] = self.generate_sub_periods(current_date, lord, duration, 1)
            
            timeline.append(md_node)
            current_date = md_end
            
        return timeline

    def get_current_dasha_details(self, timeline, target_date=None):
        """
        Navigates the tree to find exactly where we are NOW.
        """
        if target_date is None: target_date = datetime.now()
        
        result = {}
        
        # 1. Find Maha
        curr_md = None
        for md in timeline:
            if md['start'] <= target_date < md['end']:
                curr_md = md
                break
        
        if not curr_md: return None
        result['mahadasha'] = curr_md
        
        # 2. Find Antar
        if 'sub_periods' in curr_md and curr_md['sub_periods']:
            for ad in curr_md['sub_periods']:
                if ad['start'] <= target_date < ad['end']:
                    result['antardasha'] = ad
                    
                    # 3. Find Pratyantar
                    if 'sub_periods' in ad and ad['sub_periods']:
                        for pd in ad['sub_periods']:
                            if pd['start'] <= target_date < pd['end']:
                                result['pratyantardasha'] = pd
                                
                                # 4. Find Sookshma
                                if 'sub_periods' in pd and pd['sub_periods']:
                                    for sd in pd['sub_periods']:
                                        if sd['start'] <= target_date < sd['end']:
                                            result['sookshmadasha'] = sd
                                            break
                                break
                    break
                    
        return result