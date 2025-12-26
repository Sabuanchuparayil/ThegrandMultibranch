export default function FAQPage() {
  const faqs = [
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards, PayPal, and bank transfers. All transactions are secure and encrypted.',
    },
    {
      question: 'Do you offer custom jewelry design?',
      answer: 'Yes! We offer custom design services. Contact our team to discuss your vision and requirements.',
    },
    {
      question: 'How do I know my jewelry is authentic?',
      answer: 'All our jewelry comes with certificates of authenticity. We only work with certified diamonds and premium materials.',
    },
    {
      question: 'What is your warranty policy?',
      answer: 'We offer a lifetime warranty on craftsmanship. If there\'s a manufacturing defect, we\'ll repair or replace it at no cost.',
    },
    {
      question: 'Can I resize my ring?',
      answer: 'Yes, we offer ring resizing services. Contact us within 30 days of purchase for free resizing.',
    },
    {
      question: 'Do you ship internationally?',
      answer: 'Yes, we ship worldwide. International shipping rates and delivery times vary by destination.',
    },
    {
      question: 'How do I care for my jewelry?',
      answer: 'Clean your jewelry regularly with a soft cloth. Store pieces separately to prevent scratching. Avoid exposure to harsh chemicals.',
    },
    {
      question: 'What if my order is damaged?',
      answer: 'If your order arrives damaged, contact us immediately. We\'ll send a replacement at no cost to you.',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Frequently Asked Questions</h1>
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <div key={index} className="border-b border-gray-200 pb-6 last:border-b-0">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">{faq.question}</h2>
                <p className="text-gray-700">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}


