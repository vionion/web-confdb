Ext.define('CmsConfigExplorer.view.path.ModuleDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.path-moduledetails',
    
    requires:['CmsConfigExplorer.model.Moduledetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: '',
        online: "False"
    },
    stores:{
        moddetails:{

    //                type:'tree',
                    model:'CmsConfigExplorer.model.Moduledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onModDetailsLoad',
                        scope: 'controller'
                    }

                }
    }
//    
//    links: {
//        details: {
//            type: 'CmsConfigExplorer.model.Moduledetails',
//            id: 'moDet11'
//        }
//    }
});