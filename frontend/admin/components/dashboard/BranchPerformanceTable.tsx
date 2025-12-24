/**
 * Branch Performance Table Component
 * Displays performance metrics for multiple branches
 */
'use client';

import React from 'react';

export interface BranchPerformance {
  branchId: string;
  branchName: string;
  sales: number;
  orders: number;
  growth: number;
  currency: string;
}

interface BranchPerformanceTableProps {
  data: BranchPerformance[];
  onBranchClick?: (branchId: string) => void;
}

export const BranchPerformanceTable: React.FC<BranchPerformanceTableProps> = ({
  data,
  onBranchClick,
}) => {
  const formatCurrency = (value: number, currency: string = 'GBP') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatGrowth = (growth: number) => {
    const sign = growth > 0 ? '+' : '';
    const color = growth > 0 ? 'text-green-600' : growth < 0 ? 'text-red-600' : 'text-gray-600';
    return <span className={color}>{sign}{growth.toFixed(1)}%</span>;
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Branch Performance</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Branch
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Sales
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Orders
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Growth
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((branch) => (
              <tr
                key={branch.branchId}
                onClick={() => onBranchClick?.(branch.branchId)}
                className={onBranchClick ? 'hover:bg-gray-50 cursor-pointer' : ''}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{branch.branchName}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                  {formatCurrency(branch.sales, branch.currency)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                  {branch.orders}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                  {formatGrowth(branch.growth)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

