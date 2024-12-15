from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Import 
from app.agents.preprocessor_node import QueryPreprocessorNode
from app.agents.jda_node import JDANode
from app.agents.suggestor_node import SuggestorNode
from app.agents.resume_rephraser_node import ResumeRephraserNode
from app.agents.cover_letter_rephraser_node import CoverLetterRephraserNode
from app.agents.craft_resume_node import CraftResumeNode
from app.agents.craft_cover_letter_node import CraftCoverLetterNode

from app.routers import (
    handle_doc_type,
)
from app.types.node_state import NodeState
from app.types.config_schema import ConfigSchema

graph_builder = StateGraph(state_schema=NodeState, config_schema=ConfigSchema)

# Add Nodes
graph_builder.add_node(node="query_preprocessor", action=QueryPreprocessorNode())
graph_builder.add_node(node="jd_analysis", action=JDANode())
graph_builder.add_node(node="exp_suggestor", action=SuggestorNode())
graph_builder.add_node(node="resume_rephraser", action=ResumeRephraserNode())
graph_builder.add_node(node="cover_letter_rephraser", action=CoverLetterRephraserNode())
graph_builder.add_node(node="craft_resume", action=CraftResumeNode())
graph_builder.add_node(node="craft_cover_letter", action=CraftCoverLetterNode())


# # Add edges 
graph_builder.add_edge(START, "query_preprocessor")

graph_builder.add_edge("query_preprocessor", "jd_analysis")
graph_builder.add_edge("jd_analysis", "exp_suggestor")


graph_builder.add_conditional_edges(
    "exp_suggestor",
    handle_doc_type,
    {
        "resume_rephraser": "resume_rephraser",
        "cover_letter_rephraser": "cover_letter_rephraser"
    }
)

graph_builder.add_edge("resume_rephraser", "craft_resume")
graph_builder.add_edge("cover_letter_rephraser", "craft_cover_letter")

graph_builder.add_edge("craft_cover_letter", END)
graph_builder.add_edge("craft_resume", END)


# Compile graph
checkpointer = MemorySaver()
graph = graph_builder.compile(
    checkpointer=checkpointer,
)