import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faLightbulb, faRocket, faCogs } from '@fortawesome/free-solid-svg-icons';

const ChatComponent = () => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!prompt.trim()) {
      alert("Please enter your prompt");
      return;
    }

    setPrompt('');

    try {
      const response = await fetch("http://52.59.213.161:8080/chat", {
        method: "POST",
        body: JSON.stringify({ prompt }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      console.log(data);

      const createRoadmapResponse = await fetch("http://52.59.213.161:8080/create_roadmap", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log(createRoadmapResponse.status);
      console.log(await createRoadmapResponse.json());
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="min-h-screen max-w-6xl mx-auto p-6 mt-12 bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600 rounded-xl shadow-lg">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-extrabold text-white">Build Your Personalized Roadmap</h1>
        <p className="text-2xl text-gray-100 mt-4">Hi, I'm your personal assistant. Let's create a customized learning path for you.</p>
      </div>
      <form onSubmit={handleSubmit} className="flex items-center justify-center mb-12">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="What would you like to learn?..."
          className="border border-gray-300 rounded-full px-6 py-3 w-2/3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out"
        />
        <button type="submit" className="ml-4 bg-blue-700 hover:bg-blue-800 text-white font-bold py-3 px-6 rounded-full focus:outline-none transition duration-300 ease-in-out transform hover:scale-105">
          <FontAwesomeIcon icon={faPaperPlane} className="mr-2" /> Send
        </button>
      </form>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {[{icon: faLightbulb, text: 'Discover new ideas'}, {icon: faRocket, text: 'Accelerate your learning'}, {icon: faCogs, text: 'Tailor your roadmap'}].map((item, index) => (
          <div key={index} className="bg-white shadow-lg rounded-lg p-8 text-center transform transition duration-500 hover:scale-105">
            <FontAwesomeIcon icon={item.icon} className="text-4xl text-blue-500 mb-4" />
            <p className="text-gray-700 text-lg">{item.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatComponent;

