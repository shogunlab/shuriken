#!/usr/bin/env python
"""Set Python environment."""
# -*- coding: utf-8 -*-

import argparse
import datetime
import errno
import os
import sys
import time

from splinter import Browser
from fuzzywuzzy import fuzz

class Color:
    """Use colors to make command line output prettier."""

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class Shuriken:
    """Object for testing lists of XSS payloads."""

    def __init__(self):
        """Initiate object with default encoding and other required data."""
        # Expect some weird characters from fuzz lists, make encoding UTF-8
        sys.getdefaultencoding()

        # All potential XSS findings
        self.xss_links = []

        # Fuzzy string matching partials list
        self.xss_partials = []

        # Keep index of screens for log files
        self.screen_index = ""

        # Get user args and store
        self.user_args = self.parse_args()

        # PhantomJS browser
        self.browser = Browser("phantomjs")

    def main(self):
        """Call functions to inject XSS and test for vulnerabilities."""
        # Print out a welcome message
        print("\n")
        print("=" * 34 + Color.YELLOW + "\nWelcome to the" + Color.RED + \
            " Shuriken " + Color.YELLOW + "XSS tool!\n" + \
            Color.END + "=" * 34 + "\n")

        self.test_xss(self.user_args.PAYLOADS_LIST,
                      self.user_args.URL,
                      self.user_args.REQUEST_DELAY,
                      self.user_args.SCREENSHOT_NAME)
        print(Color.GREEN + "\n=== Testing complete! ===\n" + Color.END)

        # If the test found possible XSS vulnerabilities, ask if we should log
        if self.xss_links:
            print(Color.YELLOW + \
                "XSS vulnerabilities were detected!" + \
                Color.END)
            self.log_file(self.xss_links)
        # There were partials detected by fuzzy detection
        elif self.xss_partials:
            print(Color.YELLOW + \
                "Partial XSS vulnerabilities were detected!" + \
                Color.END)
            self.log_file(self.xss_links)
        else:
            print(Color.YELLOW + \
                "No potential XSS vulnerabilities detected...\n" + \
                Color.END
            )
            print("Goodbye!\n")

    def make_sure_path_exists(self, path):
        """Ensure that file path exists before writing."""
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def inject_payload(self, payload, link, request_delay,
                       user_screenshot_name):
        """Inject XSS payload string from user supplied payload list."""
        browser = self.browser

        # Let user specify where in the URL fuzz values should be injected
        injected_link = link.replace("{xss}", payload)

        # If user added a delay, wait that amount of time before requesting
        # Also, if user wants to interrupt/exit during wait time,
        # let them log before leaving
        if request_delay is not None:
            try:
                time.sleep(float(request_delay))
            except KeyboardInterrupt:
                print(Color.YELLOW + \
                    "\nTesting interrupted by user!\n" + Color.END)
                self.log_file(self.xss_links)
                sys.exit()

        browser.visit(injected_link)

        # Keep index of screens, so they can be easily
        # linked to line nums in log
        self.screen_index = str(len(self.xss_links) + 1)

        # Check to see if payload was reflected in HTML source,
        # if so, take screenshot depending on user flag
        self.detect_xss(payload, browser, user_screenshot_name, injected_link)

    def detect_xss(self, payload, browser_object, user_screenshot_name,
                   injected_link):
        """Check the HTML source to determine if XSS payload was reflected."""
        # If fuzzy detection chosen, evaluate partial reflection of XSS
        # by tokenizing the HTML source and detecting parts of the payload
        # and source common to both.
        #
        # Other methods of scoring include fuzz.ratio(), fuzz.partial_ratio()
        # and fuzz.token_sort_ratio()
        partial_score = fuzz.token_set_ratio(
            payload.lower(), browser_object.html.lower())
        # Set the level of detection asked for by the user, e.g. Only detect
        # matches with score higher than 50% fuzzy detection
        fuzzy_level = self.user_args.FUZZY_DETECTION

        if payload.lower() in browser_object.html.lower():
            print(Color.GREEN + "\n[+] XSS vulnerability found:" + \
                Color.END)

            # If user set the --screen flag to target, capture screenshot of
            # payload
            if user_screenshot_name is not None:
                self.take_screenshot(user_screenshot_name,
                                     browser_object, self.screen_index)

            # Add link to list of all positive XSS hits
            self.xss_links.append(injected_link)
            print(Color.BLUE + injected_link + Color.END)
        # If user enabled fuzzy detection and partial score was larger than
        # fuzz level, add it to partials list and print results
        elif fuzzy_level and (partial_score >= fuzzy_level):
            print(Color.YELLOW + \
                "\n[-] Partial XSS vulnerability found:" + Color.END)
            print(Color.BLUE + injected_link + Color.END)
            self.xss_partials.append(injected_link)
            print("Detection score: %s" % partial_score)
        else:
            print(Color.RED + "\n[+] No XSS detected at: \n" + \
                Color.BLUE + injected_link + Color.END)
            if (fuzzy_level):
                print("Detection score: %s" % partial_score)

    def take_screenshot(self, user_screenshot_name, browser_object,
                        screen_index):
        """Take a screenshot of the page in the browser object."""
        # Check if screenshots directory exists, if not then create it
        self.make_sure_path_exists("screenshots")
        screenshot_file_name = "screenshots/" + \
            user_screenshot_name + "_" + \
            datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + \
            "_" + screen_index + ".png"
        # Save screenshot to directory
        browser_object.driver.save_screenshot(screenshot_file_name)
        print(Color.YELLOW + "Screenshot saved: " + \
            screenshot_file_name + Color.END)

    def test_xss(self, payloads_param, link, request_delay,
                 user_screenshot_name):
        """Load string from payload list and call function to inject it."""
        # If the user added time delay, show them what it is set to.
        if request_delay is not None:
            print(Color.YELLOW + "\n[!] Request delay is set to [" + \
                str(request_delay) + "] seconds between requests." + Color.END)

        # Load the payload file and inject all payloads
        # into user supplied URL to test for XSS
        payloads = []
        with open(payloads_param) as payload_file:
            for line in payload_file:
                line = line.strip()
                payloads.append(line)
        for item in payloads:
            self.inject_payload(item, link, request_delay,
                                user_screenshot_name)

    def log_file(self, link_list):
        """Log successful XSS payload reflections to file."""
        # Prompt the user to confirm log file, if yes, log XSS hits
        log_confirm = input(
            "\nWould you like to save these results? [y/n] > ")
        if log_confirm == "y":
            target_name = input("Please enter the target name > ")
            # Check if logs directory exists, if not then create it
            self.make_sure_path_exists("logs")
            # Set file name
            file_name = "logs/" + target_name + "_" + \
                datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            # Save log file to directory if XSS links is populated
            if self.xss_links:
                with open(file_name + ".txt", 'w') as link_file:
                    for link in link_list:
                        link_file.write(link)
                        link_file.write("\n")
                    # Add metadata about what payload file was used
                    link_file.write(
                        "\n*** Created from the payload file >>> " +
                        self.user_args.PAYLOADS_LIST)
                    link_file.close()
            # If the user enabled fuzzy detection, log partial results
            if (self.user_args.FUZZY_DETECTION):
                with open(file_name + "_partials.txt", 'w') as partial_file:
                    for link in self.xss_partials:
                        partial_file.write(link)
                        partial_file.write("\n")
                    # Add metadata about what payload file was used
                    partial_file.write(
                        "\n*** Created from the payload file >>> " +
                        self.user_args.PAYLOADS_LIST)
                    partial_file.close()
            print("\nFile successfully saved as: " + \
                Color.BLUE + file_name + Color.END)
            print("\n")
        else:
            print("\nGoodbye!")
            print("\n")

    def parse_args(self):
        """Parse arguments from the user sent on command line."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-u', action='store', dest='URL',
            help='The URL to inject XSS payloads into.', required=True)
        parser.add_argument(
            '-p', action='store', dest='PAYLOADS_LIST',
            help='The payload list to use for injection.', required=True)
        parser.add_argument(
            '-t', action='store', dest='REQUEST_DELAY',
            help='Amount of time (in seconds) to delay between requests.')
        parser.add_argument(
            '-s', '--screen', action='store', dest='SCREENSHOT_NAME',
            help='Enable screenshots of XSS hits.')
        parser.add_argument(
            '-f', '--fuzzy', action='store', dest='FUZZY_DETECTION', type=int,
            const=50, nargs="?",
            help='Fuzzy detection rate of XSS [0 to 100 match] (default=50).')

        arguments = parser.parse_args()

        # Check for existence of '{xss}' injection point in URL string
        if "{xss}" not in arguments.URL:
            print(Color.RED + "Please provide the '{xss}' placeholder for" + \
                " injection point in the URL" + Color.END)
            print(Color.GREEN + \
                "Example: -u \"http://example.com/index.php?name={xss}\"" + \
                Color.END)
            exit()

        return arguments

if __name__ == "__main__":
    try:
        Shuriken().main()
    except KeyboardInterrupt:
        print(Color.YELLOW + \
            "\nTesting interrupted by user!\n" + Color.END)
        Shuriken().log_file(Shuriken().xss_links)
        sys.exit()
