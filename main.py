#!/usr/bin/env python
from modules import DPH_MA_Monitor, Boston_MA_Monitor, Somerville_MA_Monitor, Cambridge_MA_Monitor
from modules import draw_screen
from apscheduler.schedulers.blocking import BlockingScheduler

DEBUG = False

def update_screen():
    # BUILD STATE_INFORMATION
    state_info = {
        "name" : "Massachusetts",
        "two_letter" : "MA"
    }
    # Update STATE_INFORMATION with scraped data
    ma_data = DPH_MA_Monitor.get_data()
    state_info.update(ma_data)
    if DEBUG:
        print(state_info)

    # BUILD LOCATIONS
    locations = []
    locations.append(Boston_MA_Monitor.get_data())
    locations.append(Somerville_MA_Monitor.get_data())
    locations.append(Cambridge_MA_Monitor.get_data())
    if DEBUG:
        print(locations)

    draw_screen.makeScreen(state_info, locations)

# REFRESH SCREEN ONCE AT BEGINNING
update_screen()

# SET UP SCHEDULER TO RUN THIS TASK
scheduler = BlockingScheduler()
scheduler.add_job(update_screen, 'interval', hours=2)
scheduler.start()