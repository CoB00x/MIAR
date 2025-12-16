from fastapi import FastAPI
from .database import engine, Base
from .routers import router as amenity_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Amenity Service",
    description="Microservice for managing additional hotel services",
    version="1.0.0"
)

# Include routers
app.include_router(amenity_router)

@app.get("/")
def read_root():
    return {"message": "Amenity Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)