import re
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.blog import Blog
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog import BlogIn


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


class BlogService:

    @staticmethod
    def getBlogs(
        db: Session,
        client_id: int | None = None,
        author_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, blogs = BlogRepository.get_all_blogs(
            db=db,
            client_id=client_id,
            author_id=author_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "blogs": blogs
        }

    @staticmethod
    def getBlogById(db: Session, blog_id: int):
        blog = BlogRepository.get_by_id(db, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog

    @staticmethod
    def getBlogBySlug(db: Session, slug: str):
        blog = BlogRepository.get_by_slug(db, slug)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog

    @staticmethod
    def createBlog(db: Session, request: BlogIn, current_user_id: int | None = None):
        blog_data = request.model_dump(exclude_unset=True)

        # Set author_id from current user if not provided in payload
        if not blog_data.get("author_id") and current_user_id:
            blog_data["author_id"] = current_user_id

        # Generate slug from title if not supplied
        slug = blog_data.get("slug")
        if not slug and blog_data.get("title"):
            slug = slugify(blog_data["title"])
            blog_data["slug"] = slug

        if not slug:
            raise HTTPException(status_code=400, detail="Blog slug or title is required")

        if BlogRepository.get_by_slug(db, slug):
            raise HTTPException(status_code=400, detail="Blog slug already exists")

        blog = Blog(**blog_data)
        return BlogRepository.create(db, blog)

    @staticmethod
    def updateBlog(db: Session, blog_id: int, request: BlogIn):
        blog = BlogRepository.get_by_id(db, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        update_data = request.model_dump(exclude_unset=True)

        if "slug" in update_data and update_data["slug"] and update_data["slug"] != blog.slug:
            existing = BlogRepository.get_by_slug(db, update_data["slug"])
            if existing and existing.id != blog_id:
                raise HTTPException(status_code=400, detail="Blog slug already in use")

        return BlogRepository.update(db, blog, update_data)

    @staticmethod
    def deleteBlog(db: Session, blog_id: int):
        blog = BlogRepository.get_by_id(db, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        BlogRepository.delete(db, blog)
        return {"message": "Blog deleted successfully"}
