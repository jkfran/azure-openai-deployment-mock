import json
import asyncio
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

# Mock API Key for validation
VALID_API_KEY = "MOCK-AZURE-OPENAI-API-KEY-1234567890"

# Middleware to check the API key
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("api-key")
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return await call_next(request)


# Mock non-streaming response
async def mock_non_streaming_response():
    return {
        "id": "chatcmpl-xyz",
        "object": "chat.completion",
        "created": 1694200000,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response for non-streaming completion."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}
    }



# Mock streaming response generator (simulates tokens streaming one by one)
async def mock_streaming_response():
    long_text = (
        "This is a super long mock streaming response. "
        "It will keep streaming in small chunks to simulate a large amount of tokens. "
        "Each chunk will be sent with a small delay to emulate the real streaming behavior "
        "of the model. You can imagine this going on for a very long time, sending token "
        "after token, chunk after chunk, until the entire response is completed. "
        "For the purpose of this mock, we are repeating a small text many times to simulate "
        "a much larger response. "
    )

    # Break the long text into small chunks
    chunk_size = 7  # Number of characters per chunk
    chunks = [long_text[i:i + chunk_size] for i in range(0, len(long_text), chunk_size)]

    for chunk in chunks:
        yield f"data: {json.dumps({'choices': [{'delta': {'content': chunk}}]})}\n\n"
        await asyncio.sleep(0.3)  # Short delay between chunks to simulate streaming

    yield "data: [DONE]\n\n"  # End of the stream


# Main endpoint to handle both streaming and non-streaming completions
@app.post("/openai/deployments/{model_name}/chat/completions")
async def chat_completion(request: Request, model_name: str, api_key: str = Header(...)):
    # Read the raw request body without parsing it
    request_body = await request.body()
    print(f"Received payload: {request_body}")

    # Simulate ignoring the payload and responding based on the 'stream' flag
    is_streaming = False  # Default to non-streaming
    try:
        request_data = json.loads(request_body)
        is_streaming = request_data.get("stream", False)
    except Exception as e:
        # If the request body can't be parsed as JSON, just ignore it
        print(f"Error parsing JSON: {e}")

    if is_streaming:
        # Return a streaming response if "stream": true
        return StreamingResponse(mock_streaming_response(), media_type="text/event-stream")
    else:
        # Return a standard JSON response
        return JSONResponse(await mock_non_streaming_response())
