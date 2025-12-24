// Shared TypeScript types for frontend applications

export type RegionCode = 'UK' | 'UAE' | 'INDIA';
export type CurrencyCode = 'GBP' | 'AED' | 'INR';

export interface Region {
  code: RegionCode;
  name: string;
  defaultCurrency: CurrencyCode;
  taxRate: number;
  timezone: string;
  locale: string;
  isActive: boolean;
}

export interface Currency {
  code: CurrencyCode;
  name: string;
  symbol: string;
  isActive: boolean;
}

export interface ExchangeRate {
  fromCurrency: CurrencyCode;
  toCurrency: CurrencyCode;
  rate: number;
  effectiveDate: string;
}

export interface Branch {
  id: string;
  name: string;
  code: string;
  region: Region;
  addressLine1: string;
  addressLine2?: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
  phone: string;
  email: string;
  canShip: boolean;
  canClickCollect: boolean;
  canCrossBorder: boolean;
  operatingHours: Record<string, any>;
  isActive: boolean;
}

export interface Product {
  id: string;
  name: string;
  slug: string;
  description?: string;
  basePrice: number;
  currency: CurrencyCode;
  // Jewellery-specific attributes
  metalType?: string;
  purity?: string;
  stoneDetails?: StoneDetail[];
  makingCharge?: number;
  variants?: ProductVariant[];
}

export interface StoneDetail {
  type: string;
  carat: number;
  certification?: string;
}

export interface ProductVariant {
  id: string;
  size?: string;
  weight?: number;
  purity?: string;
  price: number;
}

export interface Order {
  id: string;
  orderNumber: string;
  status: string;
  branch?: Branch;
  region: Region;
  currency: CurrencyCode;
  totalAmount: number;
  items: OrderItem[];
  createdAt: string;
}

export interface OrderItem {
  id: string;
  product: Product;
  quantity: number;
  price: number;
  total: number;
}

