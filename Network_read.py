# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:00:52 2022
@author: boyan

This code runs for Chrome and chromium-based browsers.

"""
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# // specify the path of the Edgedriver binary that you have downloaded
driver = webdriver.Edge('MSEdgeDriver')
driver.get('https://portal.gofluent.com/app/dashboard')
time.sleep(5)
timings = driver.execute_script("return window.performance.getEntries();")
perf = driver.get_log('performance')
print(timings)
# String scriptToExecute = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"; 