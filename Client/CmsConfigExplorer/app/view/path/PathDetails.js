
Ext.define("CmsConfigExplorer.view.path.PathDetails",{
    extend: "Ext.panel.Panel",

    controller: "path-pathdetails",

    viewModel: {
        type: "path-pathdetails"
    },
    
    requires:['CmsConfigExplorer.view.path.PathDetailsModel',
             'CmsConfigExplorer.view.path.PathDetailsController'],
    
    alias: 'widget.pathdetails',
    reference: "pathDetailsPanel",
    layout: {
        type: 'vbox',
        align: 'stretch'
    },
    
    listeners:{
        cusPatDetLoaded: 'onPatDetLoaded' 
        
    },
    border: true,
    bodyPadding: 5,
//    height: '100%',
    items: [
        {
            xtype: 'form',
            bodyPadding: 15,
            overflowY: 'auto',
            //frame:true,
//                border: true,    
            header: false,
//                bodyStyle:'padding:5px 5px 0',
            width: '100%',
            fieldDefaults: {
                labelAlign: 'top',
                msgTarget: 'side'
            },
            items: [
                        {
                            xtype: 'container',
                            anchor: '100%',
                            layout:'column',
                            items:[
                                {
                                xtype: 'container',
                                columnWidth:.5,
                                layout: 'anchor',
                                items: [{
                                    xtype:'textfield',
                                    reference: 'patDetailsName',
                                    fieldLabel: 'Label',
                                    name: 'label',
                                    editable: false,
                                    anchor:'96%'
                                }
                                ]
                            },
                            {
                                xtype: 'container',
                                columnWidth:.5,
                                layout: 'anchor',
                                items: [
                                    {
                                    xtype:'textfield',
                                    reference: 'patDetailsAuthor',
                                    fieldLabel: 'Author',
                                    name: 'author',
                                    editable: false,
                                    anchor:'96%'
                                }]
                            }

                            ]
                        }

                    ]
        },
        {
            xtype: 'grid',
            reference: 'pathPrescaleGrid',
            flex: 2,
            layout: 'fit',
            loadMask: true,
            width: '100%',
//            header : true,
//                        height: '75%',
            scrollable: true, 
            columns:[],
            store: {}
            
        },{
            xtype: 'textarea',
            reference: 'pathDescriptionArea',
            height: '40%',
            flex:2,
            fieldLabel: 'Description',
            labelAlign: 'top'
        }
        
    ] 
    
});
