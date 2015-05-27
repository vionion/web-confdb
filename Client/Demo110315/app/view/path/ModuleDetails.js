
Ext.define("Demo110315.view.path.ModuleDetails",{
    extend: "Ext.panel.Panel",

    viewModel: {
        type: "path-moduledetails"
    },
    
    controller: "path-moduledetails",

    alias: 'widget.moduledetails',
    
    reference: 'modDetails',
    
    paddingRight: 5,
    paddingBottom: 5,

    listeners:{
      cusDetLoaded: 'onDetLoaded'  
    },
    
    layout: 'border',
    flex: 1,
    items: [
            {
                xtype: 'form',
                region: 'center',
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
                                    reference: 'modDetailsName',
                                    fieldLabel: 'Label',
                                    name: 'label',
                                    editable: false,
//                                    bind:{
//                                        text: '{details.name}'
//                                    },
                                    anchor:'96%'
                                },
                                {
                                    xtype:'combobox',
                                    fieldLabel: 'Used in',
                                    disabled: true,
                                    name: 'usedin',
                                    anchor:'96%'
                                },
                                {
                                    xtype:'combobox',
                                    fieldLabel: 'ADD',
                                    name: 'add',
                                    disabled: true,
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
                                    reference: 'modDetailsAuthor',
                                    fieldLabel: 'Author',
                                    name: 'author',
                                    editable: false,
//                                    bind:{
//                                        text: '{details.author}'
//                                    },
                                    anchor:'96%'
                                },{
                                    xtype:'textfield',
                                    reference: 'modDetailsClass',
                                    fieldLabel: 'Class',
                                    name: 'class',
                                    editable: false,
//                                    bind:{
//                                        text: '{details.class}'
//                                    },
                                    anchor:'96%'
                                },
                                {
                                    xtype:'textfield',
                                    reference: 'modDetailsType',
                                    fieldLabel: 'Type',
                                    name: 'type',
                                    editable: false,
//                                    bind:{
//                                        text: '{details.type}'
//                                    },
                                    anchor:'96%'
                                }]
                            }

                            ]
                        }


                    ]

            }]

});
