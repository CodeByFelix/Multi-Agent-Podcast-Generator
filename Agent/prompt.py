PodcastDetailPrompt = """
You are tasked with extracting and generating structured podcast details based on the input description provided by the user.

From the user's message, identify and generate the following:
- **Podcast Topic**
- **Discussion Area or Focus**
- **Interviewer Name** (leave empty if not mentioned)
- **Interviewer Gender** (leave empty if not mentioned)
- **Expert Name** (leave empty if not mentioned)
- **Expert Gender** (leave empty if not mentioned)

If a name or gender is not explicitly mentioned in the input, do not infer or guess — leave the corresponding field blank.

Ensure your response is accurate and clearly structured for use in further processing.
"""

feedbackPrompt = """
You are an intelligent assistant that evaluates user feedback during a podcast creation process.

You will be provided with:
- Podcast topic
- Focus area of the discussion
- Interviewer name and gender
- Expert name and gender
- Focus points covered so far

Your task is to analyze the user's feedback and determine if it:
1. **Requests a change** in the podcast details (e.g., editing topic, names, focus points, etc.)
2. **Asks for additional features or adjustments** to be made before continuing
3. Or simply indicates satisfaction and a desire to **continue execution** without changes.

Here are the details for the podcast so far:
Podcast Topic: {topic}
Discussion Area: {discusionArea}
Interviewer's Name: {interviewerName}
Interviewer's gender: {interviewer}
Expert's Name: {expertName}
Experst's gender {expert}
Main Focus Point of the Interview: {focusPoint}

Return:
- **True** → if the feedback requires a modification or update to the podcast content.
- **False** → if the feedback implies that the agent should proceed with execution as it is.

Respond only with a boolean: `True` or `False`.
"""

PodcastDetailPromptFeedback = """
You are tasked with modifying the podcast details based on human feedback.

Use the feedback to update any of the following fields **only if the feedback clearly specifies a change**:
- Podcast Topic
- Discussion Area
- Interviewer's Name and Gender
- Expert's Name and Gender

If the feedback does not provide new values for any field, retain the original values.  
**Do not guess or infer** missing information. If a name or gender is not explicitly stated, retain previous value.

Here are the current podcast details:
- Podcast Topic: {topic}
- Discussion Area: {discusionArea}
- Interviewer's Name: {interviewerName}
- Interviewer's Gender: {interviewer}
- Expert's Name: {expertName}
- Expert's Gender: {expert}

Now modify the details accordingly based on the user’s feedback.
Respond with only the updated podcast details in the same format.
"""

searchQueryPrompt = """Todays date is {today}
You are tasked with generating a search querry for a web search.
The websearch will be used to generate Focus areas or subtopics to guid a podcast discusion.
The details to use for the generation of the search querries are as follows:
Podcast Topic: {topic}
Discussion Arean: {discusionArea}

"""

searchQueryPromptFeedback = """Todays date is {today}
You are tasked with generating a search querry for a web search.
The websearch will be used to generate Focus areas or subtopics to guide a podcast discusion.
The details to use for the generation of the search querries are as follows:
Podcast Topic: {topic}
Discussion Arean: {discusionArea}

Also consider the human feedback given to the system.
here is the feedback: {feedback}
"""

discusionPointPrompt = """You are tasked with generating a focus area, subtopics or discusion points to guide a podcast
The details of the podcast are as follows:
Podcast Topic: {topic}
Discussion Arean: {discusionArea}

You will be provided with a context. The context is a web search result which was retrieve with respect to the podcast topic and discussion are.
You will genrate the focus area and discusion points to guide the podcast
The purpose of the context is to guide you through recent news and happening.
use your knowledge augumented with the context to generate a well structured conversation points to guide the podcast

here is the context: {context}"""


discusionPointPromptFeedback = """You are tasked with generating a focus area, subtopics or discusion points to guide a podcast
The details of the podcast are as follows:
Podcast Topic: {topic}
Discussion Arean: {discusionArea}

You will be provided with a context. The context is a web search result which was retrieve with respect to the podcast topic and discussion are.
You will genrate the focus area and discusion points to guide the podcast
The purpose of the context is to guide you through recent news and happening.
use your knowledge augumented with the context to generate a well structured conversation points to guide the podcast

here is the context: {context}

These conversation points have been generated ealier, but there was a human feedback for a few modification.
You take the old points, regenrate it while considering the human feedback
The old points are shown below:
{oldPoints}

here is the human feedback {feedback}"""


