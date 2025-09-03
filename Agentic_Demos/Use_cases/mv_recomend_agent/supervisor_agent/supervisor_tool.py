from recomendations_agent.agent import root_agent as recommendation_agent
from plot_details_agent.agent import root_agent as plot_details_agent

def supervisor_router(user_input: str):
    """
    Supervisor router to decide which movie agent to invoke.
    """
    user_input_clean = user_input.strip().lower()

    recommend_keywords = ["recommend", "suggest", "top movies", "best movies", "movie list"]
    details_keywords = ["plot", "details", "info", "information", "story", "summary"]

    if any(keyword in user_input_clean for keyword in recommend_keywords):
            # Call recommendation agent
        return recommendation_agent(user_input)

    elif any(keyword in user_input_clean for keyword in details_keywords):
            # Call details agent
        return plot_details_agent(user_input)

    else:
         return "Please ask for movie recommendations or details."
