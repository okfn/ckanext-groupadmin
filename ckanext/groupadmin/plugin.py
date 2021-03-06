from ckan import plugins
from ckan.config.routing import SubMapper
from ckan.plugins import toolkit
from ckanext.groupadmin.logic import action, auth
from ckanext.groupadmin import model


class GroupAdminPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IActions
    def get_actions(self):
        return dict((name, function) for name, function
                    in action.__dict__.items()
                    if callable(function))

    # IAuthFunctions
    def get_auth_functions(self):
        return dict((name, function) for name, function
                    in auth.__dict__.items()
                    if callable(function))

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'groupadmin')
        toolkit.add_ckan_admin_tab(config_, 'group_admins', 'Group Admins')

    # IConfigurable
    def configure(self, config):
        model.setup()

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.groupadmin.controller:GroupAdminController'
        with SubMapper(map, controller=controller) as m:
            m.connect('group_admins', '/ckan-admin/group_admins',
                      action='manage', ckan_icon='user')
            m.connect('group_admin_remove',
                      '/ckan-admin/group_admin_remove',
                      action='remove')
        return map
