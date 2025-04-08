forEach: BoundedContext
fileName: base.py
path: {{name}}/models
---
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for SQLAlchemy models
Base = declarative_base() 