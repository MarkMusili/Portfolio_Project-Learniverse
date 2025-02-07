import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

function Calendar2024() {
    const [value, onChange] = useState(new Date());
    const [activeStartDate, setActiveStartDate] = useState(new Date());

    // Handle month/year change
    const handleNavigation = (event) => {
        const [year, month] = event.target.value.split('-');
        setActiveStartDate(new Date(year, month - 1));
    };

    return (
        <div className="max-w-12xl mx-auto p-4">
            <h1 className="text-2xl font-semibold mb-4">Calendar 2024</h1>
            <div className="mb-4">
                <label htmlFor="month" className="mr-2">Go to:</label>
                <input
                    type="month"
                    id="month"
                    min="2024-01"
                    max="2024-12"
                    defaultValue="2024-01"
                    onChange={handleNavigation}
                    className="p-2 border rounded"
                />
            </div>
            <div className="bg-blue-500 p-4 rounded-lg h-500">
                <Calendar
                    onChange={onChange}
                    value={value}
                    activeStartDate={activeStartDate}
                    onActiveStartDateChange={({ activeStartDate }) =>
                        setActiveStartDate(activeStartDate)
                    }
                    className="w-full h-full"
                    calendarClassName="bg-white rounded-lg shadow-lg h-full"
                    tileClassName="border border-blue-200 p-2 text-center"
                />
            </div>
        </div>
    );
}

export default Calendar2024;