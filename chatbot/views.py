from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage  # Assuming your model exists
import json

# LangChain imports
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from .deepseek_llm import DeepSeekLLM  # your custom LLM class
from .openrouter import DeepSeekRouterLLM
import os
import json
import re
def clean_plaintext(answer):
    # Remove triple backticks and plaintext blocks
    answer = re.sub(r"```(?:plaintext)?\n?([\s\S]*?)```", r"\1", answer)
    answer = re.sub(r"```(?:text)?\n?([\s\S]*?)```", r"\1", answer)
    answer = re.sub(r"```(?:html)?\n?([\s\S]*?)```", r"\1", answer)
    # Strip leading/trailing whitespace
    return answer.strip()
# Load vectorstore only once
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectorstore = Chroma(persist_directory="./Chroma", embedding_function=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful and polite chatbot deployed on a Netflix Clone website. Your role is to assist users with movie or TV show suggestions and answer queries using the context provided.

Formatting Rules:
- DO NOT use markdown formatting (no triple backticks, no asterisks, no hashtags).
- Use UPPERCASE for movie/show titles if emphasis is needed.
- Use numbered lists (1., 2., etc.) or dashes (-) for clarity.
- Use line breaks between sections and entries.
- Ensure responses are clean and ready for direct HTML/text display.

If a movie/show is not found in the context, politely inform the user it's not available yet but may be added soon.

Example Response:

Hi there! I'm here to help you find great content.

Here are a few suggestions you might enjoy:

1. THE GOOD PLACE  
   Genre: Comedy, Fantasy, Mystery  
   Plot: A woman finds herself in the afterlife — but things aren't what they seem.  
   Stars: Kristen Bell, William Jackson Harper, Jameela Jamil

2. THE SOCIAL NETWORK  
   Genre: Biography, Drama  
   Plot: The story behind the creation of Facebook and the conflicts that followed.  
   Stars: Jesse Eisenberg, Andrew Garfield, Justin Timberlake

If you’d like more suggestions or have another question, feel free to ask!

Context:
{context}

User Question:
{question}

Answer:
"""
)
condense_prompt = PromptTemplate.from_template("""
Given the following conversation and a follow-up question, rephrase the follow-up to be a standalone question.


Chat History:
{chat_history}

Follow Up Question: {question}

Standalone Question:
""")

# #llm = DeepSeekLLM(api_key=os.getenv("DEEPSEEK_API_KEY"))  # Or hardcode it (not recommended)
# llm = DeepSeekLLM(api_key="sk-blah blah")  # Or hardcode it (not recommended)
llm = DeepSeekRouterLLM(api_key=os.getenv("OPENROUTER_API_KEY"))

qa_llm_chain = LLMChain(llm=llm, prompt=custom_prompt)
question_generator_chain = LLMChain(llm=llm, prompt=condense_prompt)
combine_docs_chain = StuffDocumentsChain(llm_chain=qa_llm_chain, document_variable_name="context")

qa_chain = ConversationalRetrievalChain(
    retriever=retriever,
    memory=memory,
    combine_docs_chain=combine_docs_chain,
    question_generator=question_generator_chain,
    verbose=False
)

@csrf_exempt
def chatbot_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Get chatbot response
            response = qa_chain.invoke({
                "question": user_message,
                "chat_history": chat_history
            })

            # Normalize output
            if isinstance(response, dict):
                answer = response.get("answer", "Sorry, I couldn't find an answer.")
            elif isinstance(response, str):
                try:
                    parsed = json.loads(response)
                    answer = parsed.get("answer", response)
                    answer = clean_plaintext(answer)
                except json.JSONDecodeError:
                    answer = response
                    answer = clean_plaintext(answer)
            else:
                answer = str(response)
                answer = clean_plaintext(answer)

            return JsonResponse({"response": clean_plaintext(answer)})

        except Exception as e:
            print("Error in chatbot view:", e)
            return JsonResponse(
                {"response": "Sorry, I encountered an error. Please try again later."},
                status=500
            )
def chat_history(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:50]
    return JsonResponse({
        'messages': [
            {
                'message': msg.message,
                'response': msg.response,
                'timestamp': msg.created_at.isoformat()
            }
            for msg in messages
        ]
    })
