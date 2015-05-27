Ext.define('Demo110315.view.endpath.EndPathModuleDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.endpath-endpathmoduledetails',
    data: {
        name: 'Demo110315'
    },
    
    requires:['Demo110315.model.Moduledetails',
             'Demo110315.model.OUTModuledetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: ''
    },
    stores:{
        endmoddetails:{

    //                type:'tree',
                    model:'Demo110315.model.Moduledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onEndModDetailsLoad',
                        scope: 'controller'
                    }

                },
        endoummoddetails:{

    //                type:'tree',
                    model:'Demo110315.model.OUTModuledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onEndOumModDetailsLoad',
                        scope: 'controller'
                    }

                }
    }

});
