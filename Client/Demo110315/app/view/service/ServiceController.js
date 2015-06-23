
Ext.define('Demo110315.view.service.ServiceController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.service-service',
    
    onGridSrvParamsForward: function(sid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('srvParamsTree');
        
        this.getViewModel().getStore('srvparams').load({params: {sid: sid}});
        
    },

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
            this.getViewModel().getStore('services').load({params: {cnf: idc}});
        }
        else if (idv !=-1){
            this.getViewModel().getStore('services').load({params: {ver: idv}});
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    onServiceClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var sid = record.get("gid");
        var name = record.get("name");
        
        console.log('in child, fwd event');
        console.log(sid);
        
        var serviceGrid = this.lookupReference('servicesGrid');
//        serviceGrid.fireEvent('custSrvParams',sid);
        this.getViewModel().getStore('srvparams').load({params: {sid: sid}});
        
        var cp = this.lookupReference("centralPanel");
        
        this.lookupReference("srvParamsTree").expand();
        
        if(name == "PrescaleService"){
            
            console.log("DOCKED CP LEN: ");
            console.log(cp.items.length);
            console.log(cp);
            if(cp.items.length < 2){

                var preTab = Ext.create({
                    xtype: 'prescaletab'
                });

                cp.insert(1,preTab); 
            }
        }
        else {
            cp.setActiveTab(0); 
        }
        
    }

    ,onPrescaleTabRender: function(preTab){

        if(this.lookupReference("prescaleTab")){
            var dockedLen = this.lookupReference("prescaleTab").items.length;
            console.log("dockedLen");
            console.log(dockedLen);
            
            var loaded = this.getViewModel().get('prescaleLoaded');
            console.log("prescaleLoaded");
            console.log(loaded);
            
//            if(dockedLen < 3 && parG_Cols < 2){
                
            if(!loaded){    
                
                function row(pathname) {
                        this.pathname = pathname;
                }
                
                var store = this.getViewModel().getStore('srvparams');
                var dataLength = store.getCount();
                console.log("isLoaded");
                console.log(this.getViewModel().getStore('srvparams').isLoaded());

                console.log("dataLength");
                console.log(dataLength);

                var tab = this.lookupReference("prescaleTab");
                console.log("tab");
                console.log(tab);
                var i = 0;
                var found = false;
                var labels = "";
                var gridLabels = [];
                var mycolumns = [];
                
                //GET THE LABELS PARAMETER
                while((i < dataLength) && (!found)){
                    if (store.getAt(i).get("name") == "lvl1Labels"){
                        console.log("LVL1: ");
                        console.log(store.getAt(i).get("name"));
                        found = true;
                    }else {
                        i++;
                    }
                }

                if((i >= dataLength) && (!found)){
                     console.log('ERROR, LABELS NOT FOUND');
                }
                
                labels = store.getAt(i).get("value");
                var labelsLength = labels.length 
                var gotAllLabels = false;

                //RETREIVE - EXTRACT THE LABELS AND BUILD THE COLUMNS
                i = 0;
                pathColumn = {xtype: 'gridcolumn', text: 'Path',  dataIndex: 'pathname', locked: true, sortable: false, width: 150, minWidth: 150 };
                // autoSizeColumn: true, width: 150 ,  
                mycolumns.push(pathColumn);
                
                while((i<labelsLength) && (!gotAllLabels)){
                    var ch = labels.charAt(i);

                    if(ch == '{'){
                        console.log("BEGIN LABELS");
                    }
                    else if(ch == '\"'){
                        console.log("BEGIN LABEL");
                        var done = false;
                        i++;
                        var beginLabelIndex = i;
                        var label = "";
                        while(!done){

                            if (labels.charAt(i) == '\"'){
                                label = labels.slice(beginLabelIndex,i);
                                gridLabels.push(label);

                                newColumn = { xtype: 'gridcolumn', text: '',  dataIndex: '', width: 100, minWidth: 100};
                                //flex: 1, autoSizeColumn: true, 
                                newColumn.text = label;
                                newColumn.dataIndex = label;
                                newColumn.render = function(v, meta, rec){ return 'ciccio'};
                                mycolumns.push(newColumn);
                                
                                console.log("FINISH LABEL");
                                console.log(label);
                                done = true;
                            }else{
                                i++;
                            }
                        }
                    }else if(ch == '}'){
                        console.log("FINISH LABELS");
                        gotAllLabels = true;
                    }
                    else if(ch == ','){
                        console.log("MORE LABELS");
                    }

                    i++;
                }
                
                //GET THE VPSET WITH THE PRESCALE TABLE
                i = 0;
                found = false;
                var myStore={fields:[], data:[]};
                while((i < dataLength) && (!found)){
                    if (store.getAt(i).get("name") == "prescaleTable"){
                        console.log("LVL1: ");
                        console.log(store.getAt(i).get("name"));
                        found = true;
                    }else {
                        i++;
                    }
                }
                if((i >= dataLength) && (!found)){
                     console.log('ERROR, PRESCALE TABLE NOT FOUND');
                }
                
                var preTable = store.getAt(i);
                
                if(!preTable.hasChildNodes()){
                     console.log('ERROR, PRESCALE TABLE EMPTY');
                }else{
                     
                    childrenLen = preTable.childNodes.length;
                    var child = null;
                    
                    for(i=0;i<childrenLen;i++){
                        child = preTable.getChildAt(i);
                        
                        var myRow = new row(child.getChildAt(0).data.value.replace(/\"/g,""));  //("\"","")); 
//                        row.pathname = child.getChildAt(0).data.value;
                        var prescaleArray = child.getChildAt(1).data.value;
                        var splitted = prescaleArray.split(" ");
                        var splittedLen = splitted.length;
                        var i2 = 0;
                        var values = [];
                        for(;i2<splittedLen;i2++){
                            var splitItem = splitted[i2];
                            if((splitItem.charAt(0)=='{') || (splitItem.search("}")!=-1) ){
                                
                            }
                            else{
                                splitItem = splitItem.replace(",","");
                                values.push(splitItem);
                            }
                        }
                        var valuesLen = values.length;
                        i2 = 0;
                        for(;i2<valuesLen;i2++){
                            var currLabel = gridLabels[i2];
//                            row[currLabel] = values[i2];
                            myRow[currLabel] = values[i2];
                        }
                        myStore.data.push(myRow);
                    }
                    
                }
//                var preGrid = this.lookupReference("prescaleTab").lookupReference("prescaleGrid");
//                preGrid.setVisible(false);
//                preGrid.disable();
                var preGrid = Ext.create('Ext.grid.Panel',{
//                        xtype: 'grid',
                        reference: 'prescaleGrid',
                        region: 'center',
//                        flex: 1,
//                        layout: 'fit',
                        loadMask: true,
//                        width: '100%',
//                        height: '75%',
//                        scrollable: true,
                        columnLines: true,
                        enableLocking: true,
                        columns:[],
                        store: {}
//                        ,listeners:{
//                                render: 'onPreGridRender',
//                                beforeshow: 'onPreGridRender'
//                        }
                    });
                gridLabels.unshift("Path");
                myStore.fields = gridLabels;
//                preGrid.enableLocking = true;
                
                console.log('before reco');
                preGrid.reconfigure(myStore,mycolumns);
                console.log('after reco');
                
                Ext.resumeLayouts(true);
                console.log('after res');
//                preGrid.setConfig( 'scrollable', true ); 
//                console.log('after setc');
                
//                preGrid = this.lookupReference("prescaleTab").lookupReference("prescaleGrid");
//                console.log(preGrid);
                
//                preGrid.enable();
//                preGrid.setVisible(true);
                
//                preGrid.reconfigure(myStore,null);
                this.getViewModel().set('prescaleLoaded',true);
                this.lookupReference("prescaleTab").insert(1,preGrid);
                
            }

        }
        
        
    }
    
//    ,onPreGridRender: function(preGrid){
//     
//        preGrid.setConfig({ enableLocking:true}) ;
//    }
    
    
});






























