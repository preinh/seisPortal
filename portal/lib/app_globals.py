# -*- coding: utf-8 -*-

"""The application's Globals object"""

#from seiscomp3 import Client, IO, Core, DataModel

__all__ = ['Globals']

#def singleton(cls):
#    instances = {}
#    def getinstance():
#        if cls not in instances:
#            instances[cls] = cls()
#        return instances[cls]
#    return getinstance
#
#@singleton
#class singleInventory():
#    
#    debug = False
#
#    if debug:
##        dbDriverName="postgresql"
##        dbAddress="sysop:sysop@localhost/seiscomp3"
##        dbPlugin = "dbpostgresql"
#        dbDriverName="mysql"
#        dbAddress="sysop:sysop@localhost/seiscomp3"
#        dbPlugin = "dbmysql"
#    else:
#        dbDriverName="postgresql"
#        dbAddress="sysop:sysop@10.110.0.130/sc_request"
#        dbPlugin = "dbpostgresql"
#
#    # Get global plugin registry
#    registry = Client.PluginRegistry.Instance()
#    # Add plugin dbmysql
#    registry.addPluginName(dbPlugin)
#    # Load all added plugins
#    registry.loadPlugins()
#    # Create dbDriver
#    dbDriver = IO.DatabaseInterface.Create(dbDriverName)
#    # Open Connection 
#    #dbDriver.Open(dbAddress)   
#    dbDriver.connect(dbAddress)
#    # set Query object
#    dbQuery = DataModel.DatabaseQuery(dbDriver)
#    
#    inventory = dbQuery.loadInventory() 
#
#   
#    def __repr__(self):
#        return ('Inventory:Global')
#
#    def __unicode__(self):
#        return "Inventory_Global"


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """
    def __init__(self):
        """Do nothing, by default."""
        pass
