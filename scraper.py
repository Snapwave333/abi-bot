from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import datetime
import re
from datetime import timedelta
import logging
import time

class ESSScraper:
    def __init__(self, venue_id, username, password, headless=True):
        self.venue_id = venue_id
        self.username = username
        self.password = password
        self.headless = headless
        self.logger = logging.getLogger("ABI_Bot.Scraper")
        self.user_data_dir = os.path.join(os.getcwd(), "bot_profile")
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

    def scrape_schedule(self):
        """Scrapes the ESS schedule and returns a list of event dicts."""
        events = []
        with sync_playwright() as p:
            self.logger.info(f"Launching Browser (Headless: {self.headless})")
            browser = p.chromium.launch_persistent_context(
                self.user_data_dir,
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled"],
                viewport={"width": 1280, "height": 720}
            )
            
            try:
                page = browser.pages[0]
                page.set_default_timeout(20000)
                
                # Login
                self._login(page)
                
                # Navigate
                if not self._navigate_to_schedule(page):
                    return []

                # Parse
                events = self._parse_calendar(page)
                self.logger.info(f"Scraped {len(events)} events.")
                return events

            except Exception as e:
                self.logger.error(f"Scrape Error: {e}")
                return []
            finally:
                browser.close()

    def _login(self, page):
        self.logger.info("Navigating to ESS...")
        try:
            page.goto("https://ess.abimm.com/ABIMM_ASP/Request.aspx")
        except:
            self.logger.warning("Initial load failed, reloading...")
            page.reload()

        if page.locator("#input_venue").is_visible(timeout=5000):
            self.logger.info("Entering Venue ID...")
            page.fill("#input_venue", self.venue_id)
            page.click("input[type='button'][value='Submit']")
            page.wait_for_load_state("networkidle")

        if page.locator("#LoginId").is_visible(timeout=5000):
            self.logger.info("Logging in...")
            page.fill("#LoginId", self.username)
            page.fill("#PIN", self.password)
            page.click("#loginButton")
            page.wait_for_load_state("networkidle")

    def _navigate_to_schedule(self, page):
        self.logger.info("Locating Schedule...")
        found = False
        for link_text in ["My Schedule", "Schedule"]:
            if page.locator(f"text={link_text}").count() > 0:
                page.click(f"text={link_text}")
                found = True
                break
        
        if not found and "Schedule" not in page.title():
            self.logger.warning("Could not auto-navigate to Schedule.")
            return False
            
        page.wait_for_load_state("networkidle")
        try:
            page.wait_for_selector(".calendar_day_box", timeout=10000)
            return True
        except:
            self.logger.error("Calendar element not found.")
            return False

    def _parse_calendar(self, page):
        self.logger.info("Parsing calendar HTML...")
        soup = BeautifulSoup(page.content(), 'html.parser')
        events = []
        
        month_title = soup.find('span', class_='MonthTitle')
        if not month_title:
            return []

        month_year_text = month_title.get_text(strip=True)
        try:
            current_month_date = datetime.datetime.strptime(month_year_text, "%B %Y")
        except:
            self.logger.error(f"Failed to parse month date: {month_year_text}")
            return []

        day_boxes = soup.find_all('td', class_='calendar_day_box')
        
        for box in day_boxes:
            if 'other_month_box' in box.get('class', []): continue
            
            text = box.get_text(strip=True)
            if not text: continue
            
            match = re.match(r'^(\d{1,2})', text)
            if not match: continue
            day_num = int(match.group(1))

            details_div = box.find('div', class_='day_details')
            if details_div and details_div.find('a'):
                link = details_div.find('a')
                href = link.get('href', '')
                id_match = re.search(r"showDetails\('(\d+)'\)", href)
                
                if id_match:
                    evt_id = id_match.group(1)
                    time_range = link.get_text(strip=True)
                    
                    try:
                        evt_name_tag = soup.find('div', id=f"{evt_id}evt")
                        loc_name_tag = soup.find('div', id=f"{evt_id}fac")
                        
                        evt_name = evt_name_tag.get_text(strip=True) if evt_name_tag else "Unknown Event"
                        loc_name = loc_name_tag.get_text(strip=True) if loc_name_tag else "Unknown Location"
                        
                        t_match = re.search(r"(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)", time_range, re.IGNORECASE)
                        if t_match:
                            s_str, e_str = t_match.groups()
                            base_date = current_month_date.replace(day=day_num)
                            day_str = base_date.strftime('%Y-%m-%d')
                            
                            start_dt = datetime.datetime.strptime(f"{day_str} {s_str}", "%Y-%m-%d %I:%M %p")
                            end_dt = datetime.datetime.strptime(f"{day_str} {e_str}", "%Y-%m-%d %I:%M %p")
                            
                            if end_dt < start_dt:
                                end_dt += timedelta(days=1)
                            
                            events.append({
                                "summary": evt_name,
                                "location": loc_name,
                                "description": f"Shift: {time_range}\nScraped from ESS.",
                                "start": start_dt,
                                "end": end_dt,
                                "time_str": time_range
                            })
                    except Exception as e:
                        self.logger.warning(f"Error parsing event on day {day_num}: {e}")

        return events
