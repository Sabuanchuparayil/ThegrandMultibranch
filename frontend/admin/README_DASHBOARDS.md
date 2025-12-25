# Executive & Branch Dashboards

## Overview

Real-time dashboards with KPIs and visualizations for executive overview and branch-level operations.

## Features

### Executive Dashboard
- **Total Revenue** - Across all regions/branches
- **Total Orders** - Order count and trends
- **Average Order Value** - AOV metrics
- **Active Customers** - Customer count
- **Inventory Value** - Total inventory value
- **Low Stock Items** - Items needing attention
- **Sales Trends** - Multi-period sales charts
- **Region Performance** - Performance by region (UK, UAE, India)
- **Category Sales** - Sales breakdown by product category
- **Top Products** - Best performing products

### Branch Dashboard
- **Today's Metrics** - Revenue and orders for today
- **Week Metrics** - Weekly performance
- **Inventory Status** - Branch inventory levels
- **Low Stock Alerts** - Items below threshold
- **Daily Sales Trend** - Week-over-week trends
- **Hourly Performance** - Today's hourly breakdown
- **Category Performance** - Sales by category
- **Sales Channel Breakdown** - Walk-in vs Online
- **Click & Collect** - C&C order metrics

## Architecture

### Components Structure

```
frontend/admin/
├── app/
│   └── dashboard/
│       ├── layout.tsx              # Dashboard navigation layout
│       ├── executive/
│       │   └── page.tsx            # Executive dashboard page
│       └── branch/
│           └── page.tsx            # Branch dashboard page
├── components/
│   └── dashboard/
│       ├── KPICard.tsx             # Reusable KPI card component
│       └── ChartContainer.tsx      # Chart wrapper component
└── lib/
    ├── graphql/
    │   └── dashboard-queries.ts    # GraphQL queries for dashboards
    └── hooks/
        └── useDashboardData.ts     # React hooks for data fetching
```

## Real-time Updates

Dashboards use **polling** to fetch fresh data:

- **Executive Dashboard**: Polls every 30 seconds
- **Branch Dashboard**: Polls every 30 seconds
- **Inventory Data**: Polls every 60 seconds
- **Low Stock Alerts**: Polls every 60 seconds

This ensures KPIs and charts stay up-to-date without manual refresh.

## GraphQL Integration

### Queries Used

1. `GET_EXECUTIVE_KPIS` - Main KPIs for executive dashboard
2. `GET_SALES_TREND` - Sales trend data for charts
3. `GET_REGION_PERFORMANCE` - Performance by region
4. `GET_BRANCH_KPIS` - Branch-specific KPIs
5. `GET_BRANCH_INVENTORY_STATUS` - Branch inventory data
6. `GET_LOW_STOCK_ALERTS` - Low stock items

### Custom Hooks

- `useExecutiveDashboard()` - Fetches executive dashboard data
- `useBranchDashboard()` - Fetches branch dashboard data
- `useLowStockAlerts()` - Fetches low stock alerts
- `useRealtimeUpdates()` - Manages real-time polling

## Charts Library

Uses **Recharts** for all visualizations:

- Line charts for trends
- Bar charts for comparisons
- Area charts for cumulative data
- Pie charts for category breakdowns

## Installation

Ensure Recharts is installed:

```bash
cd frontend/admin
npm install recharts
```

## Usage

### Executive Dashboard

```typescript
// app/dashboard/executive/page.tsx
import { useExecutiveDashboard } from '@/lib/hooks/useDashboardData';

function ExecutiveDashboard() {
  const { kpis, loading, error } = useExecutiveDashboard({
    dateFrom: new Date('2024-01-01'),
    dateTo: new Date(),
    regionCode: 'UK', // Optional filter
  });

  // Use kpis data to display cards and charts
}
```

### Branch Dashboard

```typescript
// app/dashboard/branch/page.tsx
import { useBranchDashboard } from '@/lib/hooks/useDashboardData';

function BranchDashboard() {
  const branchId = '1'; // From URL params or context
  
  const { kpis, inventory, lowStockCount, loading } = useBranchDashboard({
    branchId,
    dateFrom: new Date('2024-01-01'),
    dateTo: new Date(),
  });

  // Use data to display branch-specific metrics
}
```

## KPI Calculations

KPIs are calculated from GraphQL query results:

- **Revenue**: Sum of order totals
- **Orders**: Count of orders
- **Average Order Value**: Revenue / Orders
- **Customers**: Unique customer count
- **Change %**: Comparison with previous period

## Date Range Filtering

Both dashboards support date range filtering:

- Executive: Default 30 days
- Branch: Default 7 days
- Custom ranges via date pickers

## Region Filtering (Executive)

Executive dashboard can filter by region:

- All Regions (default)
- UK
- UAE
- India

## Responsive Design

- Mobile: Single column layout
- Tablet: 2-column grid
- Desktop: 3-4 column grid
- Charts adapt to screen size

## Performance Optimizations

1. **Polling Intervals**: Different intervals for different data types
2. **Cache Policy**: Uses `cache-first` for fresh data (Apollo Client 3.x compatible)
3. **Lazy Loading**: Charts load only when visible
4. **Debounced Filters**: Date/region filters are debounced

## Future Enhancements

- [ ] WebSocket subscriptions for real-time updates
- [ ] Export dashboard data to PDF/Excel
- [ ] Custom date range presets
- [ ] Drill-down capabilities
- [ ] Comparative analysis (year-over-year)
- [ ] Custom dashboard configuration
- [ ] Scheduled reports

## Testing

Test dashboards with:

1. **Mock Data**: Currently uses mock data for demonstration
2. **GraphQL Queries**: Connect to actual backend when ready
3. **Real Data**: Use after database is populated

## Notes

- Current implementation uses mock data for demonstration
- Connect GraphQL queries when backend API is ready
- All queries are defined but need backend implementation
- KPI calculations are placeholder - adjust based on actual data structure

