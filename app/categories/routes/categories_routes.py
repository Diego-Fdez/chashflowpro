from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
import uuid
from app.categories.models.category_models import Category_Create, Category_Model
from app.database.database import get_db
from app.schemas import schemas
from app.middlewares import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"],
    responses={404: {"description": "Not found"}}
)

# define a route and function to create a new category
@router.post("/", response_description="Create a new category",  response_model=Category_Model,
              status_code=status.HTTP_201_CREATED)
def create_category(category: Category_Create, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    #find the user with the id
    user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == current_user.id).first()
    
    #if the user is not found, raise an exception
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {current_user.id} does not exist")
    
    #if the user is not a superuser, raise an exception
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only superusers can perform this action")
    
    #create a new category
    new_category = schemas.Category_Schema(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# define route and function to get all categories
@router.get("/", response_description="Get all categories", response_model=list[Category_Model], 
            status_code=status.HTTP_200_OK)
async def get_all_categories(db: Session = Depends(get_db), is_auth: int = Depends(oauth2.get_current_user)):
    categories = db.query(schemas.Category_Schema).all()

    #if the categories are not found, raise an exception
    if categories == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No categories found")
    
    return categories


# define route and function to get a single category by category_id
@router.get("/{id}", response_description="Get a single category by id", response_model=Category_Model,
            status_code=status.HTTP_200_OK)
async def get_category_by_id(id: uuid.UUID, db: Session = Depends(get_db), is_auth: int = Depends(oauth2.get_current_user)):
    found_category = db.query(schemas.Category_Schema).filter(schemas.Category_Schema.id == id).first()

    #if the category is not found, raise an exception
    if not found_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")
    
    return found_category


# define route and function to update a single category by category_id

@router.patch("/{id}", response_description="Update a single category by id", response_model=Category_Model,
            status_code=status.HTTP_200_OK)
async def update_category_by_id(id: uuid.UUID, category: Category_Create, db: Session = Depends(get_db),
                                current_user: int = Depends(oauth2.get_current_user)):
    found_user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == current_user.id).first()

    # if the user is not found, raise an exception
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {current_user.id} does not exist")
    
    # if the user is not a superuser, raise an exception
    if not found_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only superusers can perform this action")
    
    #find the category with the id
    found_category = db.query(schemas.Category_Schema).filter(schemas.Category_Schema.id == id)
    category_exist = found_category.first()

    #if the category is not found, raise an exception
    if not category_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")
    
    #update the category
    found_category.update(category.dict(), synchronize_session=False)
    db.commit()

    return found_category.first()


# define route and function to delete a single category by category_id
@router.delete("/{id}", response_description="Delete a single category by id", 
                status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_by_id(id: uuid.UUID, db: Session = Depends(get_db),
                                current_user: int = Depends(oauth2.get_current_user)):
    # find the user with the id
    found_user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == current_user.id).first()

    # if the user is not found, raise an exception
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {current_user.id} does not exist")
    
    # if the user is not a superuser, raise an exception
    if not found_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only superusers can perform this action")
    
    found_category = db.query(schemas.Category_Schema).filter(schemas.Category_Schema.id == id)
    category_exist = found_category.first()

    #if the category is not found, raise an exception
    if not category_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")
    
    #delete the category
    found_category.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)