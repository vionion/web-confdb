Ext.define('CmsConfigExplorer.view.sequence.SequenceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.sequence-sequence',
    
    requires:['CmsConfigExplorer.model.Sequenceitem'],
    
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
                model:'CmsConfigExplorer.model.Moduleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Params",
                    gid: -1
                },
            
                listeners: {
                    load: function(store, records, successful, operation, node, eOpts) {
                            var id = operation.config.node.get('gid')
                            if (id == -1){
                               operation.config.node.expand() 
                            }
                    }
                }
            
            }
    }

});
