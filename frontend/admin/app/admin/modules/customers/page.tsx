'use client';

import { useState } from 'react';
import { useQuery, gql } from '@apollo/client';
import { MagnifyingGlassIcon, EyeIcon, PencilIcon } from '@heroicons/react/24/outline';

const GET_CUSTOMERS = gql`
  query GetCustomers($first: Int, $filter: CustomerFilterInput) {
    users(first: $first, filter: $filter) {
      edges {
        node {
          id
          email
          firstName
          lastName
          isActive
          dateJoined
        }
      }
    }
  }
`;

export default function CustomersModule() {
  const [searchTerm, setSearchTerm] = useState('');

  const { data, loading, error } = useQuery(GET_CUSTOMERS, {
    variables: {
      first: 50,
      filter: { search: searchTerm || null },
    },
    fetchPolicy: 'cache-and-network',
    errorPolicy: 'all',
  });

  // Mock data fallback
  const mockCustomers = [
    { id: '1', email: 'john.doe@example.com', firstName: 'John', lastName: 'Doe', isActive: true, dateJoined: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000).toISOString() },
    { id: '2', email: 'jane.smith@example.com', firstName: 'Jane', lastName: 'Smith', isActive: true, dateJoined: new Date(Date.now() - 180 * 24 * 60 * 60 * 1000).toISOString() },
    { id: '3', email: 'mike.johnson@example.com', firstName: 'Mike', lastName: 'Johnson', isActive: false, dateJoined: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString() },
  ];

  // Get customers from API or fallback to mock data
  const rawCustomers = error || !data?.users?.edges
    ? mockCustomers
    : data.users.edges.map((edge: any) => edge.node);

  // Apply client-side filtering to both API and mock data
  const customers = rawCustomers.filter((customer: any) => {
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const email = customer.email?.toLowerCase() || '';
      const firstName = customer.firstName?.toLowerCase() || '';
      const lastName = customer.lastName?.toLowerCase() || '';
      const fullName = `${firstName} ${lastName}`.trim();
      if (!email.includes(searchLower) && !fullName.includes(searchLower)) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  <strong>Backend connection error:</strong> Unable to load customers from the API. Showing sample data for demonstration purposes.
                  {error.message && <span className="block mt-1 text-xs">Error: {error.message}</span>}
                </p>
              </div>
            </div>
          </div>
        )}
        
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Customer Management</h1>
          <p className="text-gray-600 mt-1">Manage customer accounts and profiles</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search customers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Member Since</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {loading ? (
                  <tr><td colSpan={5} className="px-6 py-4 text-center text-gray-500">Loading...</td></tr>
                ) : customers.length === 0 ? (
                  <tr><td colSpan={5} className="px-6 py-4 text-center text-gray-500">No customers found</td></tr>
                ) : (
                  customers.map((customer: any) => (
                    <tr key={customer.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        {customer.firstName} {customer.lastName}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{customer.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(customer.dateJoined).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs rounded-full ${customer.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                          {customer.isActive ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <button
                          onClick={() => {
                            // TODO: Open customer detail modal or navigate to detail page
                            console.log('View customer:', customer.id);
                          }}
                          className="text-blue-600 hover:text-blue-900 mr-4"
                        >
                          <EyeIcon className="h-5 w-5 inline" />
                        </button>
                        <button
                          onClick={() => {
                            // TODO: Open customer edit modal
                            console.log('Edit customer:', customer.id);
                          }}
                          className="text-gray-600 hover:text-gray-900"
                        >
                          <PencilIcon className="h-5 w-5 inline" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

