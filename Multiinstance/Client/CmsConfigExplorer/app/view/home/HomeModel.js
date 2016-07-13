Ext.define('CmsConfigExplorer.view.home.HomeModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.home-home',
    data: {
        name: 'CmsConfigExplorer',
        appversion: 'v1.2.2'
    }

    ,stores:
    {

    	confnames: {
    		
    		model:'CmsConfigExplorer.model.Confname',
            autoLoad:false,
            autoDestroy: true,

            listeners:{

            	load: 'onConfnamesLoaded', 
            	scope: 'controller'
            }
    	}

    }

});
