"""
GraphQL schema for branches
"""
import graphene
from django.core.exceptions import ValidationError

from saleor_extensions.branches.models import Branch
from saleor_extensions.regions.models import Region

# Try to import BaseMutation from Saleor, fallback to graphene.Mutation
try:
    from saleor.graphql.core.mutations import BaseMutation
    from saleor.graphql.core.types import Error
    _SALEOR_AVAILABLE = True
except ImportError:
    # Fallback if Saleor's BaseMutation is not available
    # Define Error class first so it can be used in BaseMutation
    # Use a graphene ObjectType with resolvers and direct attribute access
    class Error(graphene.ObjectType):
        field = graphene.String()
        message = graphene.String()
        
        def __init__(self, field=None, message=None):
            """Initialize Error - store values for both direct access and resolvers"""
            super().__init__()
            # Store values in instance dict to bypass descriptor and allow direct access
            object.__setattr__(self, 'field', field)
            object.__setattr__(self, 'message', message)
            # Also store in private attributes for resolvers
            object.__setattr__(self, '_error_field', field)
            object.__setattr__(self, '_error_message', message)
        
        def resolve_field(self, info):
            """Resolver for field"""
            return self._error_field
        
        def resolve_message(self, info):
            """Resolver for message"""
            return self._error_message
    
    class BaseMutation(graphene.Mutation):
        """Base mutation class"""
        class Meta:
            abstract = True
        
        @classmethod
        def perform_mutation(cls, root, info, **kwargs):
            raise NotImplementedError("Subclasses must implement perform_mutation")
        
        @classmethod
        def mutate(cls, root, info, **kwargs):
            try:
                result = cls.perform_mutation(root, info, **kwargs)
                return result
            except ValidationError as e:
                # Create result object with errors as keyword argument
                return cls(errors=[Error(field='__all__', message=str(e))])
            except Exception as e:
                return cls(errors=[Error(field='__all__', message=str(e))])
    
    _SALEOR_AVAILABLE = False


# ============================================================================
# Object Types
# ============================================================================

class RegionType(graphene.ObjectType):
    """Region GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    code = graphene.String()
    name = graphene.String()
    default_currency = graphene.String()
    tax_rate = graphene.Decimal()
    timezone = graphene.String()
    locale = graphene.String()
    is_active = graphene.Boolean()


class BranchType(graphene.ObjectType):
    """Branch GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    name = graphene.String()
    code = graphene.String()
    region = graphene.Field(RegionType)
    address_line_1 = graphene.String()
    address_line_2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    postal_code = graphene.String()
    country = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    can_ship = graphene.Boolean()
    can_click_collect = graphene.Boolean()
    can_cross_border = graphene.Boolean()
    operating_hours = graphene.JSONString()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()


# ============================================================================
# Input Types
# ============================================================================

class BranchCreateInput(graphene.InputObjectType):
    """Input for creating a branch"""
    name = graphene.String(required=True)
    code = graphene.String(required=True)
    region_id = graphene.ID(required=True)
    address_line_1 = graphene.String(required=True)
    address_line_2 = graphene.String()
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    postal_code = graphene.String(required=True)
    country = graphene.String(required=True)
    phone = graphene.String(required=True)
    email = graphene.String(required=True)
    can_ship = graphene.Boolean(default_value=True)
    can_click_collect = graphene.Boolean(default_value=True)
    can_cross_border = graphene.Boolean(default_value=False)
    is_active = graphene.Boolean(default_value=True)
    operating_hours = graphene.JSONString()


class BranchUpdateInput(graphene.InputObjectType):
    """Input for updating a branch"""
    name = graphene.String()
    code = graphene.String()
    region_id = graphene.ID()
    address_line_1 = graphene.String()
    address_line_2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    postal_code = graphene.String()
    country = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    can_ship = graphene.Boolean()
    can_click_collect = graphene.Boolean()
    can_cross_border = graphene.Boolean()
    is_active = graphene.Boolean()
    operating_hours = graphene.JSONString()


# ============================================================================
# Queries
# ============================================================================

class BranchQueries(graphene.ObjectType):
    """Branch-related queries"""
    
    branches = graphene.List(
        BranchType,
        region_code=graphene.String(),
        is_active=graphene.Boolean(),
        description="Get all branches, optionally filtered by region or status"
    )
    
    branch = graphene.Field(
        BranchType,
        id=graphene.ID(),
        code=graphene.String(),
        description="Get a specific branch by ID or code"
    )
    
    def resolve_branches(self, info, region_code=None, is_active=None):
        """Resolve branches query"""
        queryset = Branch.objects.select_related('region').all()
        
        if region_code:
            queryset = queryset.filter(region__code=region_code)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        return queryset
    
    def resolve_branch(self, info, id=None, code=None):
        """Resolve single branch query"""
        if id:
            try:
                return Branch.objects.select_related('region').get(id=id)
            except Branch.DoesNotExist:
                return None
        elif code:
            try:
                return Branch.objects.select_related('region').get(code=code)
            except Branch.DoesNotExist:
                return None
        return None


# ============================================================================
# Mutations
# ============================================================================

