"""
GraphQL schema for branches
"""
import graphene
from django.core.exceptions import ValidationError
import json
import os
import time

from saleor_extensions.branches.models import Branch

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", ".cursor", "debug.log")


# #region agent log
def _agent_log(location, message, data, hypothesis_id):
    try:
        abs_path = os.path.abspath(LOG_PATH)
        log_dir = os.path.dirname(abs_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        entry = {
            "sessionId": "debug-session",
            "runId": "debug-run1",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        with open(abs_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass
# #endregion

# Try to import BaseMutation, DateTime, JSON, and Decimal from Saleor, fallback to graphene
try:
    from saleor.graphql.core.mutations import BaseMutation
    from saleor.graphql.core.types import Error
    from saleor.graphql.core.scalars import DateTime, JSON, Decimal
    _SALEOR_AVAILABLE = True
except ImportError:
    # Fallback to graphene types if Saleor's types are not available
    DateTime = graphene.DateTime
    JSON = graphene.JSONString
    Decimal = graphene.Decimal
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

class BranchType(graphene.ObjectType):
    """Branch GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    name = graphene.String()
    code = graphene.String()
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
    operating_hours = JSON()
    is_active = graphene.Boolean()
    created_at = DateTime()
    updated_at = DateTime()


# ============================================================================
# Input Types
# ============================================================================

class BranchCreateInput(graphene.InputObjectType):
    """Input for creating a branch (uses camelCase for GraphQL convention)"""
    name = graphene.String(required=True)
    code = graphene.String(required=True)
    address_line_1 = graphene.String()  # Keep for backward compatibility
    addressLine1 = graphene.String(required=True)  # Primary camelCase field
    address_line_2 = graphene.String()  # Keep for backward compatibility
    addressLine2 = graphene.String()  # Primary camelCase field
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    postal_code = graphene.String()  # Keep for backward compatibility
    postalCode = graphene.String(required=True)  # Primary camelCase field
    country = graphene.String(required=True)
    phone = graphene.String(required=True)
    email = graphene.String(required=True)
    can_ship = graphene.Boolean()  # Keep for backward compatibility
    canShip = graphene.Boolean(default_value=True)  # Primary camelCase field
    can_click_collect = graphene.Boolean()  # Keep for backward compatibility
    canClickCollect = graphene.Boolean(default_value=True)  # Primary camelCase field
    can_cross_border = graphene.Boolean()  # Keep for backward compatibility
    canCrossBorder = graphene.Boolean(default_value=False)  # Primary camelCase field
    is_active = graphene.Boolean()  # Keep for backward compatibility
    isActive = graphene.Boolean(default_value=True)  # Primary camelCase field
    operating_hours = JSON()  # Keep for backward compatibility
    operatingHours = JSON()  # Primary camelCase field


class BranchUpdateInput(graphene.InputObjectType):
    """Input for updating a branch (uses camelCase for GraphQL convention)"""
    name = graphene.String()
    code = graphene.String()
    address_line_1 = graphene.String()  # Keep for backward compatibility
    addressLine1 = graphene.String()  # Primary camelCase field
    address_line_2 = graphene.String()  # Keep for backward compatibility
    addressLine2 = graphene.String()  # Primary camelCase field
    city = graphene.String()
    state = graphene.String()
    postal_code = graphene.String()  # Keep for backward compatibility
    postalCode = graphene.String()  # Primary camelCase field
    country = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    can_ship = graphene.Boolean()  # Keep for backward compatibility
    canShip = graphene.Boolean()  # Primary camelCase field
    can_click_collect = graphene.Boolean()  # Keep for backward compatibility
    canClickCollect = graphene.Boolean()  # Primary camelCase field
    can_cross_border = graphene.Boolean()  # Keep for backward compatibility
    canCrossBorder = graphene.Boolean()  # Primary camelCase field
    is_active = graphene.Boolean()  # Keep for backward compatibility
    isActive = graphene.Boolean()  # Primary camelCase field
    operating_hours = JSON()  # Keep for backward compatibility
    operatingHours = JSON()  # Primary camelCase field


# ============================================================================
# Queries
# ============================================================================

class BranchQueries(graphene.ObjectType):
    """Branch-related queries"""
    
    branches = graphene.List(
        BranchType,
        is_active=graphene.Boolean(),
        description="Get all branches, optionally filtered by status"
    )
    
    branch = graphene.Field(
        BranchType,
        id=graphene.ID(),
        code=graphene.String(),
        description="Get a specific branch by ID or code"
    )
    
    def resolve_branches(self, info, is_active=None):
        """Resolve branches query"""
        # #region agent log
        _agent_log(
            "branches/schema.py:resolve_branches:entry",
            "Resolve branches called",
            {"hypothesisId": "H2", "is_active": is_active},
            "H2",
        )
        # #endregion
        queryset = Branch.objects.all()
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        # #region agent log
        _agent_log(
            "branches/schema.py:resolve_branches:exit",
            "Resolve branches returning",
            {"hypothesisId": "H2", "count": queryset.count()},
            "H2",
        )
        # #endregion
        return queryset
    
    def resolve_branch(self, info, id=None, code=None):
        """Resolve single branch query"""
        if id:
            try:
                return Branch.objects.get(id=id)
            except Branch.DoesNotExist:
                return None
        elif code:
            try:
                return Branch.objects.get(code=code)
            except Branch.DoesNotExist:
                return None
        return None


# ============================================================================
# Mutations
# ============================================================================

class BranchCreate(BaseMutation):
    """Create branch mutation"""
    
    class Meta:
        description = "Create a new branch"
        error_type_class = Error
    
    branch = graphene.Field(BranchType)
    errors = graphene.List(Error)
    
    class Arguments:
        input = BranchCreateInput(required=True)
    
    @classmethod
    def perform_mutation(cls, root, info, input):
        """Create a new branch"""
        try:
            # Get field values, preferring camelCase but falling back to snake_case
            address_line_1 = getattr(input, 'addressLine1', None) or getattr(input, 'address_line_1', None)
            address_line_2 = getattr(input, 'addressLine2', None) or getattr(input, 'address_line_2', None) or ''
            postal_code = getattr(input, 'postalCode', None) or getattr(input, 'postal_code', None)
            can_ship = getattr(input, 'canShip', getattr(input, 'can_ship', True))
            can_click_collect = getattr(input, 'canClickCollect', getattr(input, 'can_click_collect', True))
            can_cross_border = getattr(input, 'canCrossBorder', getattr(input, 'can_cross_border', False))
            is_active = getattr(input, 'isActive', getattr(input, 'is_active', True))
            operating_hours = getattr(input, 'operatingHours', None) or getattr(input, 'operating_hours', None) or {}
            
            branch = Branch.objects.create(
                name=input.name,
                code=input.code,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=input.city,
                state=input.state,
                postal_code=postal_code,
                country=input.country,
                phone=input.phone,
                email=input.email,
                can_ship=can_ship,
                can_click_collect=can_click_collect,
                can_cross_border=can_cross_border,
                is_active=is_active,
                operating_hours=operating_hours,
            )
            
            # #region agent log
            _agent_log(
                "branches/schema.py:BranchCreate:success",
                "Branch created successfully",
                {"hypothesisId": "H3", "branch_id": branch.id},
                "H3",
            )
            # #endregion
            
            return BranchCreate(branch=branch, errors=None)
        except ValidationError as e:
            # #region agent log
            _agent_log(
                "branches/schema.py:BranchCreate:validation_error",
                "Validation error during branch create",
                {"hypothesisId": "H3", "error": str(e)},
                "H3",
            )
            # #endregion
            return BranchCreate(branch=None, errors=[Error(field='__all__', message=str(e))])
        except Exception as e:
            # #region agent log
            _agent_log(
                "branches/schema.py:BranchCreate:exception",
                "Unexpected error during branch create",
                {"hypothesisId": "H3", "error": str(e)},
                "H3",
            )
            # #endregion
            return BranchCreate(branch=None, errors=[Error(field='__all__', message=str(e))])


class BranchUpdate(BaseMutation):
    """Update branch mutation"""
    
    class Meta:
        description = "Update an existing branch"
        error_type_class = Error
    
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
            
            # Update fields if provided, handling both camelCase and snake_case
            if hasattr(input, 'name') and input.name is not None:
                branch.name = input.name
            if hasattr(input, 'code') and input.code is not None:
                branch.code = input.code
            # Handle address fields
            address_line_1 = getattr(input, 'addressLine1', None) or getattr(input, 'address_line_1', None)
            if address_line_1 is not None:
                branch.address_line_1 = address_line_1
            address_line_2 = getattr(input, 'addressLine2', None) or getattr(input, 'address_line_2', None)
            if address_line_2 is not None:
                branch.address_line_2 = address_line_2
            if hasattr(input, 'city') and input.city is not None:
                branch.city = input.city
            if hasattr(input, 'state') and input.state is not None:
                branch.state = input.state
            postal_code = getattr(input, 'postalCode', None) or getattr(input, 'postal_code', None)
            if postal_code is not None:
                branch.postal_code = postal_code
            if hasattr(input, 'country') and input.country is not None:
                branch.country = input.country
            if hasattr(input, 'phone') and input.phone is not None:
                branch.phone = input.phone
            if hasattr(input, 'email') and input.email is not None:
                branch.email = input.email
            # Handle boolean fields
            can_ship = getattr(input, 'canShip', None)
            if can_ship is None:
                can_ship = getattr(input, 'can_ship', None)
            if can_ship is not None:
                branch.can_ship = can_ship
            can_click_collect = getattr(input, 'canClickCollect', None)
            if can_click_collect is None:
                can_click_collect = getattr(input, 'can_click_collect', None)
            if can_click_collect is not None:
                branch.can_click_collect = can_click_collect
            can_cross_border = getattr(input, 'canCrossBorder', None)
            if can_cross_border is None:
                can_cross_border = getattr(input, 'can_cross_border', None)
            if can_cross_border is not None:
                branch.can_cross_border = can_cross_border
            is_active = getattr(input, 'isActive', None)
            if is_active is None:
                is_active = getattr(input, 'is_active', None)
            if is_active is not None:
                branch.is_active = is_active
            operating_hours = getattr(input, 'operatingHours', None) or getattr(input, 'operating_hours', None)
            if operating_hours is not None:
                branch.operating_hours = operating_hours
            
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
    
    class Meta:
        description = "Delete a branch"
        error_type_class = Error
    
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
