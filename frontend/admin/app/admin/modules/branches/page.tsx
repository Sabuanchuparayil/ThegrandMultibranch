'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, gql } from '@apollo/client';
import { PlusIcon, MagnifyingGlassIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { useToastContext } from '@/components/notifications/ToastProvider';
import { validateBranchForm, type BranchFormData } from '@/lib/validation';
import { CREATE_BRANCH, UPDATE_BRANCH, DELETE_BRANCH } from '@/lib/graphql/mutations';
import { useErrorCache } from '@/hooks/useErrorCache';

const GET_BRANCHES = gql`
  query GetBranches {
    branches {
      id
      name
      code
      region {
        id
        name
        code
      }
      addressLine1
      city
      country
      phone
      email
      isActive
      canShip
      canClickCollect
    }
  }
`;

export default function BranchesModule() {
  const [searchTerm, setSearchTerm] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingBranch, setEditingBranch] = useState<any>(null);

  const { data, loading, error, refetch } = useQuery(GET_BRANCHES, {
    fetchPolicy: 'cache-first',
    errorPolicy: 'all',
    notifyOnNetworkStatusChange: false, // Don't trigger loading on refetch
  });

  // Error caching mechanism
  const { shouldShowError, handleError, clearError } = useErrorCache({
    queryName: 'GetBranches',
    enabled: true,
  });

  // Update error cache when error changes
  // Note: handleError is memoized with useCallback, so it's stable and safe to include
  // However, we only depend on error to avoid unnecessary re-runs
  useEffect(() => {
    if (error) {
      handleError(error as Error);
    } else {
      handleError(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [error]); // Only depend on error, handleError is stable

  // Mock data fallback
  const mockBranches = [
    { id: '1', name: 'London - Mayfair', code: 'LON-001', region: { name: 'United Kingdom', code: 'UK' }, addressLine1: '123 Bond Street', city: 'London', country: 'United Kingdom', phone: '+44 20 7123 4567', email: 'mayfair@grandgold.com', isActive: true, canShip: true, canClickCollect: true },
    { id: '2', name: 'Dubai - Marina', code: 'DXB-001', region: { name: 'United Arab Emirates', code: 'UAE' }, addressLine1: '456 Marina Walk', city: 'Dubai', country: 'United Arab Emirates', phone: '+971 4 123 4567', email: 'marina@grandgold.com', isActive: true, canShip: true, canClickCollect: true },
    { id: '3', name: 'Mumbai - Bandra', code: 'BOM-001', region: { name: 'India', code: 'IN' }, addressLine1: '789 Hill Road', city: 'Mumbai', country: 'India', phone: '+91 22 1234 5678', email: 'bandra@grandgold.com', isActive: true, canShip: true, canClickCollect: false },
  ];

  // Get branches from API or fallback to mock data
  // Only use mock data if there's an error AND we should show it (not cached/suppressed)
  const rawBranches = (error && shouldShowError) || !data?.branches
    ? mockBranches
    : data.branches;

  // #region agent log
  useEffect(() => {
    fetch('http://127.0.0.1:7242/ingest/656e30d1-6cbf-4cc6-b44b-8482a46107f4', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        location: 'branches/page.tsx:BranchesModule:dataSource',
        message: 'Branches list data source',
        data: {
          hypothesisId: 'H13',
          usedMock: Boolean((error && shouldShowError) || !data?.branches),
          apiCount: Array.isArray(data?.branches) ? data.branches.length : null,
          rawCount: Array.isArray(rawBranches) ? rawBranches.length : null,
          hasError: Boolean(error),
          shouldShowError,
          errMsg: (error as any)?.message || null,
        },
        timestamp: Date.now(),
        sessionId: 'debug-session',
        runId: 'run1',
        hypothesisId: 'H13',
      }),
    }).catch(() => {});
  }, [error, shouldShowError, data?.branches?.length]);
  // #endregion

  // Apply client-side filtering to both API and mock data
  const branches = rawBranches.filter((branch: any) => {
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const name = branch.name?.toLowerCase() || '';
      const code = branch.code?.toLowerCase() || '';
      if (!name.includes(searchLower) && !code.includes(searchLower)) {
        return false;
      }
    }
    return true;
  });

  const handleEdit = (branch: any) => {
    setEditingBranch(branch);
    setShowForm(true);
  };

  const [deleteBranch] = useMutation(DELETE_BRANCH, {
    refetchQueries: [{ query: GET_BRANCHES }],
  });
  const toast = useToastContext();

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this branch?')) {
      try {
        const { data } = await deleteBranch({ variables: { id } });
        if (data?.branchDelete?.success) {
          toast.success('Branch deleted successfully');
          refetch();
        } else {
          const errors = data?.branchDelete?.errors || [];
          toast.error(errors.length > 0 ? errors[0].message : 'Failed to delete branch');
        }
      } catch (error: any) {
        toast.error(error.message || 'Failed to delete branch');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Error Banner - Only show if error is not cached/suppressed */}
        {error && shouldShowError && (
          <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm text-yellow-700">
                  <strong>Backend connection error:</strong> Unable to load branches from the API. Showing sample data for demonstration purposes.
                  <br />
                  <span className="text-xs text-yellow-600 mt-1 block font-mono">
                    Error: {error.message || 'Failed to fetch'}
                    {error.networkError && (
                      <span className="block mt-1">
                        Network: {error.networkError.message || 'Unknown network error'}
                        {'statusCode' in error.networkError && (
                          <span className="block">Status: {error.networkError.statusCode}</span>
                        )}
                      </span>
                    )}
                    {process.env.NODE_ENV === 'development' && (
                      <span className="block mt-1 text-xs opacity-75">
                        Check browser console for full error details
                      </span>
                    )}
                  </span>
                </p>
                <button
                  onClick={clearError}
                  className="mt-2 text-xs text-yellow-800 underline hover:text-yellow-900"
                >
                  Dismiss (errors will be cached for 5 minutes)
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Branch Management</h1>
            <p className="text-gray-600 mt-1">Manage store locations and branches</p>
          </div>
          <button
            onClick={() => {
              setEditingBranch(null);
              setShowForm(true);
            }}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Branch
          </button>
        </div>

        {/* Search */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search branches..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Branch
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Region
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Capabilities
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {loading ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-4 text-center text-gray-500">
                      Loading...
                    </td>
                  </tr>
                ) : branches.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-4 text-center text-gray-500">
                      No branches found
                    </td>
                  </tr>
                ) : (
                  branches.map((branch: any) => (
                    <tr key={branch.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{branch.name}</div>
                        <div className="text-sm text-gray-500">Code: {branch.code}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {branch.region?.name || 'N/A'}
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900">{branch.addressLine1}</div>
                        <div className="text-sm text-gray-500">
                          {branch.city}, {branch.country}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{branch.phone}</div>
                        <div className="text-sm text-gray-500">{branch.email}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex flex-wrap gap-1">
                          {branch.canShip && (
                            <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                              Ship
                            </span>
                          )}
                          {branch.canClickCollect && (
                            <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                              C&C
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {branch.isActive ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            Active
                          </span>
                        ) : (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                            Inactive
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleEdit(branch)}
                          className="text-blue-600 hover:text-blue-900 mr-4"
                        >
                          <PencilIcon className="h-5 w-5 inline" />
                        </button>
                        <button
                          onClick={() => handleDelete(branch.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <TrashIcon className="h-5 w-5 inline" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Form Modal */}
        {showForm && (
          <BranchFormModal
            branch={editingBranch}
            onClose={() => {
              setShowForm(false);
              setEditingBranch(null);
            }}
            onSuccess={() => {
              refetch();
              setShowForm(false);
            }}
          />
        )}
      </div>
    </div>
  );
}

// Branch Form Component
function BranchFormModal({ branch, onClose, onSuccess }: any) {
  const [formData, setFormData] = useState<BranchFormData>({
    name: branch?.name || '',
    code: branch?.code || '',
    regionId: branch?.region?.id || '',
    addressLine1: branch?.addressLine1 || '',
    addressLine2: branch?.addressLine2 || '',
    city: branch?.city || '',
    state: branch?.state || '',
    postalCode: branch?.postalCode || '',
    country: branch?.country || '',
    phone: branch?.phone || '',
    email: branch?.email || '',
    canShip: branch?.canShip ?? true,
    canClickCollect: branch?.canClickCollect ?? true,
    isActive: branch?.isActive ?? true,
  });

  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const toast = useToastContext();

  const [createBranch] = useMutation(CREATE_BRANCH, {
    refetchQueries: [{ query: GET_BRANCHES }],
  });

  const [updateBranch] = useMutation(UPDATE_BRANCH, {
    refetchQueries: [{ query: GET_BRANCHES }],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationErrors({});

    // Client-side validation
    const validation = validateBranchForm(formData);
    if (!validation.isValid) {
      const errors: Record<string, string> = {};
      validation.errors.forEach((err) => {
        errors[err.field] = err.message;
      });
      setValidationErrors(errors);
      toast.error('Please fix the form errors before submitting');
      return;
    }

    setIsSubmitting(true);

    try {
      const input = {
        name: formData.name.trim(),
        code: formData.code.trim(),
        regionId: formData.regionId,
        addressLine1: formData.addressLine1.trim(),
        addressLine2: formData.addressLine2?.trim() || '',
        city: formData.city.trim(),
        state: formData.state?.trim() || '',
        postalCode: formData.postalCode.trim(),
        country: formData.country.trim(),
        phone: formData.phone.trim(),
        email: formData.email.trim(),
        canShip: formData.canShip,
        canClickCollect: formData.canClickCollect,
        isActive: formData.isActive,
      };

      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/656e30d1-6cbf-4cc6-b44b-8482a46107f4', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location: 'branches/page.tsx:BranchFormModal:handleSubmit:input',
          message: 'Branch submit input snapshot (redacted)',
          data: {
            hypothesisId: 'H4',
            mode: branch ? 'update' : 'create',
            regionId: input.regionId,
            code: input.code,
          },
          timestamp: Date.now(),
          sessionId: 'debug-session',
          runId: 'run1',
          hypothesisId: 'H4',
        }),
      }).catch(() => {});
      // #endregion

      if (branch) {
        // Update existing branch
        const { data } = await updateBranch({
          variables: {
            id: branch.id,
            input,
          },
        });

        if (data?.branchUpdate?.branch) {
          toast.success('Branch updated successfully');
          onSuccess();
        } else {
          const errors = data?.branchUpdate?.errors || [];
          if (errors.length > 0) {
            const fieldErrors: Record<string, string> = {};
            errors.forEach((err: any) => {
              fieldErrors[err.field] = err.message;
            });
            setValidationErrors(fieldErrors);
            toast.error('Failed to update branch. Please check the errors.');
          } else {
            toast.error('Failed to update branch');
          }
        }
      } else {
        // Create new branch
        const { data } = await createBranch({
          variables: { input },
        });

        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/656e30d1-6cbf-4cc6-b44b-8482a46107f4', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            location: 'branches/page.tsx:BranchFormModal:handleSubmit:result',
            message: 'Branch create result snapshot',
            data: {
              hypothesisId: 'H4',
              hasBranch: Boolean((data as any)?.branchCreate?.branch?.id),
              errorCount: ((data as any)?.branchCreate?.errors || []).length,
              firstError: ((data as any)?.branchCreate?.errors || [])[0]?.message,
            },
            timestamp: Date.now(),
            sessionId: 'debug-session',
            runId: 'run1',
            hypothesisId: 'H4',
          }),
        }).catch(() => {});
        // #endregion

        if (data?.branchCreate?.branch) {
          toast.success('Branch created successfully');
          onSuccess();
        } else {
          const errors = data?.branchCreate?.errors || [];
          if (errors.length > 0) {
            const fieldErrors: Record<string, string> = {};
            errors.forEach((err: any) => {
              fieldErrors[err.field] = err.message;
            });
            setValidationErrors(fieldErrors);
            toast.error('Failed to create branch. Please check the errors.');
          } else {
            toast.error('Failed to create branch');
          }
        }
      }
    } catch (error: any) {
      console.error('Branch mutation error:', error);
      toast.error(error.message || `Failed to ${branch ? 'update' : 'create'} branch`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">
            {branch ? 'Edit Branch' : 'Add New Branch'}
          </h2>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Branch Name *
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => {
                  setFormData({ ...formData, name: e.target.value });
                  if (validationErrors.name) {
                    setValidationErrors({ ...validationErrors, name: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.name ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.name && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.name}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Branch Code *
              </label>
              <input
                type="text"
                required
                value={formData.code}
                onChange={(e) => {
                  setFormData({ ...formData, code: e.target.value });
                  if (validationErrors.code) {
                    setValidationErrors({ ...validationErrors, code: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.code ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.code && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.code}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Region *
              </label>
              <select
                required
                value={formData.regionId}
                onChange={(e) => {
                  setFormData({ ...formData, regionId: e.target.value });
                  if (validationErrors.regionId) {
                    setValidationErrors({ ...validationErrors, regionId: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.regionId ? 'border-red-500' : 'border-gray-300'
                }`}
              >
                <option value="">Select Region</option>
                <option value="1">United Kingdom</option>
                <option value="2">United Arab Emirates</option>
                <option value="3">India</option>
              </select>
              {validationErrors.regionId && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.regionId}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Country *</label>
              <input
                type="text"
                required
                value={formData.country}
                onChange={(e) => {
                  setFormData({ ...formData, country: e.target.value });
                  if (validationErrors.country) {
                    setValidationErrors({ ...validationErrors, country: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.country ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.country && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.country}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Address Line 1 *
              </label>
              <input
                type="text"
                required
                value={formData.addressLine1}
                onChange={(e) => {
                  setFormData({ ...formData, addressLine1: e.target.value });
                  if (validationErrors.addressLine1) {
                    setValidationErrors({ ...validationErrors, addressLine1: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.addressLine1 ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.addressLine1 && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.addressLine1}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Address Line 2
              </label>
              <input
                type="text"
                value={formData.addressLine2}
                onChange={(e) => setFormData({ ...formData, addressLine2: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City *</label>
              <input
                type="text"
                required
                value={formData.city}
                onChange={(e) => {
                  setFormData({ ...formData, city: e.target.value });
                  if (validationErrors.city) {
                    setValidationErrors({ ...validationErrors, city: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.city ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.city && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.city}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <input
                type="text"
                value={formData.state}
                onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Postal Code *
              </label>
              <input
                type="text"
                required
                value={formData.postalCode}
                onChange={(e) => {
                  setFormData({ ...formData, postalCode: e.target.value });
                  if (validationErrors.postalCode) {
                    setValidationErrors({ ...validationErrors, postalCode: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.postalCode ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.postalCode && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.postalCode}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone *</label>
              <input
                type="tel"
                required
                value={formData.phone}
                onChange={(e) => {
                  setFormData({ ...formData, phone: e.target.value });
                  if (validationErrors.phone) {
                    setValidationErrors({ ...validationErrors, phone: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.phone ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.phone && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.phone}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => {
                  setFormData({ ...formData, email: e.target.value });
                  if (validationErrors.email) {
                    setValidationErrors({ ...validationErrors, email: '' });
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  validationErrors.email ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {validationErrors.email && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.canShip}
                onChange={(e) => setFormData({ ...formData, canShip: e.target.checked })}
                className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">Can Ship</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.canClickCollect}
                onChange={(e) => setFormData({ ...formData, canClickCollect: e.target.checked })}
                className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">Click & Collect</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.isActive}
                onChange={(e) => setFormData({ ...formData, isActive: e.target.checked })}
                className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">Active</span>
            </label>
          </div>
          <div className="flex justify-end space-x-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {branch ? 'Updating...' : 'Creating...'}
                </>
              ) : (
                `${branch ? 'Update' : 'Create'} Branch`
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

