Ext.define('CmsConfigExplorer.view.summary.SummaryModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.summary-summary',
    
    requires:['CmsConfigExplorer.model.Summaryitem',
             'CmsConfigExplorer.model.Summarycolumn'],
    
    data: {
        name: 'CmsConfigExplorer',
        idCnf: -1,
        idVer: -1,
        online: "False",
        cnfname: "",
        
        columns: []
        
    },
    
    stores:{
        summaryitems:{
            type:'tree',
            model:'CmsConfigExplorer.model.Summaryitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "Summary",
                gid: -1
//                root: true
            }
            
            ,listeners: {

                load: 'onSummaryitemsLoad', 
                scope: 'controller'
            }
        }
        ,summarycolumns:{
            model:'CmsConfigExplorer.model.Summarycolumn',
            autoLoad: false
            
            ,listeners: {

                load: 'onSummarycolumnsLoad', 
                scope: 'controller'
            }
        }
    }

});
