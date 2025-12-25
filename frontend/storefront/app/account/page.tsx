'use client';

import { useQuery, gql } from '@apollo/client';
import Link from 'next/link';

const GET_USER_PROFILE = gql`
  query GetUserProfile {
    me {
      id
      email
      firstName
      lastName
      dateJoined
      isActive
    }
  }
`;

export default function AccountOverviewPage() {
  const { data, loading, error } = useQuery(GET_USER_PROFILE, {
    fetchPolicy: 'cache-first',
  });

  const user = data?.me;

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Account Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="border border-gray-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h2>
          <dl className="space-y-3">
            <div>
              <dt className="text-sm text-gray-500">Name</dt>
              <dd className="text-gray-900 font-medium">
                {user?.firstName} {user?.lastName}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Email</dt>
              <dd className="text-gray-900">{user?.email}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Member Since</dt>
              <dd className="text-gray-900">
                {user?.dateJoined
                  ? new Date(user.dateJoined).toLocaleDateString()
                  : 'N/A'}
              </dd>
            </div>
          </dl>
          <Link
            href="/account/settings"
            className="mt-4 inline-block text-yellow-600 hover:text-yellow-700 text-sm font-medium"
          >
            Edit Profile →
          </Link>
        </div>

        <div className="border border-gray-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link
              href="/account/orders"
              className="block p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              <div className="font-medium text-gray-900">View Orders</div>
              <div className="text-sm text-gray-500">Track your order history</div>
            </Link>
            <Link
              href="/account/wishlist"
              className="block p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              <div className="font-medium text-gray-900">Wishlist</div>
              <div className="text-sm text-gray-500">View saved items</div>
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Orders */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recent Orders</h2>
          <Link href="/account/orders" className="text-yellow-600 hover:text-yellow-700 text-sm font-medium">
            View All →
          </Link>
        </div>
        <div className="border border-gray-200 rounded-lg p-4 text-center text-gray-500">
          <p>No recent orders</p>
        </div>
      </div>
    </div>
  );
}

