# Shuriken | 手裏剣
![logo](https://i.imgur.com/Jr3rbL0.png "Shuriken Logo")

[![python](https://img.shields.io/badge/python-2.7-brightgreen.svg)](https://www.python.org/downloads/) [![license](https://img.shields.io/badge/license-MIT-red.svg)](https://github.com/shogunlab/shuriken/blob/master/LICENSE.md) [![twitter](https://img.shields.io/badge/twitter-%40shogun__lab-0084b4.svg)](https://twitter.com/shogun_lab)

Shuriken was developed by [Shogun Lab](http://www.shogunlab.com/) as an open source [Cross-Site Scripting](https://en.wikipedia.org/wiki/Cross-site_scripting) (XSS) command line utility to aid web security researchers who want to test a list of XSS payloads in a web application. It allows a tester to easily change payload lists, log results and take screenshots of successful payloads. 

It should only be used on valid targets who have consented to pentesting, **please ensure you have permission** before using this tool against a web application.

## Installation
Shuriken can be installed by downloading the zip file [here](https://github.com/shogunlab/shuriken/archive/master.zip) or by cloning the [Git](https://github.com/shogunlab/shuriken.git) repository:

`git clone https://github.com/shogunlab/shuriken.git`

Shuriken works with [Python](http://www.python.org/download/) **2.7.x** on any platform.

## Features
- Easily specify where in a URL the payload should be injected with the "{xss}" string.
- Quickly change payload lists.
- Take screenshots of successful XSS hits.
- Save logs of reflected XSS payloads.

## Usage
To get a list of options and switches, enter:

`python shuriken_xss.py -h`

To test a list of payloads against a target URL, specify where the payloads will go with "{xss}" and enter:

`python shuriken_xss.py -u "http://example.com/target.php?name={xss}" -p "xss-payload-list.txt"`

If you would like to screenshot and save all reflected XSS payloads, use the *--screen* flag with a name for the screenshot images and enter:

`python shuriken_xss.py -u "http://example.com/target.php?name={xss}" -p "xss-payload-list.txt" --screen ExampleTarget`

To wait a specific amount of time in between requests, use the *-t* flag with the amount of time to wait in seconds and enter:

`python shuriken_xss.py -u "http://example.com/target.php?name={xss}" -p "xss-payload-list.txt" -t 1.5

**You must specify a payload and URL**, if you don't then you'll get an error. For an example payload to test with, check out this list of [common XSS payloads](https://github.com/foospidy/payloads/blob/master/owasp/fuzzing_code_database/xss/common.txt).

## Third party libraries and dependencies
This tool depends on the proper configuration and installation of the following:
- [Python 2.7.x](https://www.python.org/downloads/) - Python 2 is needed to run the tool.
- [Splinter](https://splinter.readthedocs.io/en/latest/install.html) - Python library allowing use of a headless web browser for testing.
- [PhantomJS](http://phantomjs.org/download.html) - Headless WebKit browser used by Splinter for testing.
- [Selenium 2.0](http://www.seleniumhq.org/docs/03_webdriver.jsp) - WebDriver required by PhantomJS browser.

If you would prefer that this tool ***use a different browser for testing***, you can read the [Splinter docs](https://splinter.readthedocs.io/en/latest/#drivers) and insert your preferred browser in the "inject_payload" method where it says `browser = Browser("phantomjs")`. Leaving it blank as `browser = Browser()` will default to Firefox.

## Screenshots
Basic usage
![screen_1](https://i.imgur.com/yEQReEh.png "Shuriken Screenshot #1")


With additional *--screen* option to record screenshots
![screen_2](https://i.imgur.com/aoxh13d.png "Shuriken Screenshot #2")

## Legal
Shuriken was derived from the excellent XSS command line tool by Faizan Ahmad, called [XssPy](https://github.com/faizann24/XssPy). The Shuriken XSS tool is under an MIT license, you can read it [here](https://github.com/shogunlab/shuriken/blob/master/LICENSE.md).

The Shuriken logo is licensed under a [Creative Commons Attribution 3.0 United States License](http://creativecommons.org/licenses/by/3.0/us/). Authored by Monjin Friends.

Be responsible and use this tool at your own discretion, I cannot be held responsible for any damages caused.
