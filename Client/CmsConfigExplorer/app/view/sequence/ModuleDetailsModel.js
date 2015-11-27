Ext.define('CmsConfigExplorer.view.sequence.ModuleDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.sequence-moduledetails',
    data: {
        name: '',
        author: '',
        class: '',
        type: ''
    },
    stores:{
        seqmoddetails:{

    //                type:'tree',
                    model:'CmsConfigExplorer.model.ESModuledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onSeqModDetailsLoad',
                        scope: 'controller'
                    }

                }
    }

});
