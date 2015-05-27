Ext.define('Demo110315.view.endpath.EndPathDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.endpath-endpathdetails',
    data: {
        name: 'Demo110315'
    },
    
        
    data: {
        name: '',
        author: '',
        class: '',
        type: ''
    },
    stores:{
        endpathdetails:{
            
            model:'Demo110315.model.Pathdetails',
            autoLoad: false,
            listeners: {
                        load: 'onEndPatDetailsLoad',
                        scope: 'controller'
                    }
            
        }
    }

});
