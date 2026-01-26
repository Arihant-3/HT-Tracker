from fastapi import FastAPI
import uvicorn 

# For templates and forms
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="app/templates")

# Create a FastAPI Instance
app = FastAPI()


from fastapi.staticfiles import StaticFiles
# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")



# Root route redirects to /habits
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/habits")


from app.routes.habit import router as habit_router
app.include_router(habit_router)


from app.routes.habitlog import router as habitlog_router
app.include_router(habitlog_router)




# Run the FastAPI server
def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    
if __name__ == "__main__":
    main()
