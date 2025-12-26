/**
 * Admin Dashboard Analytics Page
 * Redirects to the analytics dashboards
 */

import { redirect } from 'next/navigation';

export default function AdminDashboardPage() {
  redirect('/dashboard/executive');
}


