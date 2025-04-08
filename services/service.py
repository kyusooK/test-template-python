forEach: Aggregate
fileName: {{nameCamelCase}}_service.py
path: {{boundedContext.name}}/services
---
from sqlalchemy.orm import Session
from repositories.{{nameCamelCase}}_repository import {{namePascalCase}}Repository
from models.{{nameCamelCase}} import {{namePascalCase}}
from typing import List, Optional, Dict
import hashlib
import os

class {{namePascalCase}}Service:
    def __init__(self, db: Session):
        self.{{nameCamelCase}}_repository = {{namePascalCase}}Repository(db)
    
    {{#checkPassword}}
    def _hash_password(self, password: str) -> str:
        """Hash a password for storage"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return salt.hex() + key.hex()
    
    {{/checkPassword}}
    def get_{{namePlural}}(self, skip: int = 0, limit: int = 100) -> List[{{namePascalCase}}]:
        """Get all {{namePlural}} with pagination"""
        return self.{{nameCamelCase}}_repository.get_all(skip, limit)
    
    def get_{{nameCamelCase}}(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}) -> Optional[{{namePascalCase}}]:
        """Get a {{nameCamelCase}} by ID"""
        return self.{{nameCamelCase}}_repository.get_by_id({{aggregateRoot.keyFieldDescriptor.nameCamelCase}})
    
    {{#aggregateRoot.fieldDescriptors}}
    {{#if isSearchKey}}
    def get_{{../nameCamelCase}}_by_{{nameCamelCase}}(self, {{nameCamelCase}}: {{className}}) -> Optional[{{../namePascalCase}}]:
        """Get a {{../nameCamelCase}} by {{nameCamelCase}}"""
        return self.{{../nameCamelCase}}_repository.get_by_{{nameCamelCase}}({{nameCamelCase}})
    
    {{/if}}
    {{/aggregateRoot.fieldDescriptors}}
    def create_{{nameCamelCase}}(self, {{#aggregateRoot.fieldDescriptors}}{{#unless isKey}}{{nameCamelCase}}: {{#if isVO}}str{{else}}{{className}}{{/if}}{{#if isName}} = None{{/if}}{{#unless @last}}, {{/unless}}{{/unless}}{{/aggregateRoot.fieldDescriptors}}) -> Optional[{{namePascalCase}}]:
        """Create a new {{nameCamelCase}}"""
        {{#aggregateRoot.fieldDescriptors}}
        {{#if isSearchKey}}
        # Check if {{nameCamelCase}} already exists
        if self.{{../nameCamelCase}}_repository.get_by_{{nameCamelCase}}({{nameCamelCase}}):
            raise ValueError("{{namePascalCase}} already exists")
        
        {{/if}}
        {{/aggregateRoot.fieldDescriptors}}
        {{#checkPassword}}
        # Hash the password
        hashed_password = self._hash_password(password)
        
        {{/checkPassword}}
        # Create the {{nameCamelCase}}
        return self.{{nameCamelCase}}_repository.create(
            {{#aggregateRoot.fieldDescriptors}}
            {{#unless isKey}}
            {{nameCamelCase}}={{#if isPassword}}hashed_password{{else}}{{nameCamelCase}}{{/if}}{{#unless @last}},{{/unless}}
            {{/unless}}
            {{/aggregateRoot.fieldDescriptors}}
        )
    
    def update_{{nameCamelCase}}(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}, data: Dict) -> Optional[{{namePascalCase}}]:
        """Update a {{nameCamelCase}}'s details"""
        {{#checkPassword}}
        # Don't allow password update through this method
        if 'password' in data:
            del data['password']
        {{/checkPassword}}
            
        return self.{{nameCamelCase}}_repository.update({{aggregateRoot.keyFieldDescriptor.nameCamelCase}}, **data)
    
    {{#checkPassword}}
    def change_password(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}, new_password: str) -> Optional[{{namePascalCase}}]:
        """Change a {{nameCamelCase}}'s password"""
        hashed_password = self._hash_password(new_password)
        return self.{{nameCamelCase}}_repository.update({{aggregateRoot.keyFieldDescriptor.nameCamelCase}}, hashed_password=hashed_password)
    {{/checkPassword}}
    
    def delete_{{nameCamelCase}}(self, {{aggregateRoot.keyFieldDescriptor.nameCamelCase}}: {{aggregateRoot.keyFieldDescriptor.className}}) -> bool:
        """Delete a {{nameCamelCase}} by ID"""
        return self.{{nameCamelCase}}_repository.delete({{aggregateRoot.keyFieldDescriptor.nameCamelCase}})

<function>
window.$HandleBars.registerHelper('checkPassword', function(options) {
    for(var i = 0; i < this.aggregateRoot.fieldDescriptors.length; i++) {
        if(this.aggregateRoot.fieldDescriptors[i].name.toLowerCase().includes('password')) {
            return options.fn(this);
        }
    }
    return options.inverse(this);
});
</function> 