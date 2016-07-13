Ext.define('CmsConfigExplorer.view.sequence.SequenceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.sequence-sequence',
    
    requires:['CmsConfigExplorer.model.Sequenceitem',
             'CmsConfigExplorer.model.SeqModuleitem'],
    
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        online: "False",
        first: true
    },
    
    stores:
    {        
        seqitems:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.Sequenceitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "Sequences",
                gid: -1
//                root: true
            },
            
            listeners: {

                load: 'onSeqitemsLoad', 
                scope: 'controller'
//                beforeload: 'onSeqitemsBeforeLoad'
            }
        },
        seqparameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.SeqModuleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
//                    text: "Params",
                    gid: -1
                },
            
                listeners: {
                    load: 'onSeqparametersLoad',
                    scope: 'controller'

                }
            
            }
    }

});
