import React, { useState, useEffect } from 'react';

function Roadmap() {
  const [roadmap, setRoadmap] = useState({ Title: "", Introduction: "", Topics: [] });

  useEffect(() => {
    fetch('http://localhost:8001/Roadmap')
      .then((r) => r.json())
      .then((data) => {
        setRoadmap(data);
        console.log(data);
      });
  }, []);

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl rounded-lg shadow-md bg-white">
      <h1 className="text-center text-3xl font-bold mb-4 underline">{roadmap.Title}</h1>
      <div className="introduction-box bg-gray-100 p-4 rounded-lg shadow-sm">
        <h2 className="text-xl font-bold mb-2">Introduction</h2>
        <p id="introduction">{roadmap.Introduction}</p>
      </div>
      <div className="topics-box bg-gray-100 p-4 rounded-lg shadow-sm">
        <h2 className="text-xl font-bold mb-2">Topics:</h2>
        <ul className="flex flex-wrap justify-center gap-4">
          {roadmap.Topics && roadmap.Topics.map((topic, index) => (
            <li key={index} className="topic p-4 rounded-lg shadow-md bg-white w-full md:w-1/2">
              <h3 className="text-lg font-bold mb-2">{topic.TopicName}</h3>
              <p>{topic.Descriptions}</p>
              <div className="objectives mt-4">
                <h5 className="text-base font-bold mb-2">Objectives:</h5>
                <ul className="list-disc pl-4">
                  {topic.LearningObjectives.map((objective, index) => (
                    <li key={index}>{objective}</li>
                  ))}
                </ul>
              </div>
              <p>Milestones: <b>{topic.Milestones}</b></p>
              <p className="links">
                Links:
                {topic.Resources.map((resource, index) => (
                  <a key={index} href={resource} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                    Link
                  </a>
                ))}
              </p>
            </li>
          ))}
        </ul>
      </div>
      {roadmap.AdditionalInfo && (
        <div className="additional-info-box bg-gray-100 p-4 rounded-lg shadow-sm">
          <h2 className="text-xl font-bold mb-2">Additional Information</h2>
          <p className="font-bold">
            <b>Tip</b>: {roadmap.AdditionalInfo.Tips}
          </p>
          <p><b>Project Ideas</b>: {roadmap.AdditionalInfo.ProjectIdeas}</p>
        </div>
      )}
    </div>
  );
}

export default Roadmap;
