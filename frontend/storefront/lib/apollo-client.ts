import { ApolloClient, InMemoryCache, createHttpLink, from } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';

// Get GraphQL URL from environment variable
// In production, this must be set in Railway environment variables
const getGraphQLUrl = () => {
  const url = process.env.NEXT_PUBLIC_GRAPHQL_URL;
  if (!url) {
    if (process.env.NODE_ENV === 'production') {
      console.error('NEXT_PUBLIC_GRAPHQL_URL is not set! Please configure it in Railway environment variables.');
      // Return a placeholder that will fail gracefully
      return 'https://backend-production-d769.up.railway.app/graphql/';
    }
    // Development fallback
    return 'http://localhost:8000/graphql/';
  }
  return url;
};

const httpLink = createHttpLink({
  uri: getGraphQLUrl(),
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
const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      );
    });
  }

  if (networkError) {
    console.error(`[Network error]: ${networkError}`);
    
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
    },
    query: {
      errorPolicy: 'all',
    },
  },
});

