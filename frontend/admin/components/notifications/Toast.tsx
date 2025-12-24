'use client';

import { useEffect } from 'react';
import { CheckCircleIcon, XCircleIcon, InformationCircleIcon, ExclamationTriangleIcon, XMarkIcon } from '@heroicons/react/24/outline';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

interface ToastProps {
  toast: Toast;
  onClose: (id: string) => void;
}

export function ToastComponent({ toast, onClose }: ToastProps) {
  useEffect(() => {
    if (toast.duration && toast.duration > 0) {
      const timer = setTimeout(() => {
        onClose(toast.id);
      }, toast.duration);
      return () => clearTimeout(timer);
    }
  }, [toast.id, toast.duration, onClose]);

  const icons = {
    success: CheckCircleIcon,
    error: XCircleIcon,
    info: InformationCircleIcon,
    warning: ExclamationTriangleIcon,
  };

  const colors = {
    success: 'bg-green-50 border-green-200 text-green-800',
    error: 'bg-red-50 border-red-200 text-red-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
  };

  const iconColors = {
    success: 'text-green-400',
    error: 'text-red-400',
    info: 'text-blue-400',
    warning: 'text-yellow-400',
  };

  const Icon = icons[toast.type];
  const colorClass = colors[toast.type];
  const iconColorClass = iconColors[toast.type];

  return (
    <div
      className={`${colorClass} border-l-4 rounded-lg shadow-lg p-4 mb-4 flex items-start animate-in slide-in-from-right-full duration-300`}
      role="alert"
    >
      <div className="flex-shrink-0">
        <Icon className={`h-5 w-5 ${iconColorClass}`} />
      </div>
      <div className="ml-3 flex-1">
        <p className="text-sm font-medium">{toast.message}</p>
      </div>
      <div className="ml-4 flex-shrink-0">
        <button
          onClick={() => onClose(toast.id)}
          className={`inline-flex rounded-md ${iconColorClass} hover:opacity-75 focus:outline-none focus:ring-2 focus:ring-offset-2`}
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}

interface ToastContainerProps {
  toasts: Toast[];
  onClose: (id: string) => void;
}

export function ToastContainer({ toasts, onClose }: ToastContainerProps) {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 w-full max-w-sm space-y-2">
      {toasts.map((toast) => (
        <ToastComponent key={toast.id} toast={toast} onClose={onClose} />
      ))}
    </div>
  );
}

