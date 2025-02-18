from sqlalchemy.orm import Session
from models.category import CategoryModel
from schemas.category import CategoryRequest
from core.websocket import broadcast_message


# **Create a new category**
def create_category(db: Session, request: CategoryRequest):
    """
    Creates a new category in the database.

    This function receives an SQLAlchemy Session and a CategoryRequest object,
    instantiates a new CategoryModel from the provided data, and inserts it into
    the database. The database session is then committed to persist the new record.
    Finally, the new_category object is refreshed to include any database-generated
    values (e.g., auto-incremented IDs).

    :param db: The SQLAlchemy session used for database interactions.
    :type db: Session

    :param category: Data required to create a new category, including fields like
                     'name' and 'description'.
    :type category: CategoryRequest

    :return: The newly created CategoryModel instance, populated with all fields
             (including database-generated values).
    :rtype: CategoryModel

    :raises SQLAlchemyError: If there is an error during the commit operation.
    """
    category = CategoryModel(
        name=request.name,
        description=request.description,
    )

    db.add(category)  # Add new category to the database
    db.commit()  # Commit the transaction
    db.refresh(
        category
    )  # Refresh the category object ( güncellenmiş nesneyi teslim eder)
    broadcast_message(f"Yeni Kategori Eklendi: {category.name}")
    return category


# **Get all categories**
def get_categories(db: Session):
    """
    Retrieves all categories from the database.
    """
    return db.query(CategoryModel).all()


# **Get category by id**
def get_category(db: Session, category_id: int):
    """
    Retrieves a single category by its ID.
    """
    return _get_category_by_id(db, category_id)


# **Update category**
def update_category(
    db: Session,
    category_id: int,
    request: CategoryRequest,
):
    """
    Update current category in the database.
    """
    category = _get_category_by_id(db, category_id)
    old_category_name = category.name
    if not category:
        return None

    category.name = request.name
    category.description = request.description
    db.commit()
    # broadcast_message(f"{old_category_name} Kategori Düzenlendi: {category.name}")
    return category


# **Delete category**
def delete_category(db: Session, category_id: int):
    category = _get_category_by_id(db, category_id)

    if not category:
        return None

    db.delete(category)
    db.commit()
    broadcast_message(f"Kategori Silindi: {category.name}")
    return category


def _get_category_by_id(db: Session, category_id: int) -> CategoryModel:  # private
    return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()


# private CategoryModel GetCategoryById( int category_id) => _categoryRepository.GetCategoryById(category_id);
