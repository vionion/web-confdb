
Ext.define("Demo110315.view.path.Path",{
    extend: "Ext.panel.Panel",
    
    requires:['Demo110315.model.Moduleitem',
             'Demo110315.model.Pathitem',
             'Demo110315.view.path.Parameters',
             'Demo110315.view.path.Pathtree',
             'Demo110315.view.path.ModuleDetails',
             'Demo110315.view.path.PathDetails'],
    
    alias:'widget.pathtab',
    
    reference: "pathtab",
    
    controller: "path-path",
    viewModel: {
        type: "path-path"
    },

    layout: {
        type: 'border'
    },
    
//    listeners:{
//        custSetVerId: 'onSetVerId'
//    },
    
    items: [
        {
            xtype: 'toolbar',
            region: 'north',
            paddingLeft: 5,
            items:[ 
                    {
                        xtype: 'textfield',
                        fieldLabel: 'Search',
                        labelWidth: 47,
                        enableKeyEvents: true,
                        disabled: true
                    }
                ]
        },
        {
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'pathtree',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            viewConfig: {
                loadingHeight: 100
            },
            listeners:{
                rowclick: 'onNodeClick',
                custModParams: 'onModParamsForward',
//                custPatDet: 'onPatDetForward',
                render: 'onRender',
                beforeshow: 'onRender'
                //scope: 'controller'
        }

    },
    {
        region: 'center',
        xtype: 'panel',
        reference: "centralPanel",
        header: false,
        split: true,
        height: '100%',
        
        layout:{
            type:  'card'
//            align: 'stretch'
        },
        
        items:[
            {
                xtype: 'container',
                layout:{
                    type: 'vbox',
                    align: 'stretch'
                },
                items:[
                    {
                        xtype: 'moduledetails',
        //                width: '100%',
                        height: '25%',
                        title: 'Module Details',
                        collapsible: true,
                        split: true
                    },
                    {
                        xtype: 'parameters',
                        split: true,
                        flex: 2,
        //                layout: 'fit',
                        loadMask: true,
        //                width: '100%',
                        height: '75%'
                    }
                    
                ]
                
            },
            {            
                xtype: 'pathdetails',
//                hidden: true,
                split: true,
                title: 'Path Details',
                height: '100%'          
            }
        ]
        
    }    
    ]

});





//{
//        region: 'center',
//        collapsible: true,
//        xtype: 'moduledetails',
//        width: '100%',
//        height: '25%'
//    },{
//        region: 'south',
////        layout: 'fit',
//        xtype: 'parameters',
//        split: true,
//        height: '100%',
//        width: '50%',
//        loadMask: true
//        
//    }
