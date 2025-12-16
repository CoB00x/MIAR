from fastapi import FastAPI
from .database import engine, Base
from .routers import router as restaurant_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Service",
    description="Microservice for managing restaurant operations in hotel",
    version="1.0.0"
)

# Include routers
app.include_router(restaurant_router)

@app.get("/")
def read_root():
    return {"message": "Restaurant Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)