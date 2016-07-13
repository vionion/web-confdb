
Ext.define("CmsConfigExplorer.view.summary.Summary",{
    extend: "Ext.panel.Panel",
 
    requires: [
        "CmsConfigExplorer.view.summary.SummaryController",
        "CmsConfigExplorer.view.summary.SummaryModel",
        'Ext.grid.selection.SpreadsheetModel',
        'Ext.grid.plugin.Clipboard'
    ],
    
    alias: 'widget.summaryview',
    
    reference: 'summaryview',
    
    controller: "summary-summary",
    viewModel: {
        type: "summary-summary"
    },
    
    listeners:{
        beforerender: 'onSummaryRender'
    },
    
    layout: {
        type: 'border'
    },
    border: true,
    loadMask: true,
    items:[

    ]
    
    
});
