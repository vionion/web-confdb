Ext.define('CmsConfigExplorer.view.sequence.ModuleDetailsModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.sequence-moduledetails',
    
    requires: ['CmsConfigExplorer.model.SeqModuledetails'],
    
    data: {
        name: '',
        author: '',
        class: '',
        type: ''
    },
    stores:{
        seqmoddetails:{

    //                type:'tree',
                    model:'CmsConfigExplorer.model.SeqModuledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onSeqModDetailsLoad',
                        scope: 'controller'
                    }

                }
    }

});
