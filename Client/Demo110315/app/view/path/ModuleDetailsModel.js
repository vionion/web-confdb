Ext.define('Demo110315.view.path.ModuleDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.path-moduledetails',
    
    requires:['Demo110315.model.Moduledetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: ''
    },
    stores:{
        moddetails:{

    //                type:'tree',
                    model:'Demo110315.model.Moduledetails',
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
//            type: 'Demo110315.model.Moduledetails',
//            id: 'moDet11'
//        }
//    }
});