from fastapi import FastAPI , HTTPException,status
from confluent_kafka import Producer 
import json, time , hashlib 
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()
kafka = Producer({'bootstrap.servers': 'localhost:9092'}) 

def log_to_kafka(data : dict):
    'fire and forget never blocks the response.'
    kafka.produce('llm_logs', key = data['user_id'],value = json.dumps(data).encode('utf-8'))
    kafka.poll(0)
    

@app.post('/chat')
async def chat(user_id: str, prompt: str):
    start_time = time.time()
    
    try:
        # Use the async version of the generate_content method
        response = await model.generate_content_async(prompt)
        tokens_in_use = len(prompt.split()) + len(response.text.split())
        
        duration = time.time() - start_time
        
        # Log the request and response to Kafka
        log_to_kafka({
            "user_id": user_id,
            "prompt": prompt,
            'prompt_hash': hashlib.sha256(prompt.encode()).hexdigest(),
            "response": response.text,
            "latency_seconds": round(duration, 2),
            'model': "gemini-2.5-flash",
            "tokens_in_use": tokens_in_use
        })

        return {
            "user_id": user_id,
            "response": response.text,
            "latency_seconds": round(duration, 2),
            "tokens_in_use": tokens_in_use
        }
        
    except Exception as e:
        # It's better to raise an HTTPException in FastAPI for proper status codes
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    