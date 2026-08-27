from sqlalchemy.orm import Session
from app.services.blog_service import BlogService
from app.schemas.blog import BlogIn


class BlogController:

    @staticmethod
    def get_all_blogs(
        db: Session,
        client_id: int | None = None,
        author_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return BlogService.getBlogs(
            db=db,
            client_id=client_id,
            author_id=author_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_blog_by_id(db: Session, blog_id: int):
        return BlogService.getBlogById(db, blog_id)

    @staticmethod
    def get_blog_by_slug(db: Session, slug: str):
        return BlogService.getBlogBySlug(db, slug)

    @staticmethod
    def create_blog(db: Session, request: BlogIn, current_user_id: int | None = None):
        return BlogService.createBlog(db, request, current_user_id=current_user_id)

    @staticmethod
    def update_blog(db: Session, blog_id: int, request: BlogIn):
        return BlogService.updateBlog(db, blog_id, request)

    @staticmethod
    def delete_blog(db: Session, blog_id: int):
        return BlogService.deleteBlog(db, blog_id)
