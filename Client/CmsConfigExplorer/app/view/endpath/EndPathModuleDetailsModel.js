Ext.define('CmsConfigExplorer.view.endpath.EndPathModuleDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.endpath-endpathmoduledetails',
    data: {
        name: 'CmsConfigExplorer'
    },
    
    requires:['CmsConfigExplorer.model.Moduledetails',
             'CmsConfigExplorer.model.OUTModuledetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: '',
        online: "False"
    },
    stores:{
        endmoddetails:{

    //                type:'tree',
                    model:'CmsConfigExplorer.model.Moduledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onEndModDetailsLoad',
                        scope: 'controller'
                    }

                },
        endoummoddetails:{

    //                type:'tree',
                    model:'CmsConfigExplorer.model.OUTModuledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onEndOumModDetailsLoad',
                        scope: 'controller'
                    }

                }
    }

});
