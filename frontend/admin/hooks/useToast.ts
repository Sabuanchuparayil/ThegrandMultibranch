'use client';

import { useState, useCallback } from 'react';
import { Toast, ToastType } from '@/components/notifications/Toast';

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((type: ToastType, message: string, duration: number = 5000) => {
    const id = Math.random().toString(36).substring(2, 9);
    const newToast: Toast = { id, type, message, duration };
    setToasts((prev) => [...prev, newToast]);
    return id;
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const success = useCallback((message: string, duration?: number) => {
    return showToast('success', message, duration);
  }, [showToast]);

  const error = useCallback((message: string, duration?: number) => {
    return showToast('error', message, duration);
  }, [showToast]);

  const info = useCallback((message: string, duration?: number) => {
    return showToast('info', message, duration);
  }, [showToast]);

  const warning = useCallback((message: string, duration?: number) => {
    return showToast('warning', message, duration);
  }, [showToast]);

  return {
    toasts,
    showToast,
    removeToast,
    success,
    error,
    info,
    warning,
  };
}


