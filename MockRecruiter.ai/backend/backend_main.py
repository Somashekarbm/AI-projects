# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import requests
# from pydantic import BaseModel
# # from llama_index.llms.ollama import Ollama
# # from langchain_community.llms import Ollama
# # from langchain_ollama import OllamaLLM
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (including OPTIONS)
#     allow_headers=["*"],  # Allow all headers
# )

# # Load Open-Source LLM (Mixtral or OpenChat)
# # llm = OllamaLLM(model="llama3")  


# # llm = ChatOllama(
# #     model = "llama2",
# #     temperature = 0.8,
# #     num_predict = 256,
# #     # other params ...
# # )

# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# class UserResponse(BaseModel):
#     question: str
#     answer: str


# # grading_prompt = PromptTemplate.from_template(
# #     "Evaluate the following interview response:\nQuestion: {question}\nAnswer: {answer}\nProvide a rating from 1-10 and specific feedback."
# # )
# # output_parser = StrOutputParser()
# # grading_chain = grading_prompt | llm | output_parser

# @app.post("/evaluate") 
# async def evaluate_response(user_response: UserResponse):
#     prompt = f"Evaluate this interview response:\nQuestion: {user_response.question}\nAnswer: {user_response.answer}\nProvide feedback."

#     response = requests.post(OLLAMA_URL, json={
#         "model": "gemma2:2b",
#         "prompt": prompt,
#         "stream": False  # Important! Ollama expects this parameter
#     })
    
#     if response.status_code != 200:
#         error_detail = response.text  # Capture Ollama error response
#         raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {error_detail}")

#     feedback = response.json().get("response", "No feedback received.")
#     return {"feedback": feedback}



# # interviewer_styles = {
# #     "friendly": "Respond with a supportive and encouraging tone.",
# #     "strict": "Provide tough and critical feedback as a serious interviewer.",
# #     "technical": "Focus on technical depth and correctness."
# # }

# # @app.post("/evaluate/{persona}")
# # async def evaluate_with_persona(persona: str, user_response: UserResponse):
# #     if persona not in interviewer_styles:
# #         raise HTTPException(status_code=400, detail="Invalid persona. Choose from: friendly, strict, technical.")
    
# #     style = interviewer_styles.get(persona, "Provide neutral feedback.")
# #     prompt = f"{style}\nEvaluate this interview response:\nQuestion: {user_response.question}\nAnswer: {user_response.answer}\nProvide a detailed evaluation."
    
# #     response = llm.invoke({"prompt": prompt})

# #     return {"feedback": response}



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

class UserResponse(BaseModel):
    question: str
    answer: str

logging.basicConfig(level=logging.DEBUG)

@app.get("/")
async def root():
    return {"message": "MockRecruiter Backend is Running"}


@app.post("/evaluate")
async def evaluate_response(user_response: UserResponse):
    prompt = f"Evaluate this interview response:\nQuestion: {user_response.question}\nAnswer: {user_response.answer}\nProvide feedback."

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "gemma2:2b",
            "prompt": prompt,
            "stream": False
        }, timeout=150)

        logging.debug(f"Ollama Response: {response.status_code} - {response.text}")

        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        feedback = response.json().get("response", "No feedback received.")
        return {"feedback": feedback}

    except requests.exceptions.ConnectionError:
        logging.error("Could not connect to Ollama. Is it running?")
        raise HTTPException(status_code=503, detail="Could not connect to Ollama. Ensure it's running on 127.0.0.1:11434.")
    except requests.exceptions.Timeout:
        logging.error("Request to Ollama timed out.")
        raise HTTPException(status_code=504, detail="Request to Ollama timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ollama request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ollama request failed: {str(e)}")









