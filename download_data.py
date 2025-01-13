from playwright.async_api import async_playwright
from datetime import datetime, timedelta
import asyncio
import os  # Import os for file existence check

async def download_data():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)  # Set headless=True for no GUI
        page = await browser.new_page()
        
        # Define the hardcoded end date
        until_date = "2024-12-04"
        until_date_obj = datetime.strptime(until_date, "%Y-%m-%d")
        
        # Loop through the date range
        for _ in range(1000):  # Modify this range for how many iterations you want
            # Calculate from_date (5 days before until_date)
            from_date_obj = until_date_obj - timedelta(days=5)
            from_date = from_date_obj.strftime("%Y-%m-%d")
            
            # Construct the file path
            html_path = f"data/trading_economics_calendar_{until_date}.html"
            
            # Skip the iteration if the file already exists
            if os.path.exists(html_path):
                print(f"File {html_path} already exists. Skipping...")
            else:
                # Go to the calendar page
                await page.goto("https://tradingeconomics.com/calendar")
                
                # Interact with the dropdown to select the calendar type
                await page.click("//form/div[3]/div/div/table/tbody/tr/td[1]/div/div[1]/button")
                await page.wait_for_selector("//form/div[3]/div/div/table/tbody/tr/td[1]/div/div[1]/ul/li[13]/a", state="visible")
                await page.click("//form/div[3]/div/div/table/tbody/tr/td[1]/div/div[1]/ul/li[13]/a")
                
                # Fill in the date range
                await page.wait_for_selector('//*[@id="startDate"]', state="visible")
                await page.fill('//*[@id="startDate"]', from_date)
                await page.fill('//*[@id="endDate"]', until_date)
                
                # Click the search button
                await page.click("//form/div[3]/div/div/div[1]/div/span[3]/button")
                
                # Wait for the page to load the calendar data
                await page.wait_for_load_state('networkidle')
                
                # Inject custom CSS to hide headers and reduce font size
                await page.add_style_tag(content="""
                    body, body * {
                        font-size: 10px !important;
                    }
                    #header, .header, header, .navbar, .hidden-head{
                        display: none !important;
                    }
                """)

                # Get the page's HTML content
                html_content = await page.content()

                # Save the HTML content to a file
                with open(html_path, "w", encoding="utf-8") as file:
                    file.write(html_content)

                print(f"HTML saved to {html_path}")

                # Sleep for 5 seconds to prevent overloading the server
                await asyncio.sleep(5)

            # Update until_date for the next loop (decrement by 1 day)
            until_date_obj = from_date_obj - timedelta(days=1)
            until_date = until_date_obj.strftime("%Y-%m-%d")
        
        await browser.close()

# Run the async function
asyncio.run(download_data())
