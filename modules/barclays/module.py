# -*- coding: utf-8 -*-

# Copyright(C) 2012-2013 Romain Bignon
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


from weboob.capabilities.bank import CapBank, AccountNotFound
from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import ValueBackendPassword

from .browser import Barclays


__all__ = ['BarclaysModule']


class BarclaysModule(Module, CapBank):
    NAME = 'barclays'
    MAINTAINER = u'Romain Bignon'
    EMAIL = 'romain@weboob.org'
    VERSION = '1.2'
    DESCRIPTION = u'Barclays'
    LICENSE = 'AGPLv3+'
    CONFIG = BackendConfig(ValueBackendPassword('login',    label=u"N° d'abonné", masked=False),
                           ValueBackendPassword('password', label='Code confidentiel'),
                           ValueBackendPassword('secret',   label='Mot secret'))
    BROWSER = Barclays

    def create_default_browser(self):
        return self.create_browser(self.config['secret'].get(),
                                   self.config['login'].get(),
                                   self.config['password'].get())

    def iter_accounts(self):
        with self.browser:
            return self.browser.get_accounts_list()

    def get_account(self, _id):
        with self.browser:
            account = self.browser.get_account(_id)

        if account:
            return account
        else:
            raise AccountNotFound()

    def iter_history(self, account):
        for tr in self.browser.get_history(account):
            if not tr._coming:
                yield tr

    def iter_coming(self, account):
        for tr in self.browser.get_history(account):
            if tr._coming:
                yield tr

    def iter_investment(self, account):
        return self.browser.iter_investments(account)
