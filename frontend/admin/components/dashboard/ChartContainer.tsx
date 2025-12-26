/**
 * Chart Container Component
 * Wrapper for Recharts components with consistent styling
 */

import { ReactNode } from 'react';
import { ResponsiveContainer } from 'recharts';

interface ChartContainerProps {
  title: string;
  children: ReactNode;
  height?: number;
  className?: string;
  actions?: ReactNode;
}

export default function ChartContainer({
  title,
  children,
  height = 300,
  className = '',
  actions,
}: ChartContainerProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        {actions && <div className="flex items-center gap-2">{actions}</div>}
      </div>
      <ResponsiveContainer width="100%" height={height}>
        {children}
      </ResponsiveContainer>
    </div>
  );
}


