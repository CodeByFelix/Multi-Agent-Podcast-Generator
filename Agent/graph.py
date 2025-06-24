from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver
from .tools import *
from .schema import PodcastSchema, Podcast

def conversationGraph () -> CompiledStateGraph:
    builder = StateGraph (Podcast)
    builder.add_node ('generate question', generateQuestion)
    builder.add_node ('generate response', generateResponse)

    builder.add_edge (START, 'generate question')
    builder.add_edge ('generate question', 'generate response')
    builder.add_edge ('generate response', END)

    graph = builder.compile ()
    return graph

def graph () -> CompiledStateGraph:
    podcastBuilder = StateGraph (PodcastSchema)
    podcastBuilder.add_node ('create podcast details', createPodcastDetails)
    podcastBuilder.add_node ('web search', webSearch)
    podcastBuilder.add_node ('generate points',generatePoints)
    podcastBuilder.add_node ('human feedback', humanFeedback)
    podcastBuilder.add_node ('process feedback', processFeedback)
    podcastBuilder.add_node ('generate podcast interviews', conversationGraph())
    podcastBuilder.add_node ('generate intro and ending', generatePodcastIntroEnding)
    podcastBuilder.add_node ('generate podcast audio', generatePodcastAudio)


    podcastBuilder.add_edge (START, 'create podcast details')
    podcastBuilder.add_edge ('create podcast details', 'web search')
    podcastBuilder.add_edge ('web search', 'generate points')
    podcastBuilder.add_edge ('generate points', 'human feedback')
    podcastBuilder.add_edge ('human feedback', 'process feedback')
    podcastBuilder.add_conditional_edges ('process feedback', shoulContinue, ['create podcast details', 'generate podcast interviews'])
    podcastBuilder.add_edge ('generate podcast interviews', 'generate intro and ending')
    podcastBuilder.add_edge ('generate intro and ending', 'generate podcast audio')
    podcastBuilder.add_edge ('generate podcast audio', END)


    memory = MemorySaver ()
    podcastGraph = podcastBuilder.compile (interrupt_after=['generate points'], checkpointer=memory)
    return podcastGraph