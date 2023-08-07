import re
import ldap

from linuxmusterTools.ldapconnector.connector import LdapConnector


class LMNLdapRouter:
    def __init__(self):
        self.lc = LdapConnector()
        self.urls = {}

    def get(self, url, **kwargs):
        """
        Parse all urls and find the right method to handle the request.
        """

        for url_model, func in self.urls.items():
            match = func.url_pattern.match(url)
            if match:
                data = match.groupdict()
                ldap_filter = func(**data)

                if func.type == 'single':
                    return self.lc.get_single(func.model, ldap_filter, scope=func.scope, subdn=func.subdn, **kwargs)

                if func.type == 'collection':
                    return self.lc.get_collection(func.model, ldap_filter, scope=func.scope, subdn=func.subdn, **kwargs)
        raise Exception('Request unknown')

    def single(self, pattern, model):
        """
        Search a single entry in the whole subtree of the base dn.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'single'
            f.model = model
            f.scope = ldap.SCOPE_SUBTREE
            f.subdn = ''
            self.urls[f.url_pattern] = f
            return f
        return decorator

    def single_l(self, pattern, model):
        """
        Search a single entry in the current level scope of the base dn.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'single'
            f.model = model
            f.scope = ldap.SCOPE_ONELEVEL
            f.subdn = ''
            self.urls[f.url_pattern] = f
            return f

        return decorator

    def single_s(self, pattern, model, subdn):
        """
        Search a single entry in the whole subtree of a subtree of the base dn.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'single'
            f.model = model
            f.scope = ldap.SCOPE_SUBTREE
            f.subdn = subdn
            self.urls[f.url_pattern] = f
            return f

        return decorator

    def single_ls(self, pattern, model, subdn):
        """
        Search a single entry in the current level scope of a subtree.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'single'
            f.model = model
            f.scope = ldap.SCOPE_ONELEVEL
            f.subdn = subdn
            self.urls[f.url_pattern] = f
            return f

        return decorator

    def collection(self, pattern, model):
        """
        Search multiple entries in the whole subtree of the base dn.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'collection'
            f.model = model
            f.scope = ldap.SCOPE_SUBTREE
            f.subdn = ''
            self.urls[f.url_pattern] = f
            return f
        return decorator

    def collection_l(self, pattern, model):
        """
        Search multiple entries in the current level scope of the base dn.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'collection'
            f.model = model
            f.scope = ldap.SCOPE_ONELEVEL
            f.subdn = ''
            self.urls[f.url_pattern] = f
            return f

        return decorator

    def collection_s(self, pattern, model, subdn):
        """
        Search multiple entries in the whole subtree of a subtree of the base dn.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'collection'
            f.model = model
            f.scope = ldap.SCOPE_SUBTREE
            f.subdn = subdn
            self.urls[f.url_pattern] = f
            return f

        return decorator

    def collection_ls(self, pattern, model, subdn):
        """
        Search multiple entries in the current level scope of a subtree.

        :param pattern: URL pattern
        :type pattern: basestring
        :param model: model obejct to return, can be e.g. LMNUser
        :type model: dataclass object
        """

        def decorator(f):
            f.url_pattern = re.compile(f'^{pattern}$')
            f.type = 'collection'
            f.model = model
            f.scope = ldap.SCOPE_ONELEVEL
            f.subdn = subdn
            self.urls[f.url_pattern] = f
            return f

        return decorator

router = LMNLdapRouter()