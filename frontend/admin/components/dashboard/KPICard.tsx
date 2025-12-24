/**
 * Reusable KPI Card Component
 * Used in both executive and branch dashboards
 */

import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/react/24/outline';

export interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: React.ComponentType<{ className?: string }>;
  trend?: 'up' | 'down' | 'neutral';
  color?: 'blue' | 'green' | 'purple' | 'orange' | 'red';
  loading?: boolean;
}

const colorClasses = {
  blue: {
    bg: 'bg-blue-500',
    text: 'text-blue-600',
  },
  green: {
    bg: 'bg-green-500',
    text: 'text-green-600',
  },
  purple: {
    bg: 'bg-purple-500',
    text: 'text-purple-600',
  },
  orange: {
    bg: 'bg-orange-500',
    text: 'text-orange-600',
  },
  red: {
    bg: 'bg-red-500',
    text: 'text-red-600',
  },
};

export default function KPICard({
  title,
  value,
  change,
  changeLabel = 'vs last period',
  icon: Icon,
  trend,
  color = 'blue',
  loading = false,
}: KPICardProps) {
  const colors = colorClasses[color];
  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600',
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-32 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-20"></div>
          </div>
          <div className="w-14 h-14 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {change !== undefined && (
            <div className="flex items-center mt-2">
              {trend === 'up' && (
                <ArrowTrendingUpIcon className={`h-4 w-4 ${trendColors.up} mr-1`} />
              )}
              {trend === 'down' && (
                <ArrowTrendingDownIcon className={`h-4 w-4 ${trendColors.down} mr-1`} />
              )}
              <span
                className={`text-sm font-medium ${
                  trend ? trendColors[trend] : 'text-gray-600'
                }`}
              >
                {change > 0 ? '+' : ''}
                {change}% {changeLabel}
              </span>
            </div>
          )}
        </div>
        <div className={`${colors.bg} p-3 rounded-lg`}>
          <Icon className="h-8 w-8 text-white" />
        </div>
      </div>
    </div>
  );
}