interviewQuestionPrompt = """
You are the host of a podcast and an experienced interviewer.

Craft the next **engaging and context-aware** question for the expert, based on the following:
- The overall podcast topic
- The discussion area or focus of the conversation
- A specific **focus point** this question should center on
- The **previous conversation** between you and the expert

Be intuitive and conversational. Make sure the question naturally follows the flow of the ongoing discussion.

Also, take into account the gender of the interviewer and reflect it subtly in your tone and expression.

Here are the podcast details:
- Podcast Topic: {topic}
- Discussion Area: {discusionArea}
- Interviewer's Gender: {interviewer}
- Expert's Name: {expertName}
- Focus Point for the Question: {focusPoint}

Previous conversation transcript:
{podcast}
"""

responseQueryPrompt = """Todays date is {date}
You are tasked with generating a querry to make a web search.
The web search will be used to retrieve context to assist the expert to responde to a podcast question

The details of the podcast is as follows:
Podcast Topic: {topic}
Discusion Area: {discusionArea}

Here is the podcast question: {question}"""


expertResponsePrompt = """
You are a knowledgeable expert invited to speak on a podcast.

Your area of expertise aligns with the podcast topic, and you're expected to respond to the interviewer's latest question thoughtfully and informatively.

Consider the following when crafting your response:
- The podcast topic and discussion area
- **Recent web-based context** provided to keep your answer updated and relevant
- Your **gender**, and reflect it naturally in your tone
- The **flow of previous conversation** so your response feels like a natural continuation

Speak in a friendly, confident, and engaging tone suitable for a podcast audience.

Here are the podcast details:
- Podcast Topic: {topic}
- Discussion Area: {discusionArea}
- Expert Gender: {expert}
- Interviewer's Name: {interviewerName}

Recent context retrieved from the web:
{context}

Previous conversation transcript:
{podcast}
"""

podcastIntroPromptInterviewer = """
You are to generate a compelling and engaging introduction speech for a podcast episode. The introduction will be delivered by the interviewer.

The speech must include the following elements:
1. A warm self-introduction from the interviewer.
2. The name of the podcast.
3. A brief explanation of the podcast's focus area and what it offers to listeners.
4. A preview of what the audience should expect from the current episode.
5. An introduction of the expert guest joining the episode.
6. A clear mention of the main focus point around which the discussion will be centered.

Make the tone conversational, energetic, and inviting—designed to immediately capture the listener's attention and make them eager to hear more.

Here are the details for this episode:
Podcast Topic: {topic}
Discussion Area: {discusionArea}
Interviewer's Name: {interviewerName}
Expert's Name: {expertName}
Main Focus Point of the Interview: {focusPoint}

Keep the response concise no longer than 50 words. Avoid rambling or repeating ideas.
"""


podcastIntroPromptExpert = """
You are to generate a welcoming and insightful opening response from the expert guest on a podcast.

The expert's response should:
1. Briefly thank the host/interviewer for the invitation.
2. Express enthusiasm about being part of the podcast.
3. Mention the relevance and importance of the podcast topic.
4. Provide a short background/introduction of themselves (relevant to the topic).
5. Briefly highlight why this topic or focus point matters to the audience.
6. Set a positive tone for the conversation ahead, without revealing too much.

Make the response warm, authentic, and professional. The goal is to establish credibility while making the audience excited about what's to come.

Here are the episode details:
Podcast Topic: {topic}
Discussion Area: {discusionArea}
Interviewer's Name: {interviewerName}
Expert's Name: {expertName}
Main Focus Point of the Interview: {focusPoint}

Keep the response concise no longer than 50 words. Avoid rambling or repeating ideas.
"""

podcastEndingPrompt = """
You are an expert podcast scriptwriter. Your task is to generate a warm, appreciative, and professional **closing speech** from the interviewer at the end of a podcast episode.

The speech should be written **from the perspective of the interviewer** and should be stored in a variable named **interviewerClosingSpeech**.

The speech must include the following elements:
1. A heartfelt appreciation to the **expert guest** for their time, insights, and contribution.
2. Gratitude to the **audience** for tuning in and listening.
3. A brief recap or reference to the key takeaway(s) from the conversation (based on provided conversation details).
4. Encouragement to the audience to reflect on or take action related to the episode’s theme.
5. A call-to-action (e.g., subscribe, leave feedback, share the podcast).
6. A friendly and professional sign-off.

Use a tone that is conversational, warm, and uplifting—suitable for ending a valuable and insightful podcast episode.

Use the information below to generate the closing speech:
odcast Topic: {topic}
Discussion Area: {discusionArea}
Interviewer's Name: {interviewerName}
Expert's Name: {expertName}
Focus Point of the Interview: {focusPoint}
Conversation Summary or Highlights: {conversation}

Keep the response concise no longer than 50 words. Avoid rambling or repeating ideas.
"""