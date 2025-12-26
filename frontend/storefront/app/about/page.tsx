export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">About Grand Gold & Diamonds</h1>
        <div className="bg-white rounded-lg shadow-md p-8 space-y-6">
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Our Story</h2>
            <p className="text-gray-700 leading-relaxed">
              Grand Gold & Diamonds has been a trusted name in fine jewellery for generations. 
              We specialize in creating exquisite pieces that celebrate life's most precious moments.
            </p>
          </section>
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Our Commitment</h2>
            <p className="text-gray-700 leading-relaxed">
              We are committed to providing the highest quality jewellery, exceptional craftsmanship, 
              and outstanding customer service. Every piece is carefully selected and crafted to meet 
              our exacting standards.
            </p>
          </section>
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Quality & Craftsmanship</h2>
            <p className="text-gray-700 leading-relaxed">
              Our jewellery is crafted using only the finest materials, including certified diamonds 
              and premium gold. We work with skilled artisans who bring decades of experience to 
              every piece we create.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}


