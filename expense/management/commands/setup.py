# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.db.models import get_model
from django.db.models import ObjectDoesNotExist
from optparse import make_option

DEFAULT_GROUPS = ( "Client",
                   "Supplier" )

DEFAULT_PERMISSIONS = ( )

#TODO: Maybe in the future is more interesting work on a file like YAML to 
# Configure this permissions 
DEFAULT_GROUPS_PERMISSIONS = { "Supplier" :  
                                 (("Transaction",
                                  "can_insert_expend_for_client",
                                  u"Permission to insert expend to client"),),
                                 "Client":
                                 (("Transaction",
                                  "can_confirm_expend",
                                  u"Permission to insert expend to client"),)
                            }


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--auth_system', action="store_false", default=True,
            dest="with_acl",
            help='Specify to not setup auth system of MONEYME that ' \
                    'is create default groups and permissions'),
    )
    help = 'Setup application MoneyMe to work properly and verify some inconsistencies'

    def handle_noargs(self, **options):
        raise DeprecationWarning("Not recommended use the command setup anymore " \
                                "for ACL use instead install.py on moneyme " \
                                "webapp root path (eg: python install.py)")
        
        from django.db.models import get_apps
        from django.db import connection
        # Verify if moneyme.expense is INSTALLED
        for app in get_apps():    
            app_name = "%s.%s" % (app.__name__.split('.')[0],
                                   app.__name__.split('.')[1])
            if app_name == "moneyme.expense": #money.expense is installed
                tables = connection.introspection.table_names()
                seen_models = connection.introspection.installed_models(tables)
                
                for m in seen_models:
                    e = str(m)
                    if "moneyme" in e: # moneyme models was created
                        moneyme_models_ok = True
                    
                    if "auth.models.Group" in e:
                        auth_group_model_ok = True
                        group_model = m
                    
                with_acl = options.get("with_acl")
                if with_acl:
                    self.__create_default_groups_if_not_exist()
                    
                
                
                    
    
    def __create_default_groups_if_not_exist(self):
        group_model = get_model("auth", "Group")
        for g in DEFAULT_GROUPS:
            try:
                # verify if the groups already exist
                group_model.objects.get(name=g)
            except ObjectDoesNotExist:
                # if not create
                g_instance = group_model.objects.create(name=g)
                self.__create_default_permissions_for_group(g_instance)
    
    def __create_default_permissions_for_group(self, group_instance):
        permission_model = get_model("auth", "Permission")
        ct_model = get_model("contenttypes", "ContentType")
        # TODO: Code for in the case of models no exist
        
        if group_instance.name == "Client":
            p_name = "Client"
        elif group_instance.name == "Supplier":
            p_name = "Supplier"
        else:
            p_name = ""
        
        if DEFAULT_GROUPS_PERMISSIONS.has_key(p_name):
            perms = DEFAULT_GROUPS_PERMISSIONS[p_name]
            
            for perm in perms:
                # Import model of the permission that must apply
                module = __import__('moneyme.expense.models', globals(), locals(), perm[0], -1)
                exec("apply2model = module.%s" % perm[0], globals(), locals())
                ct4model = ct_model.objects.get_for_model(apply2model)
                permission = permission_model()
                permission.name = perm[2]
                permission.codename = perm[1]
                permission.content_type = ct4model
                permission.save()
                group_instance.permissions.add(permission)
                group_instance.save()   
                


