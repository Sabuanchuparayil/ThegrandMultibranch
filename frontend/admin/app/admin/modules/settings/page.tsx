'use client';

import { Cog6ToothIcon, UserCircleIcon, BellIcon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

const settingSections = [
  { id: 'general', name: 'General Settings', icon: Cog6ToothIcon },
  { id: 'users', name: 'User Management', icon: UserCircleIcon },
  { id: 'notifications', name: 'Notifications', icon: BellIcon },
  { id: 'regions', name: 'Regions & Currencies', icon: GlobeAltIcon },
];

export default function SettingsModule() {
  const [activeSection, setActiveSection] = useState('general');

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">System Settings</h1>
          <p className="text-gray-600 mt-1">Configure system preferences and options</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-4">
              <nav className="space-y-2">
                {settingSections.map((section) => {
                  const Icon = section.icon;
                  return (
                    <button
                      key={section.id}
                      onClick={() => setActiveSection(section.id)}
                      className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${
                        activeSection === section.id
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className="h-5 w-5 mr-3" />
                      {section.name}
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-md p-6">
              {activeSection === 'general' && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">General Settings</h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Site Name</label>
                      <input type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" defaultValue="Grand Gold & Diamonds" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                      <input type="email" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                    </div>
                  </div>
                </div>
              )}

              {activeSection === 'users' && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">User Management</h2>
                  <p className="text-gray-600">Manage system users and permissions</p>
                </div>
              )}

              {activeSection === 'notifications' && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Notification Settings</h2>
                  <p className="text-gray-600">Configure email, SMS, and WhatsApp notifications</p>
                </div>
              )}

              {activeSection === 'regions' && (
                <div>
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Regions & Currencies</h2>
                  <p className="text-gray-600">Manage regions and currency settings</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

