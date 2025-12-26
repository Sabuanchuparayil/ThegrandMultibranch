import { ApolloClient, InMemoryCache, createHttpLink, from, type FetchPolicy, type WatchQueryFetchPolicy } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

// #region agent log
const _debugLog = (location: string, message: string, data: Record<string, any>, hypothesisId: string) => {
  try {
    fetch('http://127.0.0.1:7242/ingest/656e30d1-6cbf-4cc6-b44b-8482a46107f4', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        location,
        message,
        data: { ...data, hypothesisId },
        timestamp: Date.now(),
        sessionId: 'debug-session',
        runId: 'run1',
        hypothesisId,
      }),
    }).catch(() => {});
  } catch {
    // ignore
  }
};
// #endregion

// Get GraphQL URL from environment or use Railway backend URL
const getGraphQLUrl = () => {
  // Priority: Environment variable > Railway backend URL > localhost
  // IMPORTANT: Set NEXT_PUBLIC_GRAPHQL_URL in Railway environment variables
  // to avoid needing to rebuild when backend URL changes
  let url: string;
  if (process.env.NEXT_PUBLIC_GRAPHQL_URL) {
    url = process.env.NEXT_PUBLIC_GRAPHQL_URL;
  } else if (typeof window !== 'undefined') {
    // In browser, use the Railway backend URL
    // This will be used if NEXT_PUBLIC_GRAPHQL_URL is not set
    url = 'https://backend-production-fb5f.up.railway.app/graphql/';
  } else {
    // Server-side fallback
    url = 'http://localhost:8000/graphql/';
  }
  
  // #region agent log
  if (typeof window !== 'undefined') {
    _debugLog(
      'apollo-client.ts:getGraphQLUrl',
      'GraphQL URL resolved',
      {
        url,
        hasEnvVar: !!process.env.NEXT_PUBLIC_GRAPHQL_URL,
        envVar: process.env.NEXT_PUBLIC_GRAPHQL_URL || 'not set',
        isBrowser: typeof window !== 'undefined',
      },
      'H1'
    );
  }
  // #endregion
  
  return url;
};

const graphqlUrl = getGraphQLUrl();
const httpLink = createHttpLink({
  uri: graphqlUrl,
  credentials: 'include', // Include cookies for CORS
});

// #region agent log
// Log HTTP link configuration
if (typeof window !== 'undefined') {
  _debugLog(
    'apollo-client.ts:httpLink',
    'HTTP link created',
    {
      uri: graphqlUrl,
      hasCredentials: true,
      credentialsValue: 'include',
    },
    'H1'
  );
}
// #endregion

// Auth link to add authentication tokens
const authLink = setContext((_, { headers }) => {
  // Get the authentication token from local storage or environment variable
  let token: string | null = null;
  
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('authToken');
  }
  
  // Fallback to environment variable if localStorage is empty
  if (!token && process.env.NEXT_PUBLIC_AUTH_TOKEN) {
    token = process.env.NEXT_PUBLIC_AUTH_TOKEN;
  }
  
  // Only use token if it's a non-empty string
  const authHeader = token && token.trim() !== '' 
    ? `Bearer ${token}` 
    : '';
  
  return {
    headers: {
      ...headers,
      authorization: authHeader,
    },
  };
});

// Error link for handling GraphQL errors
// Note: Retry logic is handled by Apollo Client's built-in retry mechanism
// and our error cache system prevents showing the same error repeatedly
const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (graphQLErrors) {
    // #region agent log
    _debugLog(
      'apollo-client.ts:errorLink:graphQLErrors',
      'Apollo GraphQL errors',
      {
        operationName: operation?.operationName,
        url: operation?.getContext()?.uri || 'unknown',
        errorMessages: graphQLErrors.map((e) => e.message).slice(0, 5),
        variablesKeys: Object.keys(operation?.variables || {}),
      },
      'H2'
    );
    // #endregion

    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      );
    });
  }

  if (networkError) {
    // #region agent log
    // Capture comprehensive network error details
    const networkErrorDetails = {
      // Basic error info
      name: networkError.name || 'NetworkError',
      message: networkError.message || 'Network error',
      
      // Status code (if available)
      statusCode: 'statusCode' in networkError ? (networkError as any).statusCode : null,
      
      // Operation context
      operationName: operation?.operationName || 'unknown',
      operationContext: operation?.getContext() || {},
      
      // URL information
      urlFromContext: operation?.getContext()?.uri || null,
      urlFromHttpLink: getGraphQLUrl(),
      
      // Error object properties
      errorKeys: Object.keys(networkError),
      errorString: String(networkError),
      errorType: networkError.constructor?.name || typeof networkError,
      
      // Additional error properties
      cause: 'cause' in networkError ? (networkError as any).cause : null,
      stack: networkError.stack || null,
      
      // Request details
      variablesKeys: Object.keys(operation?.variables || {}),
      hasAuthToken: typeof window !== 'undefined' ? !!localStorage.getItem('authToken') : false,
    };
    
    _debugLog(
      'apollo-client.ts:errorLink:networkError',
      'Apollo network error - detailed analysis',
      networkErrorDetails,
      'H1'
    );
    
    // Also log to console with full error object
    console.error('[Network error - Full Details]:', {
      error: networkError,
      ...networkErrorDetails,
    });
    // #endregion

    // Log network errors with full details for debugging
    const errorMessage = networkError.message || 'Network error';
    const errorStatus = 'statusCode' in networkError ? networkError.statusCode : 'unknown';
    const errorName = networkError.name || 'NetworkError';
    
    // Always log network errors with full context for debugging
    console.error(`[Network error]: ${errorName} - ${errorMessage}`, {
      statusCode: errorStatus,
      operation: operation?.operationName,
      variables: operation?.variables,
      url: networkErrorDetails.urlFromContext || networkErrorDetails.urlFromHttpLink || 'unknown',
      fullError: networkError,
    });
    
    // Handle 401 unauthorized errors
    if ('statusCode' in networkError && networkError.statusCode === 401) {
      // Redirect to login or clear token
      if (typeof window !== 'undefined') {
        localStorage.removeItem('authToken');
        // Only redirect if not already on login page
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }
  }
});

// Create Apollo Client
// #region agent log
// Type-safe default options configuration
// Using explicit type assertions to ensure TypeScript recognizes the literal types
const defaultOptionsConfig: {
  watchQuery: {
    errorPolicy: 'all';
    fetchPolicy: WatchQueryFetchPolicy;
    nextFetchPolicy: WatchQueryFetchPolicy;
  };
  query: {
    errorPolicy: 'all';
    fetchPolicy: FetchPolicy;
  };
} = {
  watchQuery: {
    errorPolicy: 'all',
    fetchPolicy: 'cache-first' as WatchQueryFetchPolicy,
    nextFetchPolicy: 'cache-first' as WatchQueryFetchPolicy,
  },
  query: {
    errorPolicy: 'all',
    fetchPolicy: 'cache-first' as FetchPolicy,
  },
};
// #endregion

export const apolloClient = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          // Add field policies for caching strategies
        },
      },
    },
  }),
  defaultOptions: defaultOptionsConfig,
  // DevTools configuration (Apollo Client 3.14+ uses devtools.enabled instead of connectToDevTools)
  ...(process.env.NODE_ENV === 'development' ? { devtools: { enabled: true } } : {}),
});

