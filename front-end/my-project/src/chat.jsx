import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

const ChatComponent = () => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!prompt.trim()) {
      alert("Please enter your prompt");
      return;
    }

    // Clear the input field
    setPrompt('');

    // Show loading animation or response div
    // (You can handle this part as needed)

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
    <div className="max-w-12xl mx-auto p-4 mt-8"> {/* Added mt-8 to increase margin from the top */}
      <div className="container mx-auto p-4">
        <div className="Header mb-20">
          <p className="text-3xl text-center text-gray-800 bg-white py-4 px-8 shadow-lg rounded-xl max-w-2xl">Build your own personalized Roadmap</p>
        </div>
        <div className="info-section max-w-2xl flex justify-center,grid grid-cols-20 sm:grid-cols-1 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((_, index) => (
            <div key={index} className="info" >
              <p className= "  bg-white shadow-lg rounded-lg p-13">Hi, I am your personal assistant. I can help you to build your own personalized roadmap. What would you like to learn?</p>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="user_input mt-8 flex items-center">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="What would you like to learn?..."
            className="input border rounded-full px-4  py-8 mr-2 focus:outline-none max-w-6xl"
          />
          <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none">
            <FontAwesomeIcon icon={faPaperPlane} className="mr-2" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatComponent;
