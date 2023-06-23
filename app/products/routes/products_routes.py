from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session, aliased
import uuid
from sqlalchemy import func, or_
from typing import Optional
from app.products.models.products_models import Product_Create, Product_Update, Product_Model
from app.database.database import get_db
from app.schemas import schemas
from app.middlewares import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}}
)

# define a route to create a new product
@router.post("/", response_description="Create a new product", response_model=Product_Model,
              status_code=status.HTTP_201_CREATED)
def create_product(product: Product_Create, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    # create a new product
    new_product = schemas.Product_Schema(user_id = current_user.id, **product.dict())
    # add the new product to the database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # return the new product
    return new_product


# define a route and function to get all products by user
@router.get("/", response_description="Get all products by user", response_model=list[Product_Model],
            status_code=status.HTTP_200_OK)
async def get_all_products_by_user(db: Session = Depends(get_db), 
                                    current_user: int = Depends(oauth2.get_current_user),
                                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Create an alias for the table Product_Schema
    Product = aliased(schemas.Product_Schema)

    # Query using the pg_trgm extension and the ts_rank function
    query = db.query(Product).filter(Product.user_id == current_user.id)

    if search:
        # Apply matching and ranking using ts_rank and ilike
        query = query.filter(or_(Product.product_name.ilike(f"%{search}%"), 
                                  func.ts_rank(func.to_tsvector(Product.product_name), func.to_tsquery(search)).isnot(None)))

    # Apply order, limit, and offset
    query = query.order_by(func.ts_rank(func.to_tsvector(Product.product_name), func.to_tsquery(search)).desc(), Product.product_name)
    query = query.limit(limit).offset(skip)

    # Run the query and get the results
    find_product = query.all()
    
    # If no products are found
    if not find_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Products not found")
    
    # Return the products found
    return find_product


# define a route and function to get a product by id
@router.get("/{product_id}", response_description="Get a product by id", response_model=Product_Model,
            status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: uuid.UUID, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    # Query the database for the product with the given id
    find_product = db.query(schemas.Product_Schema).filter(schemas.Product_Schema.id == product_id).first()

    # If no product is found
    if not find_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Product with id: {product_id} not found")
    
    # If the product is not owned by the current user
    if find_product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Only the user can access this action")
    
    # Return the product found
    return find_product
















