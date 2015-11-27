Ext.define('CmsConfigExplorer.view.endpath.EndPathSmartPrescaleModel', {
    extend: 'Ext.app.ViewModel',
    
    requires:['CmsConfigExplorer.model.EndSP'],
    
    alias: 'viewmodel.endpath-endpathsmartprescale',
    data: {
        name: 'CmsConfigExplorer'
    },
    
        
    data: {
//        name: '',
//        author: '',
//        class: '',
//        type: '',
//        online: "False"
    },
    stores:{
        endspexpressions:{
            
            model:'CmsConfigExplorer.model.EndSP',
            autoLoad:false
//            ,listeners: {
////                load: 'onEndspexpressionsLoad',
//                filterchange: 'onEndspexpressionsFilterChange',
//                scope: 'controller'
//            }
            
        }
    }

});