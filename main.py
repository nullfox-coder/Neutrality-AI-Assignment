import logging
from playwright.async_api import async_playwright

class SchedulingService:
    def __init__(self,url,appointment_type,patient_type):
        self.url = url
        self.appointment_type = appointment_type
        self.patient_type = patient_type
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.closed = True
        self.state = {}
    
    async def initialize_browser(self,headless=False):
        #Start Playwright and open the browser
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        logging.info("Browser initialized.")
    
    async def close_browser(self):
        #Close the browser and Playwright
        await self.browser.close()
        await self.playwright.stop()
        logging.info("Browser closed.")

    async def navigate_to_scheduling_page(self,schedule_button):
        #Navigate to the scheduling URL and wait for the page to load
        try:
            await self.page.goto(self.url)
            await self.page.wait_for_load_state("networkidle")
            href = schedule_button
            #await self.page.screenshot(path="before_nav.png")
            if href:
                await self.page.goto(href)
                await self.page.wait_for_load_state("networkidle")
                logging.info(f"Navigated to scheduling page: {href}")
                #await self.page.screenshot(path="after_nav.png")
            else:
                logging.warning("Cannot navigate to the scheduling page.")

        except Exception as e:
            logging.error(f"Error navigating to scheduling page: {e}")
            await self.page.screenshot(path="navigate_error.png")
    
    async def select_appointment_type_direct_click(self):
        #Select the specific appointment type by clicking the corresponding button/link
        try:
            await self.page.wait_for_selector("span.ib-booking_select-box-text")
            await self.page.evaluate(f"""
            const radioButton = document.querySelector("input[name='isNew']");
            if (radioButton) {{
                radioButton.checked = true;  // Check the radio button manually
                radioButton.dispatchEvent(new Event('change', {{ bubbles: true }}));  // Manually dispatch the change event
            }}
            """)
            logging.info(f"Selected patient type: {self.patient_type}")
            await self.page.wait_for_timeout(2000)
            await self.page.click("button#continue")
            
            await self.page.screenshot(path="before_appointment.png")
            await self.page.click(f"//div[@class='ib-booking-option-title' and contains(text(), '{self.appointment_type}')]")
            logging.info(f"Selected appointment type: {self.appointment_type}")
        except Exception as e:
            logging.error(f"Error selecting appointment type: {e}")
            await self.page.screenshot(path="select_appointment_type_error.png")
            
    
    async def get_available_slots(self):
        #Scrape the available appointment slots and return them in a structured forest
        try:
            # Wait for the availability table to become visible
            await self.page.wait_for_selector(".ib-booking_availability-table")

            available_slots = []

            # Find all the active booking columns (dates with available slots)
            columns = await self.page.query_selector_all("div.ib-booking-column")

            # Loop through each column to find available time slots
            limit_slots=0
            for column in columns:
                if(limit_slots>=5):
                    break
                limit_slots+=1
                # Extract the day and date
                day_element = await column.query_selector(".ib-booking-day")
                date_element = await column.query_selector(".ib-booking-dateNum")
                
                if day_element and date_element:
                    day = await day_element.inner_text()
                    date = await date_element.inner_text()
                    full_date = f"{day}, {date}"

                    # Find all available time slots in this column
                    time_slots = await column.query_selector_all(".ib-booking-time .ib-booking-active")

                    # Extract the time values
                    for slot in time_slots:
                        time = await slot.inner_text()
                        if time.strip():
                            available_slots.append({
                                'date': full_date,
                                'time': time
                            })
            
            logging.info(f"Found available slots: {available_slots}")
            return available_slots
        except Exception as e:
            logging.error(f"Error scraping available slots: {e}")
            await self.page.screenshot(path="available_slots_error.png")
            return []

    
    async def check_available_appointments(self,date_preference=None):
        #Combines the steps to check available appointments for a scpecific tyoe and optional date
        try:
            # Get all available slots using the get_available_slots function
            available_slots = await self.get_available_slots()

            # Filter the slots based on the date_preference
            slots_for_date_preference = [slot for slot in available_slots if slot['date'] == date_preference]

            if slots_for_date_preference:
                logging.info(f"Available slots for {date_preference}: {slots_for_date_preference}")
                return slots_for_date_preference
            else:
                logging.info(f"No available slots for {date_preference}")
                return []

        except Exception as e:
    
            logging.error(f"Error checking available appointments for {date_preference}: {e}")
            await self.page.screenshot(path="check_appointments_error.png")
            return []
    
    
async def main():
    logging.basicConfig(level=logging.INFO)

    url1 = "https://care.425dental.com/schedule-appointments/?_gl=1*1eu87tj*_gcl_au*MTY4NjUyNjY2NC4xNzI2MjUyODIw*_ga*Nzc0MzUzODQ3LjE3MjYyNTI4MjA.*_ga_P7N65JEY18*MTcyNjg2NDgzMi41LjEuMTcyNjg2NDkwMi4wLjAuMA.."
    url2 = "http://425dent.com"

    p_type = int(input("Select Patient Type : \n1.New Patient\n2.Returning Patient\n"))
    a_type = int(input("Select Appointment Type :\n1.New Appointment\n2.Emergency Appointment\n3.Invisalign Consultant\n4.Dental Cleaning\n"))
    p_type_list = ["New Patient","Returning Patient"]
    a_type_list = ["New Patient Exam - 60 min","Emergency Exam - 30 min","In-office Invisalign Consultation - 60 min","Dental Cleaning - 60 min"]
    s_type_list = ["/Org_NP","/Org_EV","/Org_IO_INVISI","/Org-Clean"]
    patient_type=p_type_list[p_type-1]
    schedule_button=url2+s_type_list[a_type-1]
    appointment_type=a_type_list[a_type-1]
 
    
    service = SchedulingService(url1,appointment_type,patient_type)

    await service.initialize_browser()

    await service.navigate_to_scheduling_page(schedule_button)
    
    await service.select_appointment_type_direct_click()
    await service.get_available_slots()

    slots = await service.check_available_appointments()

    print(slots)

    await service.close_browser()

import asyncio
asyncio.run(main())
