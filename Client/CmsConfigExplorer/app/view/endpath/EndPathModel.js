Ext.define('CmsConfigExplorer.view.endpath.EndPathModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.endpath-endpath',
    
    requires:['CmsConfigExplorer.model.Endpathitem',
             'CmsConfigExplorer.model.EndPathModuleitem',
             'CmsConfigExplorer.model.EndSP'],
    
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        online: "False",
        first: true,
        trf: false,
        spname: ""
    },
    
    stores:
    {        
        endpathitems:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.Endpathitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "End Paths",
                gid: -1
//                root: true
            },
            
            listeners: {

                load: 'onEndPathitemsLoad', 
                scope: 'controller',
                
                beforeload: 'onEndPathitemsBeforeLoad'

            }
        },
        endparameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.EndPathModuleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Params",
                    gid: -1
                },
            
                listeners: {
                    
                    load: 'onEndparametersLoad' 
//                    function(store, records, successful, operation, node, eOpts) {
//                            var id = operation.config.node.get('gid');
//                            if (id == -1){
//                               operation.config.node.expand(); 
//                            }
//                    }
                }
            
            }//,
//        endspexpressions:{
//            
//            model:'CmsConfigExplorer.model.EndSP',
//            autoLoad:false
//            
//        }
        
    }
});
