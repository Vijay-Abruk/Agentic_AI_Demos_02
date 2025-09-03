#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from demo_project_1.crew import MovieResearchProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    inputs = {
        'topic': 'Popular Movies',
        'current_year': str(datetime.now().year)
    }
    try:
        MovieResearchProject().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Error running the crew: {e}")

def train():
    inputs = {
        "topic": "Popular Movies",
        'current_year': str(datetime.now().year)
    }
    try:
        MovieResearchProject().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Error training the crew: {e}")

def replay():
    try:
        MovieResearchProject().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Error replaying the crew: {e}")

def test():
    inputs = {
        "topic": "Popular Movies",
        "current_year": str(datetime.now().year)
    }
    try:
        MovieResearchProject().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Error testing the crew: {e}")
