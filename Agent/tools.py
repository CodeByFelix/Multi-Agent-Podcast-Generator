import os
from .schema import *
from .prompt import *
from datetime import datetime
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.constants import Send
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from pydub import AudioSegment
from google.cloud import texttospeech
from dotenv import load_dotenv




def createPodcastDetails (state: InputMessage) -> InputMessage:
    if state['feedback']:
        initialDetaild = state['podcastDetail']
        sys_msg = PodcastDetailPromptFeedback.format (topic=initialDetaild.topic,
                                                      discusionArea=initialDetaild.discusionArea,
                                                      interviewerName=initialDetaild.interviewerName,
                                                      interviewer=initialDetaild.interviewer,
                                                      expertName=initialDetaild.expertName,
                                                      expert=initialDetaild.expert)
        podcastDetails = podcastDetail_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content=state['humanFeedback'])])

        today = datetime.today().strftime("%Y-%m-%d")
        sys_msg = searchQueryPromptFeedback.format (today=today, topic=podcastDetails.topic, discusionArea=podcastDetails.discusionArea, feedback=state['humanFeedback'])

        searchQuery = searchQuerry_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content="Generate the search querry")])
        print (searchQuery.searchQuery)

        return {'podcastDetail': podcastDetails, 'searchQuery': searchQuery.searchQuery}

    else:
        sys_msg = PodcastDetailPrompt
        podcastDetails = podcastDetail_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content=state['message'])])

        today = datetime.today().strftime("%Y-%m-%d")
        sys_msg = searchQueryPrompt.format (today=today, topic=podcastDetails.topic, discusionArea=podcastDetails.discusionArea)

        searchQuery = searchQuerry_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content="Generate the search querry")])
        print (searchQuery.searchQuery)

        return {'podcastDetail': podcastDetails, 'searchQuery': searchQuery.searchQuery}


def webSearch (state: InputMessage) -> InputMessage:
    query = state['searchQuery']
    search_doc = tavily_search.invoke (query)

    formated_docs = '\n\n'.join (
        [f'<Document href="{doc['url']}"/>\n{doc['content']}\n</Document>' for doc in search_doc]
    )

    return {'context': [formated_docs]}
    
def wikipediaSearch (state: InputMessage) -> InputMessage:
    query = state['searchQuery']
    search_doc = WikipediaLoader(query=query, load_max_docs=3).load()


    formated_docs = '\n\n'.join (
        [f'<Document href="{doc.metadata['source']}"/>\n{doc.page_content}\n</Document>' for doc in search_doc]
    )

    return {'context': [formated_docs]}

def generatePoints (state: InputMessage) -> InputMessage:
    
    if state ['feedback']:
        podcastDetails = state['podcastDetail']
        context = state['context']
        context = "\n\n".join (context)
        oldPoints = "\n".join (state['focusPoints'])
        feedback = state['humanFeedback']

        sys_msg = discusionPointPromptFeedback.format (topic=podcastDetails.topic, discusionArea=podcastDetails.discusionArea, context=context, oldPoints=oldPoints, feedback=feedback)
        discusionPoints = discusionPoints_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage (content="Generate the Coversation points")])
        print (discusionPoints.dict())
        return {'focusPoints': discusionPoints.focusPoints}

    else:
        podcastDetails = state['podcastDetail']
        context = state['context']
        context = "\n\n".join (context)

        sys_msg = discusionPointPrompt.format (topic=podcastDetails.topic, discusionArea=podcastDetails.discusionArea, context=context)
        discusionPoints = discusionPoints_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage (content="Generate the Coversation points")])
        print (discusionPoints.dict())
        return {'focusPoints': discusionPoints.focusPoints}
    

    
def humanFeedback (state: InputMessage):
    "No opps node"
    pass

