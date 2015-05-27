Ext.define('Demo110315.view.sequence.ModuleDetailsModel', {
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
                    model:'Demo110315.model.ESModuledetails',
                    autoLoad:false,

                    listeners: {
                        load: 'onSeqModDetailsLoad',
                        scope: 'controller'
                    }

                }
    }

});
