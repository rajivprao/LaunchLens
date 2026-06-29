from typing import TypedDict,List,Dict,Any

class LaunchLensState(TypedDict):

    user_query:str 

    idea_context:str
    
    demand_research:Dict[str,Any]
    supply_research:Dict[str,Any]
    opportunity_analysis:Dict[str,Any]
    verdict:Dict[str,Any]
    
    final_report:str

