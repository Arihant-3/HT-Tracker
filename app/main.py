from fastapi import FastAPI
import uvicorn 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the example file of Habit-Time Tracker!"}


def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    

if __name__ == "__main__":
    main()
