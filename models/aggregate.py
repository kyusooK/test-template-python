forEach: Aggregate
fileName: {{nameCamelCase}}.py
path: {{boundedContext.name}}/models
---
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .base import Base

class {{namePascalCase}}(Base):
    __tablename__ = "{{namePlural}}"
    
    {{#aggregateRoot.fieldDescriptors}}
    {{#if isKey}}
    {{nameCamelCase}} = Column({{className}}, primary_key=True, index=True)
    {{else}}
    {{nameCamelCase}} = Column({{className}}{{#if isLob}}(1000){{else}}{{#if isName}}(100){{else}}{{#if isVO}}(100){{/if}}{{/if}}{{/if}}, nullable={{#if isName}}False{{else}}True{{/if}}{{#if isSearchKey}}, index=True{{/if}})
    {{/if}}
    {{/aggregateRoot.fieldDescriptors}}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<{{namePascalCase}}({{#aggregateRoot.fieldDescriptors}}{{#if isKey}}{{nameCamelCase}}={{#createLeftMustache}}{{/createLeftMustache}}self.{{nameCamelCase}}{{#createRightMustache}}{{/createRightMustache}}{{/if}}{{/aggregateRoot.fieldDescriptors}})>"

<function>
window.$HandleBars.registerHelper('isLong', function (className) {
    return (className === 'Long' || className === 'Integer' || className === 'int');
});
window.$HandleBars.registerHelper('createLeftMustache', function () {
    // Handlebars에서 f-string의 중괄호를 이스케이프하기 위한 헬퍼 함수
    return '{'
});
window.$HandleBars.registerHelper('createRightMustache', function () {
    // Handlebars에서 f-string의 중괄호를 이스케이프하기 위한 헬퍼 함수
    return '{'
});
</function> 