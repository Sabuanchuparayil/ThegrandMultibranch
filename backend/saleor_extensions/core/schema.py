"""
Core GraphQL schema extensions for authentication and common operations
"""
import graphene
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

User = get_user_model()

# Try to import Saleor's types
try:
    from saleor.graphql.core.mutations import BaseMutation
    from saleor.graphql.core.types import Error
    _SALEOR_AVAILABLE = True
except ImportError:
    # Fallback if Saleor types not available
    class Error(graphene.ObjectType):
        field = graphene.String()
        message = graphene.String()
    
    class BaseMutation(graphene.Mutation):
        class Meta:
            abstract = True
        
        @classmethod
        def perform_mutation(cls, root, info, **kwargs):
            raise NotImplementedError
    _SALEOR_AVAILABLE = False


class LoginInput(graphene.InputObjectType):
    """Input for login mutation"""
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UserType(graphene.ObjectType):
    """User type for GraphQL"""
    id = graphene.ID()
    email = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    isStaff = graphene.Boolean()
    isActive = graphene.Boolean()
    
    def resolve_id(self, info):
        return self.id
    
    def resolve_email(self, info):
        return self.email
    
    def resolve_firstName(self, info):
        return getattr(self, 'first_name', '') or getattr(self, 'firstName', '')
    
    def resolve_lastName(self, info):
        return getattr(self, 'last_name', '') or getattr(self, 'lastName', '')
    
    def resolve_isStaff(self, info):
        return getattr(self, 'is_staff', False)
    
    def resolve_isActive(self, info):
        return getattr(self, 'is_active', False)


class LoginPayload(graphene.ObjectType):
    """Response payload for login mutation"""
    token = graphene.String()
    user = graphene.Field(UserType)
    errors = graphene.List(Error)


class Login(BaseMutation):
    """Login mutation to authenticate user and get token"""
    
    class Meta:
        description = "Authenticate user and get authentication token"
        error_type_class = Error
    
    token = graphene.String()
    user = graphene.Field(UserType)
    errors = graphene.List(Error)
    
    class Arguments:
        input = LoginInput(required=True)
    
    @classmethod
    def perform_mutation(cls, root, info, input):
        """Authenticate user and generate token"""
        email = input.email
        password = input.password
        
        # Authenticate user - Saleor uses email as username
        # Try email first, then fallback to username field
        user = authenticate(username=email, password=password)
        
        # If authentication fails, try to find user by email and authenticate
        if not user:
            try:
                user_obj = User.objects.get(email=email)
                # Verify password manually
                if user_obj.check_password(password):
                    user = user_obj
            except User.DoesNotExist:
                pass
        
        if not user:
            return Login(
                token=None,
                user=None,
                errors=[Error(field='__all__', message='Invalid email or password')]
            )
        
        if not user.is_active:
            return Login(
                token=None,
                user=None,
                errors=[Error(field='__all__', message='User account is disabled')]
            )
        
        # Generate token
        token = cls.generate_token(user)
        
        if not token:
            return Login(
                token=None,
                user=None,
                errors=[Error(field='__all__', message='Failed to generate authentication token')]
            )
        
        return Login(
            token=token,
            user=user,
            errors=None
        )
    
    @staticmethod
    def generate_token(user):
        """Generate authentication token for user"""
        try:
            from rest_framework.authtoken.models import Token
            token, _ = Token.objects.get_or_create(user=user)
            return token.key
        except ImportError:
            # Try Saleor's ServiceAccount
            try:
                from saleor.account.models import ServiceAccount
                service_account, _ = ServiceAccount.objects.get_or_create(
                    name=f"Admin Dashboard - {user.email}",
                    user=user,
                )
                return service_account.auth_token
            except Exception:
                return None


class CoreMutations(graphene.ObjectType):
    """Core mutations including authentication"""
    login = Login.Field()

