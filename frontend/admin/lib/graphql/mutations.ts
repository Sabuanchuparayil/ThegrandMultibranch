import { gql } from '@apollo/client';

// Authentication Mutations
export const LOGIN = gql`
  mutation Login($input: LoginInput!) {
    login(input: $input) {
      token
      user {
        id
        email
        firstName
        lastName
        isStaff
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

// Branch Mutations
export const CREATE_BRANCH = gql`
  mutation CreateBranch($input: BranchCreateInput!) {
    branchCreate(input: $input) {
      branch {
        id
        name
        code
        region {
          id
          name
          code
        }
        addressLine1
        addressLine2
        city
        state
        postalCode
        country
        phone
        email
        canShip
        canClickCollect
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

export const UPDATE_BRANCH = gql`
  mutation UpdateBranch($id: ID!, $input: BranchUpdateInput!) {
    branchUpdate(id: $id, input: $input) {
      branch {
        id
        name
        code
        region {
          id
          name
          code
        }
        addressLine1
        addressLine2
        city
        state
        postalCode
        country
        phone
        email
        canShip
        canClickCollect
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

export const DELETE_BRANCH = gql`
  mutation DeleteBranch($id: ID!) {
    branchDelete(id: $id) {
      success
      errors {
        field
        message
      }
    }
  }
`;

// Product Mutations
export const CREATE_PRODUCT = gql`
  mutation CreateProduct($input: ProductCreateInput!) {
    productCreate(input: $input) {
      product {
        id
        name
        slug
        description
        isPublished
      }
      errors {
        field
        message
      }
    }
  }
`;

export const UPDATE_PRODUCT = gql`
  mutation UpdateProduct($id: ID!, $input: ProductUpdateInput!) {
    productUpdate(id: $id, input: $input) {
      product {
        id
        name
        slug
        description
        isPublished
      }
      errors {
        field
        message
      }
    }
  }
`;

export const DELETE_PRODUCT = gql`
  mutation DeleteProduct($id: ID!) {
    productDelete(id: $id) {
      success
      errors {
        field
        message
      }
    }
  }
`;

// Order Mutations
export const UPDATE_ORDER_STATUS = gql`
  mutation UpdateOrderStatus($id: ID!, $status: OrderStatus!) {
    orderUpdate(id: $id, input: { status: $status }) {
      order {
        id
        number
        status
      }
      errors {
        field
        message
      }
    }
  }
`;

// Return Mutations
export const CREATE_RETURN_REQUEST = gql`
  mutation CreateReturnRequest($input: ReturnRequestCreateInput!) {
    returnRequestCreate(input: $input) {
      returnRequest {
        id
        rmaNumber
        orderId
        reason
        status
      }
      errors {
        field
        message
      }
    }
  }
`;

export const UPDATE_RETURN_STATUS = gql`
  mutation UpdateReturnStatus($id: ID!, $status: ReturnStatus!) {
    returnRequestUpdate(id: $id, input: { status: $status }) {
      returnRequest {
        id
        rmaNumber
        status
      }
      errors {
        field
        message
      }
    }
  }
`;

// Promotion Mutations
export const CREATE_PROMOTION = gql`
  mutation CreatePromotion($input: PromotionCreateInput!) {
    promotionCreate(input: $input) {
      promotion {
        id
        name
        code
        discountType
        discountValue
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

export const UPDATE_PROMOTION = gql`
  mutation UpdatePromotion($id: ID!, $input: PromotionUpdateInput!) {
    promotionUpdate(id: $id, input: $input) {
      promotion {
        id
        name
        code
        discountType
        discountValue
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

export const DELETE_PROMOTION = gql`
  mutation DeletePromotion($id: ID!) {
    promotionDelete(id: $id) {
      success
      errors {
        field
        message
      }
    }
  }
`;

// Customer Mutations
export const CREATE_CUSTOMER = gql`
  mutation CreateCustomer($input: CustomerCreateInput!) {
    customerCreate(input: $input) {
      user {
        id
        email
        firstName
        lastName
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

export const UPDATE_CUSTOMER = gql`
  mutation UpdateCustomer($id: ID!, $input: CustomerUpdateInput!) {
    customerUpdate(id: $id, input: $input) {
      user {
        id
        email
        firstName
        lastName
        isActive
      }
      errors {
        field
        message
      }
    }
  }
`;

export const DELETE_CUSTOMER = gql`
  mutation DeleteCustomer($id: ID!) {
    customerDelete(id: $id) {
      success
      errors {
        field
        message
      }
    }
  }
`;

// Inventory Mutations
export const CREATE_INVENTORY = gql`
  mutation CreateInventory($input: InventoryCreateInput!) {
    inventoryCreate(input: $input) {
      inventory {
        id
        quantity
        availableQuantity
        reservedQuantity
        isLowStock
        branch {
          id
          name
        }
        productVariant {
          id
          name
          sku
        }
      }
      errors {
        field
        message
      }
    }
  }
`;

export const UPDATE_INVENTORY = gql`
  mutation UpdateInventory($id: ID!, $input: InventoryUpdateInput!) {
    inventoryUpdate(id: $id, input: $input) {
      inventory {
        id
        quantity
        availableQuantity
        reservedQuantity
        isLowStock
        lowStockThreshold
      }
      errors {
        field
        message
      }
    }
  }
`;

export const ADJUST_INVENTORY_STOCK = gql`
  mutation AdjustInventoryStock($id: ID!, $quantity: Int!, $movementType: StockMovementType!) {
    inventoryAdjustStock(id: $id, quantity: $quantity, movementType: $movementType) {
      inventory {
        id
        quantity
        availableQuantity
      }
      stockMovement {
        id
        movementType
        quantity
      }
      errors {
        field
        message
      }
    }
  }
`;

