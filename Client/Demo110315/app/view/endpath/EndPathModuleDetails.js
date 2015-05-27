
Ext.define("Demo110315.view.endpath.EndPathModuleDetails",{
    extend: "Ext.panel.Panel",

    controller: "endpath-endpathmoduledetails",
    viewModel: {
        type: "endpath-endpathmoduledetails"
    },

    alias: 'widget.endmoduledetails',
    
    reference: 'endModDetails',
    
    paddingRight: 5,
    paddingBottom: 5,

    listeners:{
        cusEndDetLoaded: 'onEndDetLoaded',
        cusEndOumDetLoaded: 'onEndOumDetLoaded'    
    },
    
    layout: 'border',
    flex: 1,
    items: [
            {
                xtype: 'form',
                region: 'center',
                bodyPadding: 15,
                overflowY: 'auto',  
                header: false,
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
                                    reference: 'endModDetailsName',
                                    fieldLabel: 'Label',
                                    name: 'label',
                                    editable: false,
                                    anchor:'96%',
                                    margin: '0 0 11 0'
                                },
                                { 
                                    xtype: 'label',
                                    text: 'Go to STREAM:'
//                                    margin: '25 0 5 0'
                                },
                                {
                                    xtype:'button',
//                                    fieldLabel: 'associated STREAM',
                                    reference: 'endModDetailsStream',
                                    name: 'stream',
                                    disabled: true,
                                    anchor:'96%',
                                    margin: '3 0 6 0'
                                },        
                                {
                                    xtype:'combobox',
                                    fieldLabel: 'Used in',
                                    disabled: true,
                                    name: 'usedin',
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
                                    reference: 'endModDetailsAuthor',
                                    fieldLabel: 'Author',
                                    name: 'author',
                                    editable: false,
                                    anchor:'96%'
                                },{
                                    xtype:'textfield',
                                    reference: 'endModDetailsClass',
                                    fieldLabel: 'Class',
                                    name: 'class',
                                    editable: false,
                                    anchor:'96%'
                                },
                                {
                                    xtype:'textfield',
                                    reference: 'endModDetailsType',
                                    fieldLabel: 'Type',
                                    name: 'type',
                                    editable: false,
                                    anchor:'96%'
                                }]
                            }

                            ]
                        }


                    ]

            }]
    
    
});
