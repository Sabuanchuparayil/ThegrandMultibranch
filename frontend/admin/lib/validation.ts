/**
 * Form validation utilities
 */

export interface ValidationError {
  field: string;
  message: string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
}

/**
 * Validate email format
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate phone number (basic validation - allows international formats)
 */
export function validatePhone(phone: string): boolean {
  // Allow international formats: +, digits, spaces, dashes, parentheses
  const phoneRegex = /^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
}

/**
 * Validate postal code (basic validation)
 */
export function validatePostalCode(postalCode: string): boolean {
  // Allow alphanumeric with spaces and dashes
  const postalRegex = /^[A-Z0-9\s\-]{3,10}$/i;
  return postalRegex.test(postalCode);
}

/**
 * Validate branch form data
 */
export interface BranchFormData {
  name: string;
  code: string;
  regionId: string;
  addressLine1: string;
  addressLine2?: string;
  city: string;
  state?: string;
  postalCode: string;
  country: string;
  phone: string;
  email: string;
  canShip: boolean;
  canClickCollect: boolean;
  isActive: boolean;
}

export function validateBranchForm(data: BranchFormData): ValidationResult {
  const errors: ValidationError[] = [];

  // Required fields
  if (!data.name || data.name.trim().length === 0) {
    errors.push({ field: 'name', message: 'Branch name is required' });
  } else if (data.name.trim().length < 3) {
    errors.push({ field: 'name', message: 'Branch name must be at least 3 characters' });
  }

  if (!data.code || data.code.trim().length === 0) {
    errors.push({ field: 'code', message: 'Branch code is required' });
  } else if (!/^[A-Z0-9\-]{3,20}$/i.test(data.code.trim())) {
    errors.push({ field: 'code', message: 'Branch code must be 3-20 alphanumeric characters (hyphens allowed)' });
  }

  if (!data.regionId || data.regionId.trim().length === 0) {
    errors.push({ field: 'regionId', message: 'Region is required' });
  }

  if (!data.addressLine1 || data.addressLine1.trim().length === 0) {
    errors.push({ field: 'addressLine1', message: 'Address line 1 is required' });
  }

  if (!data.city || data.city.trim().length === 0) {
    errors.push({ field: 'city', message: 'City is required' });
  }

  if (!data.postalCode || data.postalCode.trim().length === 0) {
    errors.push({ field: 'postalCode', message: 'Postal code is required' });
  } else if (!validatePostalCode(data.postalCode)) {
    errors.push({ field: 'postalCode', message: 'Please enter a valid postal code' });
  }

  if (!data.country || data.country.trim().length === 0) {
    errors.push({ field: 'country', message: 'Country is required' });
  }

  if (!data.phone || data.phone.trim().length === 0) {
    errors.push({ field: 'phone', message: 'Phone number is required' });
  } else if (!validatePhone(data.phone)) {
    errors.push({ field: 'phone', message: 'Please enter a valid phone number' });
  }

  if (!data.email || data.email.trim().length === 0) {
    errors.push({ field: 'email', message: 'Email is required' });
  } else if (!validateEmail(data.email)) {
    errors.push({ field: 'email', message: 'Please enter a valid email address' });
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Validate product form data
 */
export interface ProductFormData {
  name: string;
  description?: string;
  slug?: string;
  isPublished: boolean;
}

export function validateProductForm(data: ProductFormData): ValidationResult {
  const errors: ValidationError[] = [];

  if (!data.name || data.name.trim().length === 0) {
    errors.push({ field: 'name', message: 'Product name is required' });
  } else if (data.name.trim().length < 3) {
    errors.push({ field: 'name', message: 'Product name must be at least 3 characters' });
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Validate customer form data
 */
export interface CustomerFormData {
  firstName: string;
  lastName: string;
  email: string;
  isActive: boolean;
}

export function validateCustomerForm(data: CustomerFormData): ValidationResult {
  const errors: ValidationError[] = [];

  if (!data.firstName || data.firstName.trim().length === 0) {
    errors.push({ field: 'firstName', message: 'First name is required' });
  } else if (data.firstName.trim().length < 2) {
    errors.push({ field: 'firstName', message: 'First name must be at least 2 characters' });
  }

  if (!data.lastName || data.lastName.trim().length === 0) {
    errors.push({ field: 'lastName', message: 'Last name is required' });
  } else if (data.lastName.trim().length < 2) {
    errors.push({ field: 'lastName', message: 'Last name must be at least 2 characters' });
  }

  if (!data.email || data.email.trim().length === 0) {
    errors.push({ field: 'email', message: 'Email is required' });
  } else if (!validateEmail(data.email)) {
    errors.push({ field: 'email', message: 'Please enter a valid email address' });
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Validate inventory form data
 */
export interface InventoryFormData {
  branchId: string;
  productVariantId: string;
  quantity: number;
  lowStockThreshold?: number;
}

export function validateInventoryForm(data: InventoryFormData): ValidationResult {
  const errors: ValidationError[] = [];

  if (!data.branchId || data.branchId.trim().length === 0) {
    errors.push({ field: 'branchId', message: 'Branch is required' });
  }

  if (!data.productVariantId || data.productVariantId.trim().length === 0) {
    errors.push({ field: 'productVariantId', message: 'Product variant is required' });
  }

  if (data.quantity === undefined || data.quantity === null) {
    errors.push({ field: 'quantity', message: 'Quantity is required' });
  } else if (data.quantity < 0) {
    errors.push({ field: 'quantity', message: 'Quantity cannot be negative' });
  }

  if (data.lowStockThreshold !== undefined && data.lowStockThreshold !== null && data.lowStockThreshold < 0) {
    errors.push({ field: 'lowStockThreshold', message: 'Low stock threshold cannot be negative' });
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

