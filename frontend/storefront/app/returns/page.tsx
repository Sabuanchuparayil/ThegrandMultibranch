export default function ReturnsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Returns & Exchanges</h1>
        <div className="bg-white rounded-lg shadow-md p-8 space-y-6">
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Return Policy</h2>
            <p className="text-gray-700 mb-4">
              We want you to be completely satisfied with your purchase. If you're not happy with 
              your order, you can return it within 30 days of delivery for a full refund or exchange.
            </p>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              <li>Items must be in original condition with all tags and packaging</li>
              <li>Custom or personalized items are not eligible for return</li>
              <li>Returns must be initiated within 30 days of delivery</li>
            </ul>
          </section>
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">How to Return</h2>
            <ol className="list-decimal list-inside text-gray-700 space-y-2">
              <li>Contact our customer service team to initiate a return</li>
              <li>You'll receive a return authorization and shipping label</li>
              <li>Package the item securely in its original packaging</li>
              <li>Ship the item back using the provided label</li>
              <li>Once received, we'll process your refund within 5-7 business days</li>
            </ol>
          </section>
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Exchanges</h2>
            <p className="text-gray-700">
              Need a different size or style? We're happy to help with exchanges. Contact our 
              customer service team, and we'll guide you through the exchange process.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}


