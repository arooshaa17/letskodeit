import logging
import time
from traceback import print_stack
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utilities.custom_logger as cl


class SeleniumDriver():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "tag":
            return By.TAG_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType +
                          " not correct/supported")
        return False

    def getElement(self, locator, locatorType="xpath"):
        try:
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
        except:
            self.log.info("Element not found with locator: " + locator +
                          " and  locatorType: " + locatorType)
        return element

    def getElements(self, locator, locatorType="xpath"):
        try:
            byType = self.getByType(locatorType)
            element_list = self.driver.find_elements(byType, locator)
        except:
            self.log.info("Element not found with locator: " + locator +
                          " and  locatorType: " + locatorType)
        return element_list

    def elementClick(self, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
        except ElementNotSelectableException:
            self.log.info("Unable to Click on element with locator: " + locator +
                          " locatorType: " + locatorType)

    def enterData(self, data, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator +
                          " locatorType: " + locatorType)
            print_stack()

    def switchFrame(self, index):
        try:
            self.driver.switch_to.default_content()
            # all_i_frames = self.driver.find_elements_by_tag_name('iframe')
            all_i_frames = self.getElements("iframe", "tag")
            frame_index = all_i_frames[index]
            self.driver.switch_to.frame(frame_index)
            time.sleep(3)
        except NoSuchFrameException:
            self.log.info("Can't switch to frame" + frame_index)

    def scrollPage(self, offset):
        self.driver.execute_script("window.scrollBy(0, arguments[0])", offset)
        time.sleep(3)

    def isElementPresent(self, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                return True
            else:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def isElementDisplayed(self, locator, locatorType="xpath"):
        """
        NEW METHOD
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not displayed with locator: " + locator +
                              " locatorType: " + locatorType)
            return isDisplayed
        except:
            print("Element not found")
            return False

    def waitForElement(self, locator, locatorType,
                       timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def getElementAttributeValue(self, attribute, locator, locatorType="xpath"):
        if locator:
            element = self.getElement(locator, locatorType)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator, locatorType="xpath", info=""):
        element = self.getElement(locator, locatorType)
        enabled = False
        try:
            attributeValue = self.getElementAttributeValue(element=element, attribute="disabled")
            if attributeValue is not None:
                enabled = element.is_enabled()
            else:
                value = self.getElementAttributeValue(element=element, attribute="class")
                self.log.info("Attribute value From Application Web UI --> :: " + value)
                enabled = not ("disabled" in value)
            if enabled:
                self.log.info("Element :: '" + info + "' is enabled")
            else:
                self.log.info("Element :: '" + info + "' is not enabled")
        except:
            self.log.error("Element :: '" + info + "' state could not be found")
        return enabled

    def elementIsEnabled(self, locator, locatorType="xpath"):
        element = self.getElement(locator, locatorType)
        if element.is_enabled:
            return True
        else:
            return False
