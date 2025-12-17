from pydantic import BaseModel, Field
from typing import Dict, Any, Optional,List


class BirthDetails(BaseModel):
    year: int = Field(..., ge=1900, le=2100, example=1990)
    month: int = Field(..., ge=1, le=12, example=5)
    day: int = Field(..., ge=1, le=31, example=25)
    hour: int = Field(..., ge=0, le=23, example=14)
    minute: int = Field(..., ge=0, le=59, example=30)
    timezone: float = Field(..., example=5.5, description="Timezone offset from UTC (e.g., 5.5 for India, -5.0 for EST)")
    latitude: float = Field(..., example=28.61)
    longitude: float = Field(..., example=77.20)
    ayanamsa: str = Field("LAHIRI")

class PlanetData(BaseModel):
    id: int
    absolute_longitude: float
    sign_id: int
    degree: float
    is_retrograde: bool
    navamsa_sign_id: Optional[int] = None
    house_number:Optional[int]= None

class ChartResponse(BaseModel):
    meta: Dict[str, Any]
    planets: Dict[str, PlanetData] 
    jaimini_karakas: Dict[str, Any]
    predictions:List[Dict[str,Any]]
    ai_reading: Optional[str] = None
