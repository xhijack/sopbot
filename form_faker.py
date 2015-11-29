from __future__ import unicode_literals

import random
import requests

import mechanize
from faker import Factory
from BeautifulSoup import BeautifulSoup as soup

fake = Factory.create()

USER_AGENTS = ['Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)']


class FormFactory(object):

    def __init__(self, url, form_url,
                 form_name=None,
                 attrs = {},
                 select_form=None,
                 handle_robots=False,
                 debug=False,
                 ):

        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-Agent', USER_AGENTS[0])]
        self.browser.set_handle_robots(handle_robots)
        self.browser.set_handle_equiv(handle_robots)
        self.browser.open(url)
        self.browser.set_debug_http(debug)
        self.browser.set_debug_responses(debug)
        self.form_url = form_url
        self.form_name = form_name
        self.input_list = []
        self.input_select_list = []
        self.attrs = attrs
        self.select_form = select_form

    def process(self):
        if self.attrs == {}:
            self.get_input_register()

        return self.fill_form()

    def fill_form(self):
        """ Fill form from attrs (Attributes)

        :return:
        """
        self.get_form()
        for key in self.attrs.keys():
            # print "{0} {1}".format(key, self.attrs[key])
            if self.browser.form.find_control(key).readonly is False:
                if self.attrs[key] or self.attrs[key] != '':
                    self.browser[key] = self.attrs[key]
                else:
                    value = generate_input(key)
                    self.browser[key] = value
                    self.attrs.update({key: value})
        self.browser.submit()
        response = self.browser.response().read()
        return response

    def get_form(self):
        """ Select form based on name or select form
        :return:
        """
        if self.form_name:
            self.browser.select_form(name=self.form_name)
        else:
            self.browser.select_form(predicate=self.select_form)

    def get_input_register(self):
        """ Getting input name list in form register

        :return:
        """
        response = requests.get(self.form_url)
        resp = soup(response.text)

        password = resp.find('input', {'type': 'password'})
        if self.form_name:
            form = resp.find('form', {'name': self.form_name})
        else:
            form = password.findParent('form')

        self.attrs = {}

        for input_text in form.findAll('input'):
            input_name = input_text.get('name', None)
            value = input_text.get('value', None)
            if input_text and input_name:
                if input_text['type'] == 'checkbox':
                    self.attrs.update({input_name: ['on']})
                elif input_text['type'] == 'radio':
                    self.attrs.update({input_name: [value]})
                else:
                    self.attrs.update({input_name: value})

        for input_select in form.findAll('select'):
            values = input_select.findAll('option')[1:]
            self.attrs.update({input_select.get('name', None): random.choice([[value['value']] for value in values])})


def generate_input(input_text):
    """ Generate fake string based on input_text

    :param `str` input_text: name of input form
    :return: fake data
    :rtype: `unicode`
    """
    if input_text:
        if 'full_name' in input_text or 'fullname' in input_text:
            return fake.first_name() + fake.last_name()
        elif 'username' in input_text:
            return fake.user_name()
        elif 'phone' in input_text:
            return str(fake.pyint()) + '655086' + str(fake.pyint())
        elif 'email' in input_text:
            return fake.email()
        elif 'password' in input_text or 'pass' in input_text or 'pwd' in input_text:
            # return fake.password()
            return 'wakuncar1988'
        elif 'gender' in input_text:
            return ['1']
        else:
            return fake.name()
