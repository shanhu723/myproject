#!/bin/env python
#coding=utf-8
'''
'''
from frame.lib.lianjia.link.homeTestCase import homeTestCase

class shangjiTest(homeTestCase):
    def setup_env(self):
        pass

    def test_post_update(self):
        print self.shangji.verify_post_update()

    def test_post_del(self):
        print self.shangji.verify_post_del()

    def test_transfer_customer(self):
        print self.shangji.verify_transfer_customer()

    def test_transfer_house(self):
        print self.shangji.verify_transfer_house()

    def test_contact_status(self):
        print self.shangji.verify_contact_status()

    def test_browser_status(self):
        print self.shangji.verify_browser_status()

    def test_selections(self):
        print self.shangji.verify_selections()

    def test_keyword(self):
        print self.shangji.verify_keyword()

    def test_feedback(self):
        print self.shangji.verify_feedback()

    def test_contact_count(self):
        print self.shangji.verify_contact_count()

    def test_browser_count(self):
        print self.shangji.verify_browser_count()


