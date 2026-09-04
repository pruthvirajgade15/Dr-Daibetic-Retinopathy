from typing import Generator
from sqlalchemy.orm import Session
from ..database.database import get_db

# Dependency alias
get_database_session = get_db
