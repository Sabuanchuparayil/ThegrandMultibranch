export default function ShippingPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Shipping Information</h1>
        <div className="bg-white rounded-lg shadow-md p-8 space-y-6">
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Shipping Options</h2>
            <div className="space-y-4">
              <div className="border-l-4 border-yellow-600 pl-4">
                <h3 className="font-semibold text-gray-900">Standard Shipping</h3>
                <p className="text-gray-700">5-7 business days - Free on orders over $100</p>
              </div>
              <div className="border-l-4 border-yellow-600 pl-4">
                <h3 className="font-semibold text-gray-900">Express Shipping</h3>
                <p className="text-gray-700">2-3 business days - $15</p>
              </div>
              <div className="border-l-4 border-yellow-600 pl-4">
                <h3 className="font-semibold text-gray-900">Overnight Shipping</h3>
                <p className="text-gray-700">Next business day - $25</p>
              </div>
            </div>
          </section>
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">International Shipping</h2>
            <p className="text-gray-700">
              We ship worldwide. International shipping rates and delivery times vary by destination. 
              Please contact us for specific rates to your country.
            </p>
          </section>
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Tracking Your Order</h2>
            <p className="text-gray-700">
              Once your order ships, you'll receive a tracking number via email. You can use this 
              number to track your package's journey to your door.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

