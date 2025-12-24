/**
 * Dashboard Index Page
 * Redirects to executive dashboard by default
 */

import { redirect } from 'next/navigation';

export default function DashboardPage() {
  redirect('/dashboard/executive');
}
