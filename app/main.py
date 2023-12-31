from fastapi import FastAPI
from .users.routes import users_routes
from app.auth.routes import auth_routes
from app.categories.routes import categories_routes
from app.clients.routes import clients_routes
from app.products.routes import products_routes


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
app.include_router(auth_routes.router)
app.include_router(categories_routes.router)
app.include_router(clients_routes.router)
app.include_router(products_routes.router)


# Define the root route
@app.get("/")
def root():
    return {"Hello": "Welcome to my API"}