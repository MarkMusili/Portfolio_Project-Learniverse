import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';


function ProjectSection() {
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
    <div>
      
      <div className="mt-8">
 
<div className="Header mb-20 bg-white py-4 px-4 shadow-lg rounded-xl max-w-6xl flex items-center justify-between">
  <h1 className="text-3xl font-semibold">Roadmaps</h1>
  <Link to='/chats'>
  <button className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">
    <FontAwesomeIcon icon={faPlus} className="mr-2" />
    Roadmap
  </button>
  </Link>
</div>
        <div className="grid grid-cols-20 sm:grid-cols-1 lg:grid-cols-3 gap-4">
          <Link to="/roadmap" className="planning bg-white shadow-lg rounded-lg p-4" draggable="true">
            <div className="project-box-wrapper">
              <div className="project-box-header">
                <p className="text-sm">{roadmap.created_at}</p>
                <button className=" bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg">
                  Planning
                </button>
              </div>
              <div className="project-box-body">
                <p>{roadmap.Title}</p>
              </div>
              <div className="Progress-bar">
                <p className="Progress-bar-title">Progress</p>
                <span className="box-progress" style={{ width: '0%', backgroundColor: '#ff942e' }}></span>
                <p className="percentage">0%</p>
              </div>
              <div className="Progress-bar-footer">
                <img src="../static/Images/Add.png" className="w-5 h-5" alt="Add" />
                <div className="timer">4 Days Left</div>
              </div>
            </div>
          </Link>

          {/* In Progress Column */}
          <Link to="/roadmap" className="inProgressColumn bg-white shadow-lg rounded-lg p-13">
            <div className="column-title bg-685bfa rounded-t-lg text-white p-2">In progress</div>
            <div id={`inProgress_${roadmap.id}`} className="in_progress" draggable="true">
              <div className="project-box-wrapper">
                <div className="project-box-header">
                  <p className="text-sm">{roadmap.created_at}</p>
                  <button className=" bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg">
                    in Progress
                  </button>
                </div>
                <div className="project-box-body">
                  <p>{roadmap.Title}</p>
                </div>
                <div className="Progress-bar">
                  <p className="Progress-bar-title">Progress</p>
                  <span className="box-progress" style={{ width: '60%', backgroundColor: '#ff942e' }}></span>
                  <p className="percentage">60%</p>
                </div>
                <div className="Progress-bar-footer">
                  <img src="../static/Images/Add.png" className="w-5 h-5" alt="Add" />
                  <div className="timer">4 Days Left</div>
                </div>
              </div>
            </div>
          </Link>

          {/* Completed Column */}
          <Link to="/roadmap" className="completedColumn bg-white shadow-lg rounded-lg p-4">
            <div className="column-title bg-25bd46 rounded-t-lg text-white p-2">Completed</div>
            <div className="completed draggable" draggable="true">
              <div className="project-box-wrapper">
                <div className="project-box-header">
                  <p className="text-sm">{roadmap.created_at}</p>
                  <button className=" bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg">
                    Completed
                  </button>
                </div>
                <div className="project-box-body">
                  <p>{roadmap.Title}</p>
                </div>
                <div className="Progress-bar">
                  <p className="Progress-bar-title">Progress</p>
                  <span className="box-progress" style={{ width: '100%', backgroundColor: '#ff942e' }}></span>
                  <p className="percentage">100%</p>
                </div>
                <div className="Progress-bar-footer">
                  <img src="../static/Images/Add.png" className="w-5 h-5" alt="Add" />
                  <div className="timer">4 Days Left</div>
                </div>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default ProjectSection;
