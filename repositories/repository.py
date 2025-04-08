forEach: Aggregate
fileName: {{nameCamelCase}}_repository.py
path: {{boundedContext.name}}/repositories
---
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.{{nameCamelCase}} import {{namePascalCase}}
from typing import List, Optional

class {{namePascalCase}}Repository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[{{namePascalCase}}]:
        """Get all {{namePlural}} with pagination"""
        return self.db.query({{namePascalCase}}).offset(skip).limit(limit).all()
    
    def get_by_id(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}) -> Optional[{{namePascalCase}}]:
        """Get a {{nameCamelCase}} by ID"""
        return self.db.query({{namePascalCase}}).filter({{namePascalCase}}.{{aggregateRoot.keyFieldDescriptor.nameCamelCase}} == {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}).first()
    
    {{#aggregateRoot.fieldDescriptors}}
    {{#if isSearchKey}}
    def get_by_{{nameCamelCase}}(self, {{nameCamelCase}}: {{className}}) -> Optional[{{../namePascalCase}}]:
        """Get a {{../nameCamelCase}} by {{nameCamelCase}}"""
        return self.db.query({{../namePascalCase}}).filter({{../namePascalCase}}.{{nameCamelCase}} == {{nameCamelCase}}).first()
    
    {{/if}}
    {{/aggregateRoot.fieldDescriptors}}
    def create(self, {{#aggregateRoot.fieldDescriptors}}{{#unless isKey}}{{nameCamelCase}}: {{#if isVO}}str{{else}}{{className}}{{/if}}{{#unless @last}}, {{/unless}}{{/unless}}{{/aggregateRoot.fieldDescriptors}}) -> Optional[{{namePascalCase}}]:
        """Create a new {{nameCamelCase}}"""
        {{nameCamelCase}} = {{namePascalCase}}(
            {{#aggregateRoot.fieldDescriptors}}
            {{#unless isKey}}
            {{nameCamelCase}}={{nameCamelCase}}{{#unless @last}},{{/unless}}
            {{/unless}}
            {{/aggregateRoot.fieldDescriptors}}
        )
        
        try:
            self.db.add({{nameCamelCase}})
            self.db.commit()
            self.db.refresh({{nameCamelCase}})
            return {{nameCamelCase}}
        except IntegrityError:
            self.db.rollback()
            return None
    
    def update(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}, **kwargs) -> Optional[{{namePascalCase}}]:
        """Update a {{nameCamelCase}}'s details"""
        {{nameCamelCase}} = self.get_by_id({{aggregateRoot.keyFieldDescriptor.nameCamelCase}})
        if not {{nameCamelCase}}:
            return None
            
        for key, value in kwargs.items():
            if hasattr({{nameCamelCase}}, key) and value is not None:
                setattr({{nameCamelCase}}, key, value)
        
        self.db.commit()
        self.db.refresh({{nameCamelCase}})
        return {{nameCamelCase}}
    
    def delete(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}) -> bool:
        """Delete a {{nameCamelCase}} by ID"""
        {{nameCamelCase}} = self.get_by_id({{aggregateRoot.keyFieldDescriptor.nameCamelCase}})
        if not {{nameCamelCase}}:
            return False
            
        self.db.delete({{nameCamelCase}})
        self.db.commit()
        return True 