Ext.define('CmsConfigExplorer.view.endpath.EndPathDetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.endpath-endpathdetails',
    
        onEndPatDetailsLoad: function(store, records, successful, operation, node, eOpts){
        
        var first = records[0];
        var mycolumns = [];
        var i = 0;
        var myStore={fields:[], data:[]};
        function row() {
        }
        var descArea = this.lookupReference('pathDescriptionArea');
        descArea.setValue(first.get("desc"));
            
        var preGrid = this.lookupReference('endPathPrescaleGrid');
        
        var labels = first.get('labels');
        var lLen = labels.length;
        var values = first.get('values');
        
        var name = this.lookupReference('endPatDetailsName');
        var author = this.lookupReference('endPatDetailsAuthor');
        
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
    
    onEndPatDetLoaded: function( pid,  idc, idv, online){
        this.getViewModel().getStore('endpathdetails').load({params: {pid: pid, cnf: idc, ver: idv, online:online}});
    }
    
});
