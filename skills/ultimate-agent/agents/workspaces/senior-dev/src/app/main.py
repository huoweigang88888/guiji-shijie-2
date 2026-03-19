"""
主应用入口
"""
from fastapi import FastAPI

app = FastAPI(title="My Project", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/items")
async def get_items():
    return {"items": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
