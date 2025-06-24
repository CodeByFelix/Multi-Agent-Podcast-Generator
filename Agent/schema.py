from typing import List, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from operator import add

class PodcastDetail (BaseModel):
    topic: str = Field (description="The topic of the podcast")
    discusionArea: str = Field (description="Specific area of intrest or angle of the main topic")
    interviewer: str = Field (description="The gender of the interviewer, it shuld be either male or female.")
    expert:str = Field (description="The gender of the expert. it should be either male or female.")
    interviewerName: str = Field (description= "The name of the interviewer")
    expertName: str = Field (description="The name of the Expert to respond the interview")

class Discusionpoints (BaseModel):
    focusPoints: List[str] = Field (description="Focus or subtopics to guide the discusion for broader and good understanding")

class SearchQuery (BaseModel):
    searchQuery: str = Field (description="A query to be used for websearh")

class Feedback (BaseModel):
    feedback: bool = Field (description="A boolean to specify if the human gave a feedback or not. True for feedback, False for No feedback") 

class InputMessage (TypedDict):
    message: str #The input message to the Podcast
    podcastDetail: PodcastDetail #The Podcast Details
    searchQuery: str #Search Querry for the web search
    context: Annotated [List, add] #List of context from the websearch
    focusPoints : List[str] #Focus points for the Podcast
    humanFeedback: str #Human feedback
    feedback: bool  #A boolean to show if a feedback was given

class InterviewQuestion (BaseModel):
    question:str = Field(description="Question from the interviewer")

class ExpertResponse (BaseModel):
    response: str = Field(description="Response from the expert")

class Podcast (TypedDict):
    podcastDetails: PodcastDetail
    focusPoint: str
    question: str
    contexts: Annotated [list, add]
    conversation: Annotated[list, add]

class PodcastIntro (BaseModel):
    intro: str = Field (description="Intro statement to the podcast by both the interviewer and expert")

class PodcastEnding (BaseModel):
    ending: str = Field (description="Ending statement to the podcast")

class PodcastSchema (TypedDict):
    message: str #The input message to the Podcast
    podcastDetail: PodcastDetail #The Podcast Details
    searchQuery: str #Search Querry for the web search
    context: Annotated [List, add] #List of context from the websearch
    focusPoints : List[str] #Focus points for the Podcast
    humanFeedback: str #Human feedback
    feedback: bool  #A boolean to show if a feedback was given
    conversation: Annotated[list, add] #Generated conversation for the podcast
    intro: Annotated[list, add]
    ending: Annotated[list, add]
    fileName: str #Name used to store the audio file