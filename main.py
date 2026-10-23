from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine, Base,SessionLocal
import models , schema


Base.metadata.create_all(bind=engine)
app=FastAPI()
# database dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get('/')
def home():
    return{
        'message':'blog api started'
    }
# create blog
@app.post('/blogs',response_model=schema.BlogResponse)
def create_blog(blog:schema.BlogCreate,db:Session=Depends(get_db)):
 new_blog=models.Blog(
    title=blog.title,
    content=blog.content

)
 db.add(new_blog)
 db.commit()
 db.refresh(new_blog)
 return new_blog
# read all blogs
@app.get('/blogs', response_model=list[schema.BlogResponse])
def get_blogs(db:Session=Depends(get_db)):
   return db.query(models.Blog).all()
# read only one blog
@app.get('/blogs/{id}', response_model=schema.BlogResponse)
def get_blog(id:int,db:Session=Depends(get_db)):
   blog=db.query(models.Blog).filter(models.Blog.id==id).first()
   if not blog: 
      raise HTTPException(status_code=401, detail='blog not found')
   return blog
# update blog API
@app.put('/blogs/{id}',response_model=schema.BlogResponse)
def update_blog(id:int,blog:schema.BlogCreate,db:Session=Depends(get_db)):
   existing_blog=db.query(models.Blog).filter(models.Blog.id==id).first()
   if not existing_blog:
      raise HTTPException(status_code=401,detail="blog not existing")
   existing_blog.title=blog.title
   existing_blog.content=blog.content
   db.commit()
   return existing_blog
# delete blog API
@app.delete('/blogs/{id}')
def delete_blog(id:int,db:Session=Depends(get_db)):
   blog=db.query(models.Blog).filter(models.Blog.id==id)
   if not blog.first():
      raise HTTPException(status_code=401, detail='blog not found')
   blog.delete()
   db.commit()
   return{
      'message':'blog deleted successfully.....'
   }


   