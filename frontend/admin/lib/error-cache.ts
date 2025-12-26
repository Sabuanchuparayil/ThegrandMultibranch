/**
 * Error Cache Mechanism
 * 
 * Caches error states to prevent showing the same error repeatedly
 * and implements retry logic with exponential backoff
 */

interface CachedError {
  timestamp: number;
  error: string;
  retryCount: number;
  lastRetry: number;
}

class ErrorCache {
  private cache: Map<string, CachedError> = new Map();
  private readonly ERROR_TTL = 5 * 60 * 1000; // 5 minutes
  private readonly MAX_RETRIES = 3;
  private readonly RETRY_DELAY_BASE = 1000; // 1 second base delay

  /**
   * Check if an error should be shown based on caching rules
   */
  shouldShowError(queryKey: string, error: Error): boolean {
    const cached = this.cache.get(queryKey);
    const now = Date.now();

    // If no cached error, show it
    if (!cached) {
      this.cache.set(queryKey, {
        timestamp: now,
        error: error.message,
        retryCount: 0,
        lastRetry: now,
      });
      return true;
    }

    // If error is different, show it
    if (cached.error !== error.message) {
      this.cache.set(queryKey, {
        timestamp: now,
        error: error.message,
        retryCount: 0,
        lastRetry: now,
      });
      return true;
    }

    // If error TTL expired, show it again
    if (now - cached.timestamp > this.ERROR_TTL) {
      this.cache.set(queryKey, {
        ...cached,
        timestamp: now,
        retryCount: 0,
      });
      return true;
    }

    // Error is cached and still valid - don't show it
    return false;
  }

  /**
   * Record a retry attempt
   */
  recordRetry(queryKey: string): boolean {
    const cached = this.cache.get(queryKey);
    if (!cached) return false;

    const now = Date.now();
    const timeSinceLastRetry = now - cached.lastRetry;
    const retryDelay = this.RETRY_DELAY_BASE * Math.pow(2, cached.retryCount);

    // Check if enough time has passed for retry
    if (timeSinceLastRetry < retryDelay) {
      return false; // Too soon to retry
    }

    // Check if max retries exceeded
    if (cached.retryCount >= this.MAX_RETRIES) {
      return false; // Max retries exceeded
    }

    // Update retry info
    this.cache.set(queryKey, {
      ...cached,
      retryCount: cached.retryCount + 1,
      lastRetry: now,
    });

    return true;
  }

  /**
   * Clear error cache for a specific query
   */
  clearError(queryKey: string): void {
    this.cache.delete(queryKey);
  }

  /**
   * Clear all error cache
   */
  clearAll(): void {
    this.cache.clear();
  }

  /**
   * Get retry delay for a query
   */
  getRetryDelay(queryKey: string): number {
    const cached = this.cache.get(queryKey);
    if (!cached) return this.RETRY_DELAY_BASE;
    return this.RETRY_DELAY_BASE * Math.pow(2, cached.retryCount);
  }

  /**
   * Check if query should be retried
   */
  shouldRetry(queryKey: string): boolean {
    const cached = this.cache.get(queryKey);
    if (!cached) return true; // First attempt

    if (cached.retryCount >= this.MAX_RETRIES) {
      return false; // Max retries exceeded
    }

    const now = Date.now();
    const timeSinceLastRetry = now - cached.lastRetry;
    const retryDelay = this.getRetryDelay(queryKey);

    return timeSinceLastRetry >= retryDelay;
  }
}

// Singleton instance
export const errorCache = new ErrorCache();

/**
 * Generate a cache key from query name and variables
 */
export function getErrorCacheKey(queryName: string, variables?: Record<string, any>): string {
  const varsKey = variables ? JSON.stringify(variables) : '';
  return `${queryName}:${varsKey}`;
}


