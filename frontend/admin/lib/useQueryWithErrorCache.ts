'use client';

import { useEffect } from 'react';
import { QueryResult, OperationVariables, DocumentNode } from '@apollo/client';
import { useQuery } from '@apollo/client';
import { useErrorCache } from '@/hooks/useErrorCache';

interface UseQueryWithErrorCacheOptions<TData = any, TVariables = OperationVariables> {
  query: DocumentNode;
  queryName: string;
  variables?: TVariables;
  options?: Parameters<typeof useQuery<TData, TVariables>>[1];
  enabled?: boolean; // Whether to show errors (default: true)
}

/**
 * Wrapper around useQuery that implements error caching
 * Prevents showing the same error repeatedly within a time window
 */
export function useQueryWithErrorCache<TData = any, TVariables = OperationVariables>({
  query,
  queryName,
  variables,
  options = {},
  enabled = true,
}: UseQueryWithErrorCacheOptions<TData, TVariables>) {
  const queryResult = useQuery<TData, TVariables>(query, {
    fetchPolicy: 'cache-first',
    errorPolicy: 'all',
    notifyOnNetworkStatusChange: false,
    ...options,
    variables: variables as TVariables,
  });

  const { shouldShowError, handleError, clearError } = useErrorCache({
    queryName,
    variables: variables as Record<string, any>,
    enabled,
  });

  // Update error cache when error changes
  useEffect(() => {
    if (queryResult.error) {
      handleError(queryResult.error as Error);
    } else {
      handleError(null);
    }
  }, [queryResult.error, handleError]);

  return {
    ...queryResult,
    shouldShowError,
    clearError,
  };
}

