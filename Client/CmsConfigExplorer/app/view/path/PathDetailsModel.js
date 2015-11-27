Ext.define('CmsConfigExplorer.view.path.PathDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.path-pathdetails',
    
    requires:['CmsConfigExplorer.model.Pathdetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: '',
        online: "False"
    },
    stores:{
        pathdetails:{
            
            model:'CmsConfigExplorer.model.Pathdetails',
            autoLoad: false,
            listeners: {
                        load: 'onPatDetailsLoad',
                        scope: 'controller'
                    }
            
        }
    }
});