URL:
https://care.425dental.com/schedule-appointments/?_gl=11eu87tj_gcl_auMTY4NjUyNjY2NC4xNzI2MjUyODIw_gaNzc0MzUzODQ3LjE3MjYyNTI4MjA._ga_P7N65JEY18*MTcyNjg2NDgzMi41LjEuMTcyNjg2NDkwMi4wLjAuMA..


implement only the part of checking for available appointments for the following appointment types:
	1.	New appointment
	2.	Emergency appointment
	3.	Invisalign consultation

Requirements:
1. Environment Setup:
	•	Use Playwright (async version) to automate browser interactions.
	•	Ensure the script works in a headless browser mode for production but can be run in headful mode for debugging purposes.
	•	Set up a logging system to track the status of browser interactions and error handling.

2. Script Structure:
Your script should follow this general structure:
	•	Class Definition: SchedulingService
	•	Encapsulate all functionality within this class.
	•	The constructor should initialize the URL, Playwright, and browser variables.

3. Browser and Page Initialization:
	•	Implement methods to initialize and close the browser properly:
	•	initialize_browser() method to start Playwright and open the browser.
	•	close_browser() method to close the browser and Playwright after the task is complete.

4. Navigate to Appointment Page:
	•	Implement a method navigate_to_scheduling_page() that navigates to the appointment scheduling URL.
	•	Wait for the page to load completely by monitoring the network idle state.

5. Appointment Type Selection:
	•	Implement a method select_appointment_type_direct_click(appointment_type) that will:
	•	Accept an appointment type as input (e.g., “New appointment”, “Emergency appointment”, “Invisalign consultation”).
	•	Find and click on the correct appointment type by selecting the respective buttons or links on the page.

6. Date Preference Handling:
	•	If the page requires date selection for viewing available slots:
	•	Implement set_date_preference(date_preference) method that will allow navigating the calendar on the website and selecting a specific date.
	•	Ensure proper navigation to the correct month and selection of the desired date.

7. Check for Available Appointment Slots:
	•	Implement a method get_available_slots() to extract and return available appointment slots for the selected appointment type:
	•	Wait for the time slot elements to become visible.
	•	Scrape the time slot details (e.g., time, date) from the page.
	•	Limit the scraping to the first 5 available slots to avoid overloading the process.
	•	Return the scraped slots as a list of dictionaries, each containing the date and time of the available slots.

8. Error Handling:
	•	Implement error handling and retry mechanisms for interactions like button clicks and page navigation.
	•	Ensure that screenshots are taken in case of any errors for easier debugging.

9. Caching Mechanism:
	•	Implement a basic caching system (using a dictionary) to avoid checking the same appointment type and date multiple times during a session. This can help reduce redundant requests.
    
10. Logging:
	•	Log each important step (e.g., page navigation, button clicks, errors) with relevant messages.
	•	Make sure to log any exceptions that occur, including capturing screenshots of the page state in case of errors.