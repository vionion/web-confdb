Ext.define('Demo110315.view.globalpset.GlobalPsetController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.globalpset-globalpset',
    
//    onGridSrvParamsForward: function(sid){
//        
//        //Ext.Msg.alert('onForward');
//        console.log('in parent, got event');
//        var grid = this.lookupReference('srvParamsTree');
//        
//        this.getViewModel().getStore('srvparams').load({params: {sid: sid}});
//        
//    },
    
    onRender: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        console.log("ID CONF");
        console.log(idc);
        
        console.log("ID VER");
        console.log(idv);
        
        if(idc !=-1){
            this.getViewModel().getStore('gpsets').load({params: {cnf: idc}});
        }
        else if (idv !=-1){
            this.getViewModel().getStore('gpsets').load({params: {ver: idv}});
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    onGpsetClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var sid = record.get("gid");
//        var name = record.get("name");
        
        console.log('in child, fwd event');
        console.log(sid);
        
//        var serviceGrid = this.lookupReference('gpsettree');
//        serviceGrid.fireEvent('custSrvParams',sid);
        this.getViewModel().getStore('gpsetparams').load({params: {gid: sid}});
        
        var cp = this.lookupReference("centralGpsetPanel");
        
        this.lookupReference("gpsetParamsTree").expand();
        
    }

//    ,onPrescaleTabRender: function(preTab){
//
//        if(this.lookupReference("prescaleTab")){
//            var dockedLen = this.lookupReference("prescaleTab").items.length;
//            console.log("dockedLen");
//            console.log(dockedLen);
//            
//            if(dockedLen < 2){
//                
//                function row(pathname) {
//                        this.pathname = pathname;
//                }
//                
//                var store = this.getViewModel().getStore('srvparams');
//                var dataLength = store.getCount();
//                console.log("isLoaded");
//                console.log(this.getViewModel().getStore('srvparams').isLoaded());
//
//                console.log("dataLength");
//                console.log(dataLength);
//
//                var tab = this.lookupReference("prescaleTab");
//                console.log("tab");
//                console.log(tab);
//                var i = 0;
//                var found = false;
//                var labels = "";
//                var gridLabels = [];
//                var mycolumns = [];
//                
//                //GET THE LABELS PARAMETER
//                while((i < dataLength) && (!found)){
//                    if (store.getAt(i).get("name") == "lvl1Labels"){
//                        console.log("LVL1: ");
//                        console.log(store.getAt(i).get("name"));
//                        found = true;
//                    }else {
//                        i++;
//                    }
//                }
//
//                if((i >= dataLength) && (!found)){
//                     console.log('ERROR, LABELS NOT FOUND');
//                }
//                
//                labels = store.getAt(i).get("value");
//                var labelsLength = labels.length 
//                var gotAllLabels = false;
//
//                //RETREIVE - EXTRACT THE LABELS AND BUILD THE COLUMNS
//                i = 0;
//                pathColumn = { xtype: 'gridcolumn', text: 'Path',  dataIndex: 'pathname' , flex: 2};
//                mycolumns.push(pathColumn);
//                
//                while((i<labelsLength) && (!gotAllLabels)){
//                    var ch = labels.charAt(i);
//
//                    if(ch == '{'){
//                        console.log("BEGIN LABELS");
//                    }
//                    else if(ch == '\"'){
//                        console.log("BEGIN LABEL");
//                        var done = false;
//                        i++;
//                        var beginLabelIndex = i;
//                        var label = "";
//                        while(!done){
//
//                            if (labels.charAt(i) == '\"'){
//                                label = labels.slice(beginLabelIndex,i);
//                                gridLabels.push(label);
//
//                                newColumn = { xtype: 'gridcolumn', text: '',  dataIndex: ''};
//                                newColumn.text = label;
//                                newColumn.dataIndex = label;
//                                mycolumns.push(newColumn);
//                                
//                                console.log("FINISH LABEL");
//                                console.log(label);
//                                done = true;
//                            }else{
//                                i++;
//                            }
//                        }
//                    }else if(ch == '}'){
//                        console.log("FINISH LABELS");
//                        gotAllLabels = true;
//                    }
//                    else if(ch == ','){
//                        console.log("MORE LABELS");
//                    }
//
//                    i++;
//                }
//                
//                //GET THE VPSET WITH THE PRESCALE TABLE
//                i = 0;
//                found = false;
//                var myStore={fields:[], data:[]};
//                while((i < dataLength) && (!found)){
//                    if (store.getAt(i).get("name") == "prescaleTable"){
//                        console.log("LVL1: ");
//                        console.log(store.getAt(i).get("name"));
//                        found = true;
//                    }else {
//                        i++;
//                    }
//                }
//                if((i >= dataLength) && (!found)){
//                     console.log('ERROR, PRESCALE TABLE NOT FOUND');
//                }
//                
//                var preTable = store.getAt(i);
//                
//                if(!preTable.hasChildNodes()){
//                     console.log('ERROR, PRESCALE TABLE EMPTY');
//                }else{
//                     
//                    childrenLen = preTable.childNodes.length;
//                    var child = null;
//                    
//                    for(i=0;i<childrenLen;i++){
//                        child = preTable.getChildAt(i);
//                        
//                        var myRow = new row(child.getChildAt(0).data.value.replace(/\"/g,""));  //("\"","")); 
////                        row.pathname = child.getChildAt(0).data.value;
//                        var prescaleArray = child.getChildAt(1).data.value;
//                        var splitted = prescaleArray.split(" ");
//                        var splittedLen = splitted.length;
//                        var i2 = 0;
//                        var values = [];
//                        for(;i2<splittedLen;i2++){
//                            var splitItem = splitted[i2];
//                            if((splitItem.charAt(0)=='{') || (splitItem.search("}")!=-1) ){
//                                
//                            }
//                            else{
//                                splitItem = splitItem.replace(",","");
//                                values.push(splitItem);
//                            }
//                        }
//                        var valuesLen = values.length;
//                        i2 = 0;
//                        for(;i2<valuesLen;i2++){
//                            var currLabel = gridLabels[i2];
////                            row[currLabel] = values[i2];
//                            myRow[currLabel] = values[i2];
//                        }
//                        myStore.data.push(myRow);
//                    }
//                    
//                }
//                
//                var preGrid = Ext.create({
//                        xtype: 'grid',
//                        reference: 'prescaleGrid',
//                        flex: 2,
//                        layout: 'fit',
//                        loadMask: true,
//                        width: '100%',
//                        height: '75%',
//                        scrollable: true, 
//                        columns:[],
//                        store: {}
//                    });
//                gridLabels.unshift("Path");
//                myStore.fields = gridLabels;
//                preGrid.reconfigure(myStore,mycolumns);
//                
//                this.lookupReference("prescaleTab").insert(1,preGrid);
//                
//            }
//        }
//        
//        
//    }
    
    
});
