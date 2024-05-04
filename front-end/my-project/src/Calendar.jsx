
import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
;

function Calendar2024() {
    const [value, onChange] = useState(new Date());

    return (
        <div className="max-w-12xl mx-auto p-4">
            <h1 className="text-2xl font-semibold mb-4">Calendar</h1>
            <div className="bg-blue-500  p-4 rounded-lg h-500"> {/* Adjust height here */}
                <Calendar
                    onChange={onChange}
                    value={value}
                    className="w-full h-full"
                    calendarClassName="bg-white rounded-lg shadow-lg h-full"
                    tileClassName="border border-blue-200 p-2 text-center"
                />
            </div>
        </div>
    );
}

export default Calendar2024;



