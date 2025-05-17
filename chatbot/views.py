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
import os

# Load vectorstore only once
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectorstore = Chroma(persist_directory="./Chroma", embedding_function=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Prompt
custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a chatbot deployed on a Netflix Clone website. You chat with users and answer politely.

Whenever they ask for movie suggestions or queries, refer to the context below. If the movie isn't listed, say it's not available yet but will be soon.

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

# llm = DeepSeekLLM(api_key=os.getenv("DEEPSEEK_API_KEY"))  # Or hardcode it (not recommended)
# llm = DeepSeekLLM(api_key="sk-blah blah")  # Or hardcode it (not recommended)

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

            # Get full response from LangChain
            response = qa_chain.invoke({"question": user_message, "chat_history": chat_history})

            # Extract just the answer (you might update chat_history too if needed)
            answer = response.get("answer", "Sorry, I couldn't find an answer.")

            return JsonResponse({"response": answer})
        except Exception as e:
            print("Error in chatbot view:", e)
            return JsonResponse({"response": f"Server error: {str(e)}"}, status=500)
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
