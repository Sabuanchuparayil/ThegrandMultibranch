"""
GraphQL Middleware to log schema usage
This helps verify that our extended schema is being used
"""
import json
from django.utils.deprecation import MiddlewareMixin


class GraphQLSchemaLoggingMiddleware(MiddlewareMixin):
    """Middleware to log GraphQL requests and schema usage"""
    
    def process_request(self, request):
        """Log GraphQL requests"""
        if request.path == '/graphql/' or request.path.endswith('/graphql/'):
            print(f"🔍 GraphQL request received: {request.method} {request.path}")
            if request.method == 'POST':
                try:
                    body = json.loads(request.body.decode('utf-8'))
                    query = body.get('query', '')
                    if query:
                        # Log first 200 chars of query
                        query_preview = query[:200].replace('\n', ' ')
                        print(f"🔍 GraphQL query preview: {query_preview}...")
                        # Check if query includes branches
                        if 'branches' in query.lower():
                            print("✅ GraphQL query includes 'branches' field")
                except:
                    pass
        return None
    
    def process_response(self, request, response):
        """Log GraphQL responses"""
        if request.path == '/graphql/' or request.path.endswith('/graphql/'):
            print(f"🔍 GraphQL response: {response.status_code}")
            if response.status_code == 400:
                try:
                    # Try to get response content
                    if hasattr(response, 'content'):
                        content = response.content.decode('utf-8')[:500]
                        print(f"🔍 GraphQL error response: {content}")
                except:
                    pass
        return response

