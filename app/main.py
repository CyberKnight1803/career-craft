from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Import agent nodes and handlers
from app.agents.preprocessor_node import QueryPreprocessorNode
from app.agents.jda_node import JDANode
from app.agents.suggestor_node import SuggestorNode
from app.agents.resume_rephraser_node import ResumeRephraserNode
from app.agents.cover_letter_rephraser_node import CoverLetterRephraserNode
from app.agents.craft_resume_node import CraftResumeNode
from app.agents.craft_cover_letter_node import CraftCoverLetterNode
from app.agents.handler_nodes import get_missing_jd, get_missing_intent

from app.routers import handle_doc_type, handle_missing_info
from app.types.node_state import NodeState
from app.types.config_schema import ConfigSchema

# Initialize the StateGraph with schemas for state management and configuration
graph_builder = StateGraph(state_schema=NodeState, config_schema=ConfigSchema)

# Add Nodes: These define the individual processing steps in the workflow
graph_builder.add_node(node="query_preprocessor", action=QueryPreprocessorNode())
graph_builder.add_node(node="jd_analysis", action=JDANode())
graph_builder.add_node(node="exp_suggestor", action=SuggestorNode())
graph_builder.add_node(node="resume_rephraser", action=ResumeRephraserNode())
graph_builder.add_node(node="cover_letter_rephraser", action=CoverLetterRephraserNode())
graph_builder.add_node(node="craft_resume", action=CraftResumeNode())
graph_builder.add_node(node="craft_cover_letter", action=CraftCoverLetterNode())

# Add handler nodes for missing data
graph_builder.add_node(node="get_missing_jd", action=get_missing_jd)
graph_builder.add_node(node="get_missing_intent", action=get_missing_intent)

# Define conditional edges based on preprocessing results
# Routes based on missing information
graph_builder.add_conditional_edges(
    "query_preprocessor",
    handle_missing_info,
    {
        "get_missing_jd": "get_missing_jd",  # Route to handle missing job descriptions
        "get_missing_intent": "get_missing_intent",  # Route to handle missing intent
        "jd_analysis": "jd_analysis"  # Continue with JD analysis if all required info is present
    }
)

# Define edges for handling missing information
graph_builder.add_edge("get_missing_jd", "query_preprocessor")
graph_builder.add_edge("get_missing_intent", "query_preprocessor")

# Define edges for job description analysis and suggestion phases
graph_builder.add_edge("jd_analysis", "exp_suggestor")

# Define conditional edges for document type handling
graph_builder.add_conditional_edges(
    "exp_suggestor",
    handle_doc_type,
    {
        "resume_rephraser": "resume_rephraser",  # Route for crafting resumes
        "cover_letter_rephraser": "cover_letter_rephraser"  # Route for crafting cover letters
    }
)

# Define edges for rephrasing and crafting steps
graph_builder.add_edge("resume_rephraser", "craft_resume")
graph_builder.add_edge("cover_letter_rephraser", "craft_cover_letter")

# End points for the workflow
graph_builder.add_edge("craft_cover_letter", END)
graph_builder.add_edge("craft_resume", END)

# Set the entry point for the workflow
graph_builder.set_entry_point("query_preprocessor")

# Compile the graph with a checkpointing mechanism for state persistence
checkpointer = MemorySaver()
graph = graph_builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["get_missing_jd", "get_missing_intent"],  # Interrupt points for user input
    interrupt_after=[]  # No interruptions post these nodes
)
