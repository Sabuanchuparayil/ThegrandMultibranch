/**
 * GraphQL queries for dashboard data
 * These queries fetch KPIs and chart data for executive and branch dashboards
 */

import { gql } from '@apollo/client';

// ============================================================================
// Executive Dashboard Queries
// ============================================================================

export const GET_EXECUTIVE_KPIS = gql`
  query GetExecutiveKPIs($dateFrom: DateTime!, $dateTo: DateTime!, $regionCode: String) {
    # Sales Summary
    orders(
      filter: {
        status: FULFILLED
        created: { gte: $dateFrom, lte: $dateTo }
      }
      first: 1000
    ) {
      totalCount
      edges {
        node {
          id
          number
          total {
            gross {
              amount
              currency
            }
            net {
              amount
              currency
            }
          }
          created
          user {
            id
            email
          }
        }
      }
    }
    
    # Get regions for filter
    regions {
      id
      code
      name
    }
  }
`;

export const GET_SALES_TREND = gql`
  query GetSalesTrend($days: Int!, $regionCode: String) {
    # Sales trend data
    # This would need to be implemented in your backend
    # For now, returns orders grouped by day
    orders(
      filter: {
        status: FULFILLED
        created: { gte: $dateFrom }
      }
      first: 10000
    ) {
      edges {
        node {
          id
          total {
            gross {
              amount
            }
          }
          created
        }
      }
    }
  }
`;

export const GET_REGION_PERFORMANCE = gql`
  query GetRegionPerformance($dateFrom: DateTime!, $dateTo: DateTime!) {
    # Performance metrics by region
    # This would query your custom OrderBranchAssignment model
    orders(
      filter: {
        status: FULFILLED
        created: { gte: $dateFrom, lte: $dateTo }
      }
      first: 10000
    ) {
      edges {
        node {
          id
          total {
            gross {
              amount
              currency
            }
          }
          # Add branch assignment query here
        }
      }
    }
  }
`;

export const GET_TOP_PRODUCTS = gql`
  query GetTopProducts($dateFrom: DateTime!, $dateTo: DateTime!, $limit: Int!) {
    # Top selling products
    orders(
      filter: {
        status: FULFILLED
        created: { gte: $dateFrom, lte: $dateTo }
      }
      first: 1000
    ) {
      edges {
        node {
          lines {
            id
            productName
            variantName
            quantity
            unitPrice {
              gross {
                amount
                currency
              }
            }
          }
        }
      }
    }
  }
`;

// ============================================================================
// Branch Dashboard Queries
// ============================================================================

export const GET_BRANCH_KPIS = gql`
  query GetBranchKPIs($branchId: ID!, $dateFrom: DateTime!, $dateTo: DateTime!) {
    # Branch information
    branch(id: $branchId) @client {
      id
      name
      code
      region {
        code
        name
      }
    }
    
    # Branch orders for the period
    orders(
      filter: {
        created: { gte: $dateFrom, lte: $dateTo }
        # Add branch filter when available
      }
      first: 1000
    ) {
      totalCount
      edges {
        node {
          id
          number
          total {
            gross {
              amount
              currency
            }
          }
          status
          created
        }
      }
    }
    
    # Today's orders
    todayOrders: orders(
      filter: {
        created: { gte: $todayStart, lte: $todayEnd }
      }
      first: 1000
    ) {
      totalCount
      edges {
        node {
          id
          total {
            gross {
              amount
            }
          }
        }
      }
    }
  }
`;

export const GET_BRANCH_INVENTORY_STATUS = gql`
  query GetBranchInventoryStatus($branchId: ID!) {
    branchInventory(branchId: $branchId, lowStockOnly: false) {
      id
      quantity
      reservedQuantity
      availableQuantity
      isLowStock
      lowStockThreshold
      productVariant {
        id
        name
        sku
        product {
          name
        }
      }
    }
  }
`;

export const GET_BRANCH_SALES_TREND = gql`
  query GetBranchSalesTrend($branchId: ID!, $days: Int!) {
    # Sales trend for specific branch
    # Implement based on your GraphQL schema
    branchInventory(branchId: $branchId) {
      id
      # Add trend data here
    }
  }
`;

export const GET_BRANCH_STOCK_MOVEMENTS = gql`
  query GetBranchStockMovements($branchId: ID!, $limit: Int!) {
    stockMovements(branchId: $branchId, limit: $limit) {
      id
      movementType
      quantity
      referenceNumber
      notes
      createdAt
      productVariant {
        name
        sku
      }
    }
  }
`;

export const GET_BRANCH_CLICK_COLLECT = gql`
  query GetBranchClickCollect($branchId: ID!, $status: String) {
    # Click & Collect orders for branch
    # Implement based on your GraphQL schema
  }
`;

// ============================================================================
// Shared Queries
// ============================================================================

export const GET_LOW_STOCK_ALERTS = gql`
  query GetLowStockAlerts($branchId: ID, $regionCode: String) {
    lowStockAlerts(branchId: $branchId) {
      id
      currentQuantity
      threshold
      status
      branchInventory {
        id
        branch {
          name
          code
        }
        productVariant {
          name
          sku
        }
      }
      createdAt
    }
  }
`;

export const GET_INVENTORY_VALUE = gql`
  query GetInventoryValue($branchId: ID, $regionCode: String) {
    # Calculate total inventory value
    # This would need aggregation in your backend
    branchInventory(branchId: $branchId) {
      id
      quantity
      productVariant {
        id
        # Add pricing information
      }
    }
  }
`;

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Calculate date range for queries
 */
export function getDateRange(days: number = 30) {
  const to = new Date();
  const from = new Date();
  from.setDate(from.getDate() - days);
  
  return {
    from: from.toISOString(),
    to: to.toISOString(),
  };
}

/**
 * Get today's date range
 */
export function getTodayRange() {
  const today = new Date();
  const start = new Date(today.setHours(0, 0, 0, 0));
  const end = new Date(today.setHours(23, 59, 59, 999));
  
  return {
    from: start.toISOString(),
    to: end.toISOString(),
  };
}

/**
 * Get this week's date range
 */
export function getWeekRange() {
  const today = new Date();
  const start = new Date(today);
  start.setDate(today.getDate() - 7);
  start.setHours(0, 0, 0, 0);
  
  return {
    from: start.toISOString(),
    to: today.toISOString(),
  };
}
