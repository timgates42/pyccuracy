#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import traceback

from Queue import Queue
from threading import Thread

from pyccuracy.result import Result
from pyccuracy.common import Context
from pyccuracy.errors import ActionFailedError

class StoryRunner(object):
    def run_stories(self, settings, fixture, context=None):
        for story in fixture.stories:
            for scenario in story.scenarios:
                if not context:
                    context = self.create_context_for(settings)
                for action in scenario.givens + scenario.whens + scenario.thens:
                    result = self.execute_action(context, action)
                    if not result:
                        break

        return Result(fixture=fixture)

    def run_scenario(self, scenario, settings, fixture, context=None):
        if not context:
            context = self.create_context_for(settings)

        for action in scenario.givens + scenario.whens + scenario.thens:
            result = self.execute_action(context, action)
            if not result:
                break

        return Result(fixture=fixture)

    def execute_action(self, context, action):
        try:
            action.execute_function(context, *action.args, **action.kwargs)
        except ActionFailedError, err:
            action.mark_as_failed(err)
            return False
        except Exception, err:
            raise ValueError("Error executing action %s - %s" % (action.execute_function, traceback.format_exc(err)))
        action.mark_as_successful()
        return True

    def create_context_for(self, settings):
        return Context(settings)

class ParallelStoryRunner(StoryRunner):
    def __init__(self, number_of_threads):
        self.number_of_threads = number_of_threads
        self.test_queue = Queue()
        self.tests_executing = 0

    def worker(self):
        while True:
            scenario, context = self.test_queue.get()

            current_story = scenario.story
            if context.settings.base_url:
                base_url = context.settings.base_url
            else:
                base_url = "http://localhost"

            context.browser_driver.start_test(base_url)
            try:
                scenario.start_run()
                for action in scenario.givens + scenario.whens + scenario.thens:
                    result = self.execute_action(context, action)
                    if not result:
                        break

                scenario.end_run()

            finally:
                context.browser_driver.stop_test()


    def start_processes(self):
        for i in range(self.number_of_threads):
            t = Thread(target=self.worker)
            t.setDaemon(True)
            t.start()

    def fill_queue(self, fixture, settings):
        for story in fixture.stories:
            for scenario in story.scenarios:
                context = self.create_context_for(settings)
                self.test_queue.put((scenario, context))

    def run_stories(self, settings, fixture, context=None):
        if len(fixture.stories) == 0:
            return

        self.fill_queue(fixture, context)

        fixture.start_run()

        self.start_processes()

        try:
            time.sleep(2)
            while self.test_queue.unfinished_tasks:
                time.sleep(1)

        except KeyboardInterrupt:
            sys.stderr.write("Parallel tests interrupted by user\n")

        test_fixture.end_run()
