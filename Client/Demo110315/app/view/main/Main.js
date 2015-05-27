/**
 * This class is the main view for the application. It is specified in app.js as the
 * "autoCreateViewport" property. That setting automatically applies the "viewport"
 * plugin to promote that instance of this class to the body element.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('Demo110315.view.main.Main', {
    extend: 'Ext.container.Container',
    requires: [
        'Demo110315.view.main.MainController',
        'Demo110315.view.main.MainModel',
        'Demo110315.view.home.Home',
        'Demo110315.view.home.HomeModel',
        'Demo110315.view.home.HomeController',
        'Demo110315.view.explorer.Explorer',
        'Demo110315.view.explorer.ExplorerController',
        'Demo110315.view.explorer.ExplorerModel',
        'Demo110315.view.editor.Editor',
        'Demo110315.view.editor.EditorController',
        'Demo110315.view.editor.EditorModel'
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
                exploreDatabase: 'onExploreDatabaseForward'
//                custFwdOpenLastVers: 'onCustFwdOpenLastVers'
            }
        }
    ]

});
