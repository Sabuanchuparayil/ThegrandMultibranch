'use client';

import { useEffect, useState, useRef } from 'react';
import { errorCache, getErrorCacheKey } from '@/lib/error-cache';

interface UseErrorCacheOptions {
  queryName: string;
  variables?: Record<string, any>;
  enabled?: boolean; // Whether to show errors (default: true)
}

/**
 * Hook to manage error caching and display
 * Prevents showing the same error repeatedly within a time window
 */
export function useErrorCache({ queryName, variables, enabled = true }: UseErrorCacheOptions) {
  const [shouldShowError, setShouldShowError] = useState(false);
  const [cachedError, setCachedError] = useState<Error | null>(null);
  const errorRef = useRef<Error | null>(null);
  const cacheKey = getErrorCacheKey(queryName, variables);

  useEffect(() => {
    // Clear error state when query name or variables change
    setShouldShowError(false);
    setCachedError(null);
    errorRef.current = null;
  }, [queryName, JSON.stringify(variables)]);

  const handleError = (error: Error | null) => {
    if (!error) {
      // Clear error cache on success
      errorCache.clearError(cacheKey);
      setShouldShowError(false);
      setCachedError(null);
      errorRef.current = null;
      return;
    }

    errorRef.current = error;

    if (!enabled) {
      setShouldShowError(false);
      return;
    }

    // Check if error should be shown based on cache
    const show = errorCache.shouldShowError(cacheKey, error);
    setShouldShowError(show);
    setCachedError(show ? error : null);
  };

  const clearError = () => {
    errorCache.clearError(cacheKey);
    setShouldShowError(false);
    setCachedError(null);
    errorRef.current = null;
  };

  return {
    shouldShowError,
    cachedError,
    handleError,
    clearError,
    currentError: errorRef.current,
  };
}

