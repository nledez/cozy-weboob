# -*- coding: utf-8 -*-

# Copyright(C) 2016      James GALT
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


from .pages import LoginPage, AccountsPage, AccountDetailPage, AccountHistoryPage, RedirectPage
from weboob.browser import URL, LoginBrowser, need_login
from weboob.exceptions import BrowserIncorrectPassword
from datetime import date

class AmundiTCBrowser(LoginBrowser):
    TIMEOUT = 120.0

    login = URL('/home', LoginPage)
    redirect = URL('/home_indispo_redirect', RedirectPage)
    accounts = URL('/home_ajax_noee\?api=/api/individu/positionTotale', AccountsPage)
    account_detail = URL('/home_ajax_noee', AccountDetailPage)
    account_history = URL('/home_ajax_noee\?api=/api/individu/operations', AccountHistoryPage)

    def __init__(self, website, *args, **kwargs):
        super(AmundiTCBrowser, self).__init__(*args, **kwargs)
        self.BASEURL = website

    def do_login(self):
        """
        Attempt to log in.
        Note: this method does nothing if we are already logged in.
        """
        assert isinstance(self.username, basestring)
        assert isinstance(self.password, basestring)
        self.login.go()
        self.page.login(self.username, self.password)
        if self.login.is_here():
            raise BrowserIncorrectPassword()

    @need_login
    def iter_accounts(self):
        self.accounts.go()
        return self.page.iter_accounts()

    @need_login
    def iter_investments(self, account):
        # self.account_detail.go()
        self.account_detail.go(params={'api':'/api/individu/positionFonds', 'idEnt':account._ident, 'date':date.today().strftime('%d/%m/%Y'), 'flagUrlFicheFonds':'true'})
        return self.page.iter_investments(data={'acc': account})

    @need_login
    def iter_history(self, account):
        self.account_history.go(params={'limit':1})
        total=int(self.page.doc['nbOperationsIndividuelles'])
        params={'valeurExterne':'false','statut':'CPTA','filtreStatutModeExclusion':'false','limit':100, 'offset':0}
        self.account_history.go(params=params)
        return self.page.iter_history(data={'acc': account, 'params':params, 'total':total})
