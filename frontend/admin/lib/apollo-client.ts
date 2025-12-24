import { ApolloClient, InMemoryCache, createHttpLink, from } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

// Get GraphQL URL from environment or use Railway backend URL
const getGraphQLUrl = () => {
  // Priority: Environment variable > Railway backend URL > localhost
  if (process.env.NEXT_PUBLIC_GRAPHQL_URL) {
    return process.env.NEXT_PUBLIC_GRAPHQL_URL;
  }
  
  // Use Railway backend URL as fallback
  if (typeof window !== 'undefined') {
    // In browser, use the Railway backend URL
    return 'https://backend-production-d769.up.railway.app/graphql/';
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
    // Log network errors but don't spam console
    const errorMessage = networkError.message || 'Network error';
    
    // Only log if it's not a CORS error (which we expect during development)
    if (!errorMessage.includes('CORS') && !errorMessage.includes('Failed to fetch')) {
      console.error(`[Network error]: ${errorMessage}`);
    }
    
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
      fetchPolicy: 'cache-and-network', // Use cache when available, but always try network
    },
    query: {
      errorPolicy: 'all',
      fetchPolicy: 'cache-and-network',
    },
  },
  // Disable error logging in production to reduce noise
  connectToDevTools: process.env.NODE_ENV === 'development',
});