class BranchCreate(BaseMutation):
    """Create branch mutation"""
    branch = graphene.Field(BranchType)
    errors = graphene.List(Error)
    
    class Arguments:
        input = BranchCreateInput(required=True)
    
    @classmethod
    def perform_mutation(cls, root, info, input):
        """Create a new branch"""
        try:
            # Convert region_id to integer if it's a string
            region_id = getattr(input, 'region_id', None)
            if region_id is None:
                raise ValidationError("region_id is required")
            if isinstance(region_id, str):
                # Try to extract numeric ID from string
                try:
                    region_id = int(region_id)
                except ValueError:
                    raise ValidationError(f"Invalid region_id format: '{region_id}'. Must be a valid integer.")
            
            branch = Branch.objects.create(
                name=input.name,
                code=input.code,
                region_id=region_id,
                address_line_1=input.address_line_1,
                address_line_2=getattr(input, 'address_line_2', ''),
                city=input.city,
                state=input.state,
                postal_code=input.postal_code,
                country=input.country,
                phone=input.phone,
                email=input.email,
                can_ship=getattr(input, 'can_ship', True),
                can_click_collect=getattr(input, 'can_click_collect', True),
                can_cross_border=getattr(input, 'can_cross_border', False),
                is_active=getattr(input, 'is_active', True),
                operating_hours=getattr(input, 'operating_hours', {}),
            )
            
            return BranchCreate(branch=branch, errors=None)
        except ValidationError as e:
            return BranchCreate(branch=None, errors=[Error(field='__all__', message=str(e))])
        except Exception as e:
            return BranchCreate(branch=None, errors=[Error(field='__all__', message=str(e))])


class BranchUpdate(BaseMutation):
    """Update branch mutation"""
    branch = graphene.Field(BranchType)
    errors = graphene.List(Error)
    
    class Arguments:
        id = graphene.ID(required=True)
        input = BranchUpdateInput(required=True)
    
    @classmethod
    def perform_mutation(cls, root, info, id, input):
        """Update an existing branch"""
        try:
            branch = Branch.objects.get(id=id)
            
            # Update fields if provided
            if hasattr(input, 'name') and input.name is not None:
                branch.name = input.name
            if hasattr(input, 'code') and input.code is not None:
                branch.code = input.code
            if hasattr(input, 'region_id') and input.region_id is not None:
                region_id = input.region_id
                if isinstance(region_id, str):
                    try:
                        region_id = int(region_id)
                    except ValueError:
                        raise ValidationError(f"Invalid region_id format: '{region_id}'. Must be a valid integer.")
                branch.region_id = region_id
            if hasattr(input, 'address_line_1') and input.address_line_1 is not None:
                branch.address_line_1 = input.address_line_1
            if hasattr(input, 'address_line_2') and input.address_line_2 is not None:
                branch.address_line_2 = input.address_line_2
            if hasattr(input, 'city') and input.city is not None:
                branch.city = input.city
            if hasattr(input, 'state') and input.state is not None:
                branch.state = input.state
            if hasattr(input, 'postal_code') and input.postal_code is not None:
                branch.postal_code = input.postal_code
            if hasattr(input, 'country') and input.country is not None:
                branch.country = input.country
            if hasattr(input, 'phone') and input.phone is not None:
                branch.phone = input.phone
            if hasattr(input, 'email') and input.email is not None:
                branch.email = input.email
            if hasattr(input, 'can_ship') and input.can_ship is not None:
                branch.can_ship = input.can_ship
            if hasattr(input, 'can_click_collect') and input.can_click_collect is not None:
                branch.can_click_collect = input.can_click_collect
            if hasattr(input, 'can_cross_border') and input.can_cross_border is not None:
                branch.can_cross_border = input.can_cross_border
            if hasattr(input, 'is_active') and input.is_active is not None:
                branch.is_active = input.is_active
            if hasattr(input, 'operating_hours') and input.operating_hours is not None:
                branch.operating_hours = input.operating_hours
            
            branch.save()
            
            return BranchUpdate(branch=branch, errors=None)
        except Branch.DoesNotExist:
            return BranchUpdate(branch=None, errors=[Error(field='id', message='Branch not found')])
        except ValidationError as e:
            return BranchUpdate(branch=None, errors=[Error(field='__all__', message=str(e))])
        except Exception as e:
            return BranchUpdate(branch=None, errors=[Error(field='__all__', message=str(e))])


class BranchDelete(BaseMutation):
    """Delete branch mutation"""
    success = graphene.Boolean()
    errors = graphene.List(Error)
    
    class Arguments:
        id = graphene.ID(required=True)
    
    @classmethod
    def perform_mutation(cls, root, info, id):
        """Delete a branch"""
        try:
            branch = Branch.objects.get(id=id)
            branch.delete()
            return BranchDelete(success=True, errors=None)
        except Branch.DoesNotExist:
            return BranchDelete(success=False, errors=[Error(field='id', message='Branch not found')])
        except Exception as e:
            return BranchDelete(success=False, errors=[Error(field='__all__', message=str(e))])


class BranchMutations(graphene.ObjectType):
    """Branch-related mutations"""
    branch_create = BranchCreate.Field()
    branch_update = BranchUpdate.Field()
    branch_delete = BranchDelete.Field()
