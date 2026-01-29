from typing import Tuple


class RecommendationService:
    """Service for generating water treatment recommendations."""
    
    @staticmethod
    def get_recommendation(avg_ph: float, avg_tds: float) -> Tuple[str, str]:
        """
        Generate treatment recommendation based on pH and TDS values.
        
        Args:
            avg_ph: Average pH value
            avg_tds: Average TDS value in mg/L or ppm
            
        Returns:
            Tuple of (treatment_train, explanation)
        """
        # Determine pH range
        ph_low = avg_ph <= 7.5
        ph_target = 7.5 < avg_ph < 8.3
        ph_high = avg_ph >= 8.3
        
        # Determine TDS range
        tds_low = avg_tds < 100
        tds_moderate = 100 <= avg_tds < 300
        tds_high = avg_tds >= 300
        
        # Apply rules
        
        # Rule A - Clean Water (No Treatment Required)
        if ph_target and tds_low:
            return (
                "No treatment required",
                "Water is within the target pH range and has low TDS, so it is considered clean and unlikely to cause corrosion."
            )
        
        # Rule B - High pH, Low TDS
        if ph_high and tds_low:
            return (
                "pH adjustment with sulfuric acid (H₂SO₄)",
                "pH is above the target range; acid dosing is recommended to bring pH into the safe operating range."
            )
        
        # Rule C - Low pH, Low TDS
        if ph_low and tds_low:
            return (
                "pH adjustment with sodium hydroxide (NaOH)",
                "pH is below the target range; caustic dosing is recommended to bring pH into the safe operating range."
            )
        
        # Rule D - Moderate TDS, Target pH
        if ph_target and tds_moderate:
            return (
                "Reverse osmosis (RO)",
                "TDS is elevated; RO is recommended to reduce dissolved solids while pH is already in range."
            )
        
        # Rule E - High TDS, Target pH
        if ph_target and tds_high:
            return (
                "Ion exchange",
                "TDS is high; ion exchange is recommended to remove dissolved ions effectively while pH is in range."
            )
        
        # Rule F - Moderate TDS, High pH
        if ph_high and tds_moderate:
            return (
                "pH adjustment with H₂SO₄ → Reverse osmosis (RO)",
                "pH is above target range and TDS is elevated. First adjust pH with acid dosing, then use RO to reduce dissolved solids."
            )
        
        # Rule G - Moderate TDS, Low pH
        if ph_low and tds_moderate:
            return (
                "pH adjustment with NaOH → Reverse osmosis (RO)",
                "pH is below target range and TDS is elevated. First adjust pH with caustic dosing, then use RO to reduce dissolved solids."
            )
        
        # Rule H - High TDS, High pH
        if ph_high and tds_high:
            return (
                "pH adjustment with H₂SO₄ → Ion exchange",
                "pH is above target range and TDS is high. First adjust pH with acid dosing, then use ion exchange to remove dissolved ions."
            )
        
        # Rule I - High TDS, Low pH
        if ph_low and tds_high:
            return (
                "pH adjustment with NaOH → Ion exchange",
                "pH is below target range and TDS is high. First adjust pH with caustic dosing, then use ion exchange to remove dissolved ions."
            )
        
        # Fallback (should not reach here with proper logic)
        return (
            "Contact water treatment specialist",
            "Water parameters are outside typical ranges. Professional consultation recommended."
        )
