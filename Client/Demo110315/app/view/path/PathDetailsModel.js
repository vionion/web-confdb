Ext.define('Demo110315.view.path.PathDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.path-pathdetails',
    
    requires:['Demo110315.model.Pathdetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: ''
    },
    stores:{
        pathdetails:{
            
            model:'Demo110315.model.Pathdetails',
            autoLoad: false,
            listeners: {
                        load: 'onPatDetailsLoad',
                        scope: 'controller'
                    }
            
        }
    }
});