forEach: BoundedContext
fileName: main.py
path: {{name}}/app
---
import os
from sqlalchemy.orm import Session
from config.database import SessionLocal
{{#aggregates}}
from services.{{nameCamelCase}}_service import {{namePascalCase}}Service
{{/aggregates}}
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db():
    """Creates a new database session for each request"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

{{#aggregates}}
def create_sample_{{nameCamelCase}}(db: Session, {{#aggregateRoot.fieldDescriptors}}{{#unless isKey}}{{nameCamelCase}}: {{className}}{{#unless @last}}, {{/unless}}{{/unless}}{{/aggregateRoot.fieldDescriptors}}):
    """Create a sample {{nameCamelCase}} for demonstration"""
    {{nameCamelCase}}_service = {{namePascalCase}}Service(db)
    
    try:
        {{nameCamelCase}} = {{nameCamelCase}}_service.create_{{nameCamelCase}}(
            {{#aggregateRoot.fieldDescriptors}}
            {{#unless isKey}}
            {{nameCamelCase}}={{nameCamelCase}}{{#unless @last}},{{/unless}}
            {{/unless}}
            {{/aggregateRoot.fieldDescriptors}}
        )
        print(f"Created {{nameCamelCase}}: {{{nameCamelCase}}}")
        return {{nameCamelCase}}
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None

def list_{{namePlural}}(db: Session):
    """List all {{namePlural}} in the database"""
    {{nameCamelCase}}_service = {{namePascalCase}}Service(db)
    {{namePlural}} = {{nameCamelCase}}_service.get_{{namePlural}}()
    
    if not {{namePlural}}:
        print("No {{namePlural}} found in the database.")
        return
    
    print("\n{{namePascalCase}} in the database:")
    for {{nameCamelCase}} in {{namePlural}}:
        print(f"{{#aggregateRoot.fieldDescriptors}}{{#if isKey}}{{namePascalCase}}: {{../nameCamelCase}}.{{nameCamelCase}}{{/if}}{{/aggregateRoot.fieldDescriptors}}{{#getDisplayFields aggregateRoot.fieldDescriptors}}, {{namePascalCase}}: {{{../nameCamelCase}}.{{nameCamelCase}}}{{/getDisplayFields}}")
{{/aggregates}}

def main():
    """Main application entry point"""
    print("{{namePascalCase}} Sample Application")
    print("==================================")
    
    # Get database session
    db = get_db()
    
    # Example operations
{{#aggregates}}
    print("\nCreating sample {{namePlural}}...")
    # TODO: Add your sample data here
    
    # List all {{namePlural}}
    list_{{namePlural}}(db)
{{/aggregates}}
    
    print("\nApplication completed.")

if __name__ == "__main__":
    main()

<function>
window.$HandleBars.registerHelper('getDisplayFields', function(fieldDescriptors, options) {
    var result = '';
    for(var i = 0; i < fieldDescriptors.length; i++) {
        if(!fieldDescriptors[i].isKey && (fieldDescriptors[i].isName || fieldDescriptors[i].isSearchKey)) {
            result += options.fn(fieldDescriptors[i]);
        }
    }
    return result;
});
</function> 