forEach: Aggregate
fileName: test_{{nameCamelCase}}.py
path: {{boundedContext.name}}/tests
---
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from models.{{nameCamelCase}} import {{namePascalCase}}
from services.{{nameCamelCase}}_service import {{namePascalCase}}Service
from repositories.{{nameCamelCase}}_repository import {{namePascalCase}}Repository

class Test{{namePascalCase}}Service(unittest.TestCase):
    def setUp(self):
        # Mock database session
        self.db = MagicMock(spec=Session)
        
        # Create a mock {{nameCamelCase}} repository
        self.{{nameCamelCase}}_repository = MagicMock(spec={{namePascalCase}}Repository)
        
        # Create the {{nameCamelCase}} service with mocked repository
        with patch('services.{{nameCamelCase}}_service.{{namePascalCase}}Repository', return_value=self.{{nameCamelCase}}_repository):
            self.{{nameCamelCase}}_service = {{namePascalCase}}Service(self.db)
    
    def test_get_{{namePlural}}(self):
        # Mock data
        mock_{{namePlural}} = [
            {{namePascalCase}}({{#getMockAggregateData aggregateRoot.fieldDescriptors 1}}{{/getMockAggregateData}}),
            {{namePascalCase}}({{#getMockAggregateData aggregateRoot.fieldDescriptors 2}}{{/getMockAggregateData}})
        ]
        
        # Configure mock
        self.{{nameCamelCase}}_repository.get_all.return_value = mock_{{namePlural}}
        
        # Call the method
        result = self.{{nameCamelCase}}_service.get_{{namePlural}}()
        
        # Assertions
        self.{{nameCamelCase}}_repository.get_all.assert_called_once_with(0, 100)
        self.assertEqual(len(result), 2)
        {{#aggregateRoot.fieldDescriptors}}
        {{#if isKey}}
        self.assertEqual(result[0].{{nameCamelCase}}, {{#getMockValue className 1}}{{/getMockValue}})
        self.assertEqual(result[1].{{nameCamelCase}}, {{#getMockValue className 2}}{{/getMockValue}})
        {{/if}}
        {{/aggregateRoot.fieldDescriptors}}
    
    def test_get_{{nameCamelCase}}_by_id(self):
        # Mock data
        mock_{{nameCamelCase}} = {{namePascalCase}}({{#getMockAggregateData aggregateRoot.fieldDescriptors 1}}{{/getMockAggregateData}})
        
        # Configure mock
        self.{{nameCamelCase}}_repository.get_by_id.return_value = mock_{{nameCamelCase}}
        
        # Call the method
        result = self.{{nameCamelCase}}_service.get_{{nameCamelCase}}({{#aggregateRoot.fieldDescriptors}}{{#if isKey}}{{#getMockValue className 1}}{{/getMockValue}}{{/if}}{{/aggregateRoot.fieldDescriptors}})
        
        # Assertions
        self.{{nameCamelCase}}_repository.get_by_id.assert_called_once_with({{#aggregateRoot.fieldDescriptors}}{{#if isKey}}{{#getMockValue className 1}}{{/getMockValue}}{{/if}}{{/aggregateRoot.fieldDescriptors}})
        {{#aggregateRoot.fieldDescriptors}}
        {{#if isKey}}
        self.assertEqual(result.{{nameCamelCase}}, {{#getMockValue className 1}}{{/getMockValue}})
        {{/if}}
        {{/aggregateRoot.fieldDescriptors}}
    
    def test_create_{{nameCamelCase}}_success(self):
        # Mock data
        mock_{{nameCamelCase}} = {{namePascalCase}}({{#getMockAggregateData aggregateRoot.fieldDescriptors 1}}{{/getMockAggregateData}})
        
        # Configure mocks
        {{#aggregateRoot.fieldDescriptors}}
        {{#if isSearchKey}}
        self.{{../../nameCamelCase}}_repository.get_by_{{nameCamelCase}}.return_value = None
        {{/if}}
        {{/aggregateRoot.fieldDescriptors}}
        self.{{nameCamelCase}}_repository.create.return_value = mock_{{nameCamelCase}}
        
        {{#checkPassword}}
        # Mock password hashing
        with patch.object(self.{{nameCamelCase}}_service, '_hash_password', return_value="hashedpw"):
        {{/checkPassword}}
            # Call the method
            result = self.{{nameCamelCase}}_service.create_{{nameCamelCase}}(
                {{#aggregateRoot.fieldDescriptors}}
                {{#unless isKey}}
                {{nameCamelCase}}={{#getMockValue className 1}}{{/getMockValue}}{{#unless @last}},{{/unless}}
                {{/unless}}
                {{/aggregateRoot.fieldDescriptors}}
            )
        
        # Assertions
        {{#aggregateRoot.fieldDescriptors}}
        {{#if isSearchKey}}
        self.{{../../nameCamelCase}}_repository.get_by_{{nameCamelCase}}.assert_called_once_with({{#getMockValue className 1}}{{/getMockValue}})
        {{/if}}
        {{/aggregateRoot.fieldDescriptors}}
        self.{{nameCamelCase}}_repository.create.assert_called_once_with(
            {{#aggregateRoot.fieldDescriptors}}
            {{#unless isKey}}
            {{nameCamelCase}}={{#if isPassword}}{{#checkPassword}}"hashedpw"{{/checkPassword}}{{else}}{{#getMockValue className 1}}{{/getMockValue}}{{/if}}{{#unless @last}},{{/unless}}
            {{/unless}}
            {{/aggregateRoot.fieldDescriptors}}
        )
        {{#aggregateRoot.fieldDescriptors}}
        {{#if isKey}}
        self.assertEqual(result.{{nameCamelCase}}, {{#getMockValue className 1}}{{/getMockValue}})
        {{/if}}
        {{/aggregateRoot.fieldDescriptors}}
    
    {{#aggregateRoot.fieldDescriptors}}
    {{#if isSearchKey}}
    def test_create_{{../../nameCamelCase}}_{{nameCamelCase}}_exists(self):
        # Mock data
        existing_{{../../nameCamelCase}} = {{../../namePascalCase}}({{nameCamelCase}}={{#getMockValue className 1}}{{/getMockValue}})
        
        # Configure mocks
        self.{{../../nameCamelCase}}_repository.get_by_{{nameCamelCase}}.return_value = existing_{{../../nameCamelCase}}
        
        # Call the method and check for exception
        with self.assertRaises(ValueError) as context:
            self.{{../../nameCamelCase}}_service.create_{{../../nameCamelCase}}(
                {{#../../aggregateRoot.fieldDescriptors}}
                {{#unless isKey}}
                {{nameCamelCase}}={{#getMockValue className 1}}{{/getMockValue}}{{#unless @last}},{{/unless}}
                {{/unless}}
                {{/../../aggregateRoot.fieldDescriptors}}
            )
        
        # Assertions
        self.assertEqual(str(context.exception), "{{namePascalCase}} already exists")
        self.{{../../nameCamelCase}}_repository.get_by_{{nameCamelCase}}.assert_called_once_with({{#getMockValue className 1}}{{/getMockValue}})
        self.{{../../nameCamelCase}}_repository.create.assert_not_called()
    {{/if}}
    {{/aggregateRoot.fieldDescriptors}}

if __name__ == '__main__':
    unittest.main()

<function>
window.$HandleBars.registerHelper('getMockValue', function(className, id) {
    if (className === 'Long' || className === 'Integer' || className === 'int') {
        return id;
    } else if (className === 'String' || className === 'str') {
        return `"test${id}"`;
    } else if (className === 'Boolean' || className === 'bool') {
        return 'True';
    } else {
        return 'None';
    }
});

window.$HandleBars.registerHelper('getMockAggregateData', function(fieldDescriptors, id, options) {
    var result = '';
    for (var i = 0; i < fieldDescriptors.length; i++) {
        var field = fieldDescriptors[i];
        var mockValue;
        
        if (field.className === 'Long' || field.className === 'Integer' || field.className === 'int') {
            mockValue = id;
        } else if (field.className === 'String' || field.className === 'str') {
            mockValue = `"test${id}"`;
        } else if (field.className === 'Boolean' || field.className === 'bool') {
            mockValue = 'True';
        } else {
            mockValue = 'None';
        }
        
        result += field.nameCamelCase + '=' + mockValue;
        if (i < fieldDescriptors.length - 1) {
            result += ', ';
        }
    }
    return result;
});

window.$HandleBars.registerHelper('checkPassword', function(options) {
    for(var i = 0; i < this.aggregateRoot.fieldDescriptors.length; i++) {
        if(this.aggregateRoot.fieldDescriptors[i].name.toLowerCase().includes('password')) {
            return options.fn(this);
        }
    }
    return options.inverse(this);
});
</function> 