Ext.define('CmsConfigExplorer.view.endpath.EndPathDetailsModel', {
    extend: 'Ext.app.ViewModel',
    
    requires:['CmsConfigExplorer.model.Pathdetails'],
    
    alias: 'viewmodel.endpath-endpathdetails',
    data: {
        name: 'CmsConfigExplorer'
    },
    
        
    data: {
        name: '',
        author: '',
        class: '',
        type: '',
        online: "False"
    },
    stores:{
        endpathdetails:{
            
            model:'CmsConfigExplorer.model.Pathdetails',
            autoLoad: false,
            listeners: {
                        load: 'onEndPatDetailsLoad',
                        scope: 'controller'
                    }
            
        }
    }

});