def processFeedback (state: InputMessage) -> InputMessage:
    feedback = state ['humanFeedback']
    podcastDetail = state['podcastDetail']
    focusPoint = state['focusPoints']
    print (f"Feedback is {feedback}")
    
    sys_msg = feedbackPrompt.format (topic=podcastDetail.topic,
                                     discusionArea=podcastDetail.discusionArea,
                                     interviewerName=podcastDetail.interviewerName,
                                     interviewer=podcastDetail.interviewer,
                                     expertName=podcastDetail.expertName,
                                     expert=podcastDetail.expert,
                                     focusPoint=focusPoint)
    feedback_bool = feedback_llm.invoke([SystemMessage (content=sys_msg)] + [HumanMessage(content=feedback)])

    print ("\n\n\n", feedback_bool.feedback)

    print ("\n\nExecuted Human Feedback\n\n")

    return {'feedback': feedback_bool.feedback}

def generateQuestion (state: Podcast) -> Podcast:
    podcastDetail = state['podcastDetails']
    focusPoint = state ['focusPoint']
    con = state.get ('conversation', [])
    if con:
        conversation = "\n\n".join (con)

    else:
        conversation = "No interview yet"
    sys_msg = interviewQuestionPrompt.format (topic=podcastDetail.topic,
                                          discusionArea=podcastDetail.discusionArea,
                                          interviewer=podcastDetail.interviewer,
                                          expertName=podcastDetail.expertName,
                                          focusPoint=focusPoint,
                                          podcast=conversation)

    interviewQuestion = interviewQuestion_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content="Generate the interview question")])
    
    return {'question': interviewQuestion.question, 'conversation': [("interviewer", interviewQuestion.question)]}

def generateResponse (state: Podcast) -> Podcast:
    podcastDetail = state ['podcastDetails']
    question = state['question']
    today = datetime.today().strftime("%Y-%m-%d")
    sys_msg_query = responseQueryPrompt.format (date=today,
                                        topic=podcastDetail.topic,
                                        discusionArea=podcastDetail.discusionArea,
                                        question=question)

    searchQuery = searchQuerry_llm.invoke ([SystemMessage(content=sys_msg_query)] + [HumanMessage(content="Generate the search query")])

    search_doc = tavily_search.invoke(searchQuery.searchQuery)
    formated_docs = '\n\n'.join (
            [f'<Document href="{doc['url']}"/>\n{doc['content']}\n</Document>' for doc in search_doc]
        )

    formated_docs

    con = state.get ('conversation', [])
    if con:
        conversation = "\n\n".join ([c[0] + "\n" + c[1] for c in con])

    else:
        conversation = "No interview yet"

    sys_msg = expertResponsePrompt.format (topic=podcastDetail.topic,
                                       discusionArea=podcastDetail.discusionArea,
                                       expert=podcastDetail.expert,
                                       interviewerName=podcastDetail.interviewerName,
                                       context=formated_docs,
                                       podcast=conversation)

    expertResponse = expertResponse_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content=question)])
    
    '''
    conver = f"""Interviewer:
    {question}

    Expert:
    {expertResponse.response}
    """
    '''

    return {'contexts': [formated_docs], 'conversation': [('expert', expertResponse.response)]}


def shoulContinue (state:PodcastSchema):
    feedback = state['feedback']
    print ("\n\nExecuting condition loop\n")
    if feedback:
        return 'create podcast details'
    
    else:
        return [Send ('generate podcast interviews', {'podcastDetails': state['podcastDetail'],
                                                      'focusPoint': focusPoint}) for focusPoint in state['focusPoints']]
    
    
