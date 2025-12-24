'use client';

import { useEffect, useState, useRef, useCallback, useMemo } from 'react';
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
  const dismissedRef = useRef<boolean>(false); // Track if error was manually dismissed
  const cacheKey = useMemo(() => getErrorCacheKey(queryName, variables), [queryName, variables]);

  useEffect(() => {
    // Clear error state when query name or variables change
    setShouldShowError(false);
    setCachedError(null);
    errorRef.current = null;
    dismissedRef.current = false; // Reset dismissed state on query change
  }, [cacheKey]);

  const handleError = useCallback((error: Error | null) => {
    if (!error) {
      // Clear error cache on success
      errorCache.clearError(cacheKey);
      setShouldShowError(false);
      setCachedError(null);
      errorRef.current = null;
      dismissedRef.current = false; // Reset dismissed state on success
      return;
    }

    // If error was manually dismissed, don't re-show it
    if (dismissedRef.current) {
      setShouldShowError(false);
      setCachedError(null);
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
  }, [cacheKey, enabled]);

  const clearError = useCallback(() => {
    errorCache.clearError(cacheKey);
    setShouldShowError(false);
    setCachedError(null);
    errorRef.current = null;
    dismissedRef.current = true; // Mark as dismissed to prevent re-showing
  }, [cacheKey]);

  return {
    shouldShowError,
    cachedError,
    handleError,
    clearError,
    currentError: errorRef.current,
  };
}

