from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schema.schema import reviewBase
from db.database import get_db
from model.models import DbReview
import time

router = APIRouter(
    prefix='/review',
    tags=['review']
)

async def time_consuming_functionality():
    time.sleep(5)
    return 'ok'

# Create Review
@router.post('/create', response_model=reviewBase)
def create_review(request: reviewBase, db: Session = Depends(get_db)):
    new_review = DbReview(
    rating = request.rating,
    item = request.item,
    comment =  request.comment,
    user = request.user,
    creator = request.creator,
    modified_date = request.modified_date,
    created_date = request.created_date,
    slug = request.slug
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Read All Reviews
@router.get('/', response_model=List[reviewBase])
async def get_all_reviews(db: Session = Depends(get_db)):
    await time_consuming_functionality()
    return db.query(DbReview).all()

# Read One Review
@router.get('/{id}', response_model=reviewBase)
def get_review(id: str, db: Session = Depends(get_db)):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Review with id {id} not found')
    return review

# Update Review
@router.patch('/{id}/update')
def update_review(id: str, request: reviewBase, db: Session = Depends(get_db)):
    review = db.query(DbReview).filter(DbReview.id == id)
    review.update({
        DbReview.rating: request.rating,
        DbReview.item: request.item,
        DbReview.comment: request.comment,
        DbReview.user: request.user,
        DbReview.creator: request.creator,
        DbReview.modified_date: request.modified_date,
        DbReview.created_date: request.created_date,
        DbReview.slug: request.slug    
    })
    db.commit()
    if not review.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Review with id {id} not found')
    return review(id, request, db)

# Delete Review
@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Review with id {id} not found')
    db.delete(review)
    db.commit()
    return review(id, db)