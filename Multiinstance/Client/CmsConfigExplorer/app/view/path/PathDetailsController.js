Ext.define('CmsConfigExplorer.view.path.PathDetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.path-pathdetails',
    
    onPatDetailsLoad: function(store, records, successful, operation, node, eOpts){
        
        var first = records[0];
        var mycolumns = [];
        var i = 0;
        var myStore={fields:[], data:[]};
        function row() {
        }
        var descArea = this.lookupReference('pathDescriptionArea');
        descArea.setValue(first.get("desc"));
        
        var preGrid = this.lookupReference('pathPrescaleGrid');
        
//        var preGrid = Ext.create({
//                        xtype: 'grid',
//                        reference: 'pathPrescaleGrid',
//                        flex: 2,
//                        layout: 'fit',
//                        loadMask: true,
//                        width: '100%',
////                        height: '75%',
//                        scrollable: true, 
//                        columns:[],
//                        store: {}
//                    });
//        
//        var desc = Ext.create({
//            xtype: 'textarea',
////            flex:1,
//            fieldLabel: 'Description',
//            labelAlign: 'top'
//        });
        
        var labels = first.get('labels');
        var lLen = labels.length;
        var values = first.get('values');
        
        var name = this.lookupReference('patDetailsName');
        var author = this.lookupReference('patDetailsAuthor');
        
        name.setValue( first.get('name') );
        author.setValue( first.get('author') );
        
        var myRow = new row();
        
        for (;i<lLen;i++){
            newColumn = { xtype: 'gridcolumn', text: '',  dataIndex: ''};
            var lab = labels[i];
            newColumn.text = lab;
            newColumn.dataIndex = lab;
            mycolumns.push(newColumn);
            
            myRow[lab] = values[i];
        }
        myStore.fields = labels;
        myStore.data.push(myRow);
        
        preGrid.reconfigure(myStore,mycolumns);
        this.getView().insert(1,preGrid); //("pathDetailsPanel")
//        this.getView().insert(2,desc); //("pathDetailsPanel")
        this.getView().setHeight('50%');
        preGrid.setTitle(first.get('name'));
        //console.log(this.getView());
        
    },
    
    onPatDetLoaded: function( pid,  idc, idv, online){
        this.getViewModel().getStore('pathdetails').load({params: {pid: pid, cnf: idc, ver: idv, online:online}});
    }
    
});
