/**
 * This class is the main view for the application. It is specified in app.js as the
 * "autoCreateViewport" property. That setting automatically applies the "viewport"
 * plugin to promote that instance of this class to the body element.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('CmsConfigExplorer.view.main.Main', {
    extend: 'Ext.container.Container',
    requires: [
        'CmsConfigExplorer.view.main.MainController',
        'CmsConfigExplorer.view.main.MainModel',
        'CmsConfigExplorer.view.home.Home',
        'CmsConfigExplorer.view.home.HomeModel',
        'CmsConfigExplorer.view.home.HomeController',
        'CmsConfigExplorer.view.explorer.Explorer',
        'CmsConfigExplorer.view.explorer.ExplorerController',
        'CmsConfigExplorer.view.explorer.ExplorerModel',
        'CmsConfigExplorer.view.editor.Editor',
        'CmsConfigExplorer.view.editor.EditorController',
        'CmsConfigExplorer.view.editor.EditorModel',
        'CmsConfigExplorer.view.importconf.Import',
        'CmsConfigExplorer.view.importconf.ImportController',
        'CmsConfigExplorer.view.importconf.ImportModel'
    ],

    xtype: 'app-main',
    
    alias: 'widget.app-main',

    autoShow: true,
    plugins: 'viewport',
    
    controller: 'main',
    viewModel: {
        type: 'main'
    },
    
    layout:{
        type: 'fit'
    },
    
    listeners:{
        
    },
    
    items:[
        {
            xtype: 'home',
            listeners:{
                exploreDatabase: 'onExploreDatabaseForward',
                importPython: 'onImportPythonForward',
                beforerender: 'onBeforeHomeRender'
//                custFwdOpenLastVers: 'onCustFwdOpenLastVers'
            }
        }
    ]

});
