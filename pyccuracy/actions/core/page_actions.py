# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyccuracy.page import Page
from pyccuracy.actions import ActionBase
from pyccuracy.languages import LanguageItem

class PageGoToAction(ActionBase):
    regex = LanguageItem('page_go_to_regex')

    def execute(self, context, url, *args):
        base_url = context.base_url

#        if url.replace(" ", "") in context.all_pages:
#            context.current_page = context.all_pages[url.replace(" ", "")]
#            url = context.current_page.url
# 
#        if base_url:
#            url = basejoin(base_url + "/", url)
# 
#        protocol, page_name, file_name, complement, querystring, anchor = urllib2.urlparse.urlparse(url)
 
#        if not protocol:
#            if not base_url and os.path.exists(abspath(join(context.tests_dir, url))):
#                url = "file://" + abspath(join(context.tests_dir, url))
#            elif os.path.exists(url):
#                url = "file://" + abspath(url)
#            else:
#                checker = URLChecker()
#                checker.set_url(url)
#                if not checker.is_valid():
#                    raise ActionFailedError(self.language['page_go_to_failure'] % url)

        context.browser_driver.page_open(url)
        context.browser_driver.wait_for_page()

class PageAmInAction(ActionBase):
    regex = LanguageItem("page_am_in_regex")

    def execute(self, context, url, *args):
        if url.replace(" ", "") in context.all_pages:
            context.current_page = context.all_pages[url.replace(" ", "")]
            url = context.current_page.url
        else:
            raise self.failed(context.language.format("page_am_in_failure", url))

class PageSeeTitle(ActionBase):
    regex = LanguageItem('page_see_title_regex')

    def execute(self, context, title, *args):
        expected_title = context.browser_driver.get_title()
        if (title != expected_title):
            raise self.failed(context.language.format("page_see_title_failure", title, expected_title))

class PageCheckContainsMarkupAction(ActionBase):
    regex = LanguageItem("page_check_contains_markup_regex")

    def execute(self, context, expected_markup, *args):
        html = context.browser_driver.get_html_source()

        if expected_markup not in html:
            msg = context.language.format("page_check_contains_markup_failure", expected_markup)
            raise self.failed(msg)

class PageCheckDoesNotContainMarkupAction(ActionBase):
    regex = LanguageItem("page_check_does_not_contain_markup_regex")

    def execute(self, context, expected_markup, *args):
        html = context.browser_driver.get_html_source()

        if expected_markup in html:
            msg = context.language.format("page_check_does_not_contain_markup_failure", expected_markup)
            raise self.failed(msg)

class PageSeeTitleAction(ActionBase):
    regex = LanguageItem("page_see_title_regex")

    def execute(self, context, title, *args):
        actual_title = context.browser_driver.get_title()
        if (actual_title != title):
            msg = context.language.format("page_see_title_failure", actual_title, title)
            raise self.failed(msg)

class PageWaitForPageToLoadAction(ActionBase):
    regex = LanguageItem("page_wait_for_page_to_load_regex")

    def execute(self, context, timeout, *args):
        try:
            timeout = float(values[0])
        except ValueError:
            timeout = None

        if timeout:
            context.browser_driver.wait_for_page(timeout * 1000)
        else:
            context.browser_driver.wait_for_page()

class PageWaitForSecondsAction(ActionBase):
    regex = LanguageItem("page_wait_for_seconds_regex")

    def execute(self, context, timeout, *args):
        try:
            timeout = float(timeout)
        except ValueError:
            raise self.failed("The specified time cannot be parsed into a float number: %s" % timeout)

        time.sleep(timeout)

