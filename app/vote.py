from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,router


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session=Depends(db.get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    if vote.dir == 1:
        pass
    else:
        pass