import React from 'react';
import heroMobile from './assets/image-hero-mobile.png';
import heroTablet from './assets/image-hero-tablet.png';
import heroDesktop from './assets/image-hero-desktop.png';
import logoDark from './assets/logo-dark.svg';
import logoLight from './assets/logo-light.svg';
import iconAnimation from './assets/icon-animation.svg';
import iconDesign from './assets/icon-design.svg';
import iconPhotography from './assets/icon-photography.svg';
import iconCrypto from './assets/icon-crypto.svg';
import iconBusiness from './assets/icon-business.svg';

// Define the courses array
const courses = [
  {
    icon: iconAnimation,
    title: 'Animation',
    description: 'Learn the latest animation techniques to create stunning motion design and captivate your audience.'
  },
  {
    icon: iconDesign,
    title: 'Design',
    description: 'Create beautiful, usable interfaces to help shape the future of how the web looks.'
  },
  {
    icon: iconPhotography,
    title: 'Photography',
    description: 'Explore critical fundamentals like lighting, composition, and focus to capture exceptional photos.'
  },
  {
    icon: iconCrypto,
    title: 'Crypto',
    description: 'All you need to know to get started investing in crypto. Go from beginner to advanced with this 54-hour course.'
  },
  {
    icon: iconBusiness,
    title: 'Business',
    description: 'A step-by-step playbook to help you start, scale, and sustain your business without outside investment.'
  }
];

const LandingPage = () => {
  return (
    <div className="relative">
      {/* Hero Image */}
      <div className="absolute top-0 right-0 w-1/2 h-screen bg-cover bg-no-repeat bg-hero-mobile md:bg-hero-tablet lg:bg-hero-desktop" style={{ backgroundImage: `url(${heroMobile})` }}></div>
      {/* Header */}
      <header className="flex justify-between items-center px-6 py-4 bg-white shadow-md">
        <img className="h-8" src={logoDark} alt="logo" />
        <button href="#" className="bg-blue text-white py-2 px-6 rounded-full text-sm font-semibold hover:bg-blue-700">Get Started</button>
      </header>
      {/* Main Content */}
      <main className="py-20">
        <section className="container mx-auto flex flex-col md:flex-row justify-between items-center px-6">
          {/* Introduction */}
          <div className="md:w-1/2 text-center md:text-left">
            <div className="mb-12">
              <h1 className="text-4xl md:text-6xl font-bold text-blue leading-tight">Maximize skill, minimize budget</h1>
              <p className="text-lg md:text-xl text-gray-700 mt-4">Our modern courses across a range of in-demand skills will give you the knowledge you need to live the life you want.</p>
            </div>
            <button href="#" className="bg-gradient-to-r from-orange to-pink text-white py-3 px-8 rounded-full text-lg font-semibold hover:bg-pink-600 transition duration-300 ease-in-out">Get Started</button>
          </div>
        </section>
        {/* Course Cards */}
        <div className="container mx-auto mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="bg-gradient-to-r from-blue-600 to-pink-400 rounded-lg shadow-lg p-6">
              <div className="bg-gradient-to-r from-blue-600 to-pink-400 text-white rounded-lg font-semibold text-lg py-8 px-6">
                Check out our most popular courses!
              </div>
            </div>
          {/* Course Cards */}
          {courses.map((course, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-6">
              <img className="w-12 mb-4 mx-auto" src={course.icon} alt={course.title} />
              <h2 className="text-xl font-bold text-blue text-center">{course.title}</h2>
              <p className="text-gray-700 mt-2">{course.description}</p>
              <button href="#" className="text-orange font-semibold mt-4 block text-center">Get Started</button>
            </div>
          ))}
        </div>
      </main>
      {/* Footer */}
      <footer className="absolute bottom-0 left-0 w-full bg-blue text-white py-6">
        <div className="container mx-auto flex justify-between items-center px-6">
          <img className="h-8" src={logoLight} alt="logo" />
          <button href="#" className="bg-gradient-to-r from-orange to-pink text-white py-3 px-8 rounded-full text-lg font-semibold hover:bg-pink-600 transition duration-300 ease-in-out">Get Started</button>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
