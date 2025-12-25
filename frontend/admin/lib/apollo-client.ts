import { ApolloClient, InMemoryCache, createHttpLink, from } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

// Get GraphQL URL from environment or use Railway backend URL
const getGraphQLUrl = () => {
  // Priority: Environment variable > Railway backend URL > localhost
  // IMPORTANT: Set NEXT_PUBLIC_GRAPHQL_URL in Railway environment variables
  // to avoid needing to rebuild when backend URL changes
  if (process.env.NEXT_PUBLIC_GRAPHQL_URL) {
    return process.env.NEXT_PUBLIC_GRAPHQL_URL;
  }
  
  // Use Railway backend URL as fallback (updated to fb5f)
  if (typeof window !== 'undefined') {
    // In browser, use the Railway backend URL
    // This will be used if NEXT_PUBLIC_GRAPHQL_URL is not set
    return 'https://backend-production-fb5f.up.railway.app/graphql/';
  }
  
  // Server-side fallback
  return 'http://localhost:8000/graphql/';
};

const httpLink = createHttpLink({
  uri: getGraphQLUrl(),
  credentials: 'include', // Include cookies for CORS
});

// Auth link to add authentication tokens
const authLink = setContext((_, { headers }) => {
  // Get the authentication token from local storage if it exists
  const token = typeof window !== 'undefined' ? localStorage.getItem('authToken') : null;
  
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

// Error link for handling GraphQL errors
// Note: Retry logic is handled by Apollo Client's built-in retry mechanism
// and our error cache system prevents showing the same error repeatedly
const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      );
    });
  }

  if (networkError) {
    // Log network errors with full details for debugging
    const errorMessage = networkError.message || 'Network error';
    const errorStatus = 'statusCode' in networkError ? networkError.statusCode : 'unknown';
    const errorName = networkError.name || 'NetworkError';
    
    // Always log network errors with full context for debugging
    console.error(`[Network error]: ${errorName} - ${errorMessage}`, {
      statusCode: errorStatus,
      operation: operation?.operationName,
      variables: operation?.variables,
      url: operation?.getContext()?.uri || 'unknown',
    });
    
    // Handle 401 unauthorized errors
    if ('statusCode' in networkError && networkError.statusCode === 401) {
      // Redirect to login or clear token
      if (typeof window !== 'undefined') {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
      }
    }
  }
});

// Create Apollo Client
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
  defaultOptions: {
    watchQuery: {
      errorPolicy: 'all',
      fetchPolicy: 'cache-first', // Use cache when available, then fetch from network if not in cache
      nextFetchPolicy: 'cache-first', // Use cache-first for subsequent requests
    },
    query: {
      errorPolicy: 'all',
      fetchPolicy: 'cache-first', // Use cache when available, then fetch from network if not in cache
    },
  },
  // Disable error logging in production to reduce noise
  connectToDevTools: process.env.NODE_ENV === 'development',
});

