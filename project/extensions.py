from flask_restplus import Api
from flask import url_for


class ExtendedApi(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    @property
    def base_url(self):
        return url_for(self.endpoint('root'), _external=True, _scheme='https')
