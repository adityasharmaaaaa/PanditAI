import swisseph as swe

class AyanamsaSystem:
    # Mapping string names to Swiss Ephemeris constants
    MODES = {
        "LAHIRI": swe.SIDM_LAHIRI,       # Standard for BPHS (Chitra Paksha)
        "RAMAN": swe.SIDM_RAMAN,         # Used by some Jaimini scholars
        "KRISHNAMURTI": swe.SIDM_KRISHNAMURTI, # Used in KP Astrology
        "YUKTESHWAR": swe.SIDM_YUKTESHWAR
    }

    @staticmethod
    def set_mode(mode_name="LAHIRI"):
        """
        Sets the global Sidereal mode for swisseph.
        """
        mode = AyanamsaSystem.MODES.get(mode_name.upper(), swe.SIDM_LAHIRI)
        
        # set_sid_mode(mode, t0, ayan_t0) - t0/ayan_t0 are usually 0 for standard predefined modes
        swe.set_sid_mode(mode, 0, 0)
        return mode_name