def generatePodcastIntroEnding (state: PodcastSchema) -> PodcastSchema:
    podcastDetail = state['podcastDetail']
    focusPoint = "\n".join (state['focusPoints'])
    sys_msg = podcastIntroPromptInterviewer.format (topic=podcastDetail.topic,
                                                    discusionArea=podcastDetail.discusionArea,
                                                    interviewerName=podcastDetail.interviewerName,
                                                    expertName=podcastDetail.expertName,
                                                    focusPoint = focusPoint)
    
    podcastIntroInterviewer = podcastIntro_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content="Generate the Podcast Intro by the Interviewer")])

    sys_msg = podcastIntroPromptExpert.format (topic=podcastDetail.topic,
                                                    discusionArea=podcastDetail.discusionArea,
                                                    interviewerName=podcastDetail.interviewerName,
                                                    expertName=podcastDetail.expertName,
                                                    focusPoint = focusPoint)
    
    podcastIntroExpert = podcastIntro_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content="Generate the Podcast Intro by the Expert")])

    con = state.get ('conversation', [])
    if con:
        conversation = "\n\n".join ([c[0] + "\n" + c[1] for c in con])
    sys_msg = podcastEndingPrompt.format (topic=podcastDetail.topic,
                                                    discusionArea=podcastDetail.discusionArea,
                                                    interviewerName=podcastDetail.interviewerName,
                                                    expertName=podcastDetail.expertName,
                                                    focusPoint = focusPoint,
                                                    conversation=conversation)
    
    podcastEnding = podcastEnding_llm.invoke ([SystemMessage(content=sys_msg)] + [HumanMessage(content="Generate the podcast ending message by the interviewer")])
    
    return {'ending': [('interviewer', podcastEnding.ending)], 'intro': [('interviewer', podcastIntroInterviewer.intro), ('expert', podcastIntroExpert.intro)]}

def save (audio, fileName:str):
    with open (fileName, "wb") as output:
        output.write (audio.audio_content)


def generatePodcastAudio (state: PodcastSchema) -> PodcastSchema :
    femaleVoiceCode = "en-US-standard-C"
    maleVoiceCode = "en-US-standard-A"
    podcastDetail = state['podcastDetail']
    interviewerVoiceCode = femaleVoiceCode if podcastDetail.interviewer == 'female' else maleVoiceCode
    expertVoiceCode = femaleVoiceCode if podcastDetail.expert == 'female' else maleVoiceCode

    podcast = state['intro'] + state['conversation'] + state['ending']
    
    now = datetime.now ()
    folderName = now.strftime ("output_%Y-%m-%d_%H-%M-%S")
    os.makedirs (folderName, exist_ok=True)
    client = texttospeech.TextToSpeechClient()
    interviewerVoice = texttospeech.VoiceSelectionParams(language_code="en-US", name=interviewerVoiceCode)
    expertVoice = texttospeech.VoiceSelectionParams(language_code="en-US", name=expertVoiceCode)

    audio_config = texttospeech.AudioConfig (audio_encoding=texttospeech.AudioEncoding.MP3,
                                         effects_profile_id = ['small-bluetooth-speaker-class-device'],
                                         speaking_rate=1,
                                         pitch=1)

    for i, (speaker, text) in enumerate (podcast):
        voice = interviewerVoice if speaker == 'interviewer' else expertVoice
        synthesis_input = texttospeech.SynthesisInput (text=text)
        responseAudio = client.synthesize_speech (input=synthesis_input,
                                     voice=voice,
                                     audio_config=audio_config)
        save (responseAudio, f"{folderName}/line_{i:02d}.mp3")

    podcastAudio = AudioSegment.silent (duration=500)

    for audioFile in os.listdir(folderName):
        audio = AudioSegment.from_mp3 (f"{folderName}/{audioFile}")
        podcastAudio += audio + AudioSegment.silent(duration=500)
    
    fileName = f"{folderName}/Podcast Audio.mp3"
    podcastAudio.export (fileName, format="mp3")

    return {'fileName': fileName}
    


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv ("LANGCHAIN_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("tavily-apiKey")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ ['LANGCHAIN_PROJECT'] = 'langchain-accademy'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "Google Credential.json"
llm = ChatOpenAI (model='gpt-4.1-nano')
discusionPoints_llm = llm.with_structured_output (Discusionpoints)
podcastDetail_llm = llm.with_structured_output (PodcastDetail)
searchQuerry_llm = llm.with_structured_output (SearchQuery)
feedback_llm = llm.with_structured_output (Feedback)
interviewQuestion_llm = llm.with_structured_output (InterviewQuestion)
expertResponse_llm = llm.with_structured_output (ExpertResponse)
podcastIntro_llm = llm.with_structured_output (PodcastIntro)
podcastEnding_llm = llm.with_structured_output (PodcastEnding)
tavily_search = TavilySearchResults (max_results=4)