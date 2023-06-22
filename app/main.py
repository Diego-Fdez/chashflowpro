from fastapi import FastAPI
from .users.routes import users_routes


# Create an instance of the FastAPI class
app = FastAPI(
    title="CashFlowPro API",
    description="CashFlowPro API documentation goes here",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# instantiate the router object
app.include_router(users_routes.router)


# Define the root route
@app.get("/")
def root():
    return {"Hello": "Welcome to my API"}