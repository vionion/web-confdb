
Ext.define("CmsConfigExplorer.view.importconf.Import",{
    extend: "Ext.panel.Panel",
 
    requires: [
        "CmsConfigExplorer.view.importconf.ImportController",
        "CmsConfigExplorer.view.importconf.ImportModel",
        'Ext.window.MessageBox'
    ],
    
    controller: "importconf-import",
    viewModel: {
        type: "importconf-import"
    },
    
    alias: 'widget.confimport',
    
    reference: 'confimport',
    
    layout: {
        type: 'border'
    },
    
    title: 'Import a Python Menu',

    items: [
         {
            xtype: 'toolbar',
            region: 'north',
            paddingLeft: 5,
            items:[ 
                    {
                        xtype: "image",
                        src: "resources/cms-logo.png",
                        margin: '0 7 0 2',
                        width: 40, //"10%",
                        height: 40 //"80%",
                    },
                    {
                        xtype: 'tbseparator'
                    }, 
                    {
                        text: 'Home',
                        width: 70,
                        height: 30,
                        listeners: {
                            click: 'onHomeClick',
                            scope: 'controller'
                        }
                    }

                ]
         }
         ,{
             region: 'west',
             xtype: 'panel',
             header: false,
             width: '20%',
             height: '100%'
         }
         ,{
             region: 'south',
             xtype: 'panel',
             header: false,
             width: '100%',
             height: '30%'
         }
         ,{
             region: 'east',
             xtype: 'panel',
             header: false,
             width: '20%',
             height: '100%'
         }
         ,{
            region: 'center',
            xtype: 'panel',
//            border: true,
            
            items:[{
                xtype: 'form', 
                header: false,
//                width: '30%',
                height: '40%',
//                title: 'Import a Python Menu',

                listeners: {
                    cusUploadedConfiguration: 'onUploadedConfiguration',
                    scope: 'controller'
                }, 

                defaults: {
                    anchor: '100%',
                    align: 'center',
                    allowBlank: false,
                    msgTarget: 'side',
                    labelWidth: 80,
                    bodyPadding: 50
                }, 
                items: [{
                            xtype: 'filefield',
//                            id: 'form-file',
                            height: '100%',
                            margin: '20 0 10 0',
                            emptyText: 'Select a Python file',
                            fieldLabel: '<b>Python File</b>',
                            name: 'pythonfile',
                            buttonText: 'Browse...',
                            buttonConfig: {
                                iconCls: 'upload-icon',
                                margin: '0 10 0 10'
                            }
                        }],

                buttons: [{
                    text: 'Import',
                    handler: function(){
                        var form = this.up('form').getForm();
                        var win = this.up('panel');
                        var vm = this.getViewModel();
                        if(form.isValid()){
                            form.submit({
                                url: 'upload',
                                waitMsg: 'Uploading your file...',
                                success: function(fp, o) {

                                    Ext.Msg.show({
                                        title: 'Success',
                                        message: 'File, corretly processed on the server',
                                        width: 300,
                                        height: 170,
                                        buttons: Ext.Msg.OK,
                                        fn: function(btn, text){
                                            win.fireEvent( 'cusUploadedConfiguration',o.result.children[0].gid);
                                        },

                                        icon: Ext.window.MessageBox.INFO
                                    });

                                }
                            });
                        }
                    }
                },{
                    text: 'Clear',
                    handler: function() {
                        this.up('form').getForm().reset();
                    }
                }]          
            }]
            
             
         }
    ]
});
