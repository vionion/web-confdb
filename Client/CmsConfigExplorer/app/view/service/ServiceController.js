
Ext.define('CmsConfigExplorer.view.service.ServiceController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.service-service',
    
    onGridSrvParamsForward: function(sid){
        
        //Ext.Msg.alert('onForward');
        //console.log('in parent, got event');
        var grid = this.lookupReference('srvParamsTree');
        var online = this.getViewModel().get("online");
        
        this.getViewModel().getStore('srvparams').load({params: {sid: sid, online:online}});
        
    },

    onRender: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        //console.log("ID CONF");
        //console.log(idc);
        
        //console.log("ID VER");
        //console.log(idv);
        
        if(idc !=-1 && idc !=-2){
            this.getViewModel().getStore('services').load({params: {cnf: idc, online:online}});
        }
        else if (idv !=-1){
            this.getViewModel().getStore('services').load({params: {ver: idv, online:online}});
        }
        else {
            //console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        this.lookupReference('servicesGrid').setLoading("Loading Services");
        
    },
    
    onServiceClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var sid = record.get("gid");
        var name = record.get("name");
        var online = this.getViewModel().get("online");
        var idv = this.getViewModel().get("idVer");
        
        //console.log('in child, fwd event');
        //console.log(sid);
        
        var serviceGrid = this.lookupReference('servicesGrid');
//        serviceGrid.fireEvent('custSrvParams',sid);
        this.getViewModel().getStore('srvparams').load({params: {sid: sid, online:online, verid:idv}});
        
        var cp = this.lookupReference("centralPanel");
        
        this.lookupReference("srvParamsTree").expand();
        
        parG = this.lookupReference("srvParamsTree");
        
        parG.setLoading("Loading Service parameters");
        parG.fireEvent( "cusTooltipActivate", parG );
        
        if(name == "PrescaleService"){
            
            //console.log("DOCKED CP LEN: ");
            //console.log(cp.items.length);
            //console.log(cp);
            if(cp.items.length < 2){

                var preTab = Ext.create({
                    xtype: 'prescaletab',
//                    hideMode : 'visibility'
                    disabled: true
                });

                cp.insert(1,preTab); 
            }
            else{
                
//                cp.getTabBar().items.items[1].setHidden(false);
//                cp.getTabBar().updateLayout();
                
                var i=0, found = false, items_length = cp.getTabBar().items.items.length;
                while(!found && i<items_length){
                    if(cp.getTabBar().items.items[i].getText() == "Prescale Table"){
                        found = true;
                    }
                    else{
                        i++;
                    }
                }
                cp.getTabBar().items.items[i].setHidden(false);
                cp.getTabBar().updateLayout();
                
            }
        }
        else {
            cp.setActiveTab(0);

            if (this.lookupReference('prescaleTab')){
                
//                cp.getTabBar().items.items[1].setHidden(true);
//                cp.getTabBar().updateLayout(); 
                
                var i=0, found = false, items_length = cp.getTabBar().items.items.length;
                while(!found && i<items_length){
                    if(cp.getTabBar().items.items[i].getText() == "Prescale Table"){
                        found = true;
                    }
                    else{
                        i++;
                    }
                }
                cp.getTabBar().items.items[i].setHidden(true);
                
//                console.log(cp.getTabBar().items.items[1]);
                cp.getTabBar().updateLayout(); 
                
            }
            
        }
        
    }

    ,onPrescaleTabRender: function(preTab){

        if(this.lookupReference("prescaleTab")){
            var dockedLen = this.lookupReference("prescaleTab").items.length;
            
            var loaded = this.getViewModel().get('prescaleLoaded');
                
            if(!loaded){    
                
                function row(pathname) {
                        this.pathname = pathname;
                }
                
                var store = this.getViewModel().getStore('srvparams');
                var dataLength = store.getCount();

                var tab = this.lookupReference("prescaleTab");
                //console.log("tab");
                //console.log(tab);
                var i = 0;
                var found = false;
                var labels = "";
                var gridLabels = [];
                var mycolumns = [];
                
                var vm_paths = this.getViewModel().get('paths');
                
                var paths_dict = {};
                for (ind = 0; ind < vm_paths.length; ind++) {
                    var p = vm_paths[ind];
                    paths_dict[p.name] = ind;
                }
                
                //GET THE LABELS PARAMETER
                while((i < dataLength) && (!found)){
                    if (store.getAt(i).get("name") == "lvl1Labels"){
                        found = true;
                    }else {
                        i++;
                    }
                }

                if((i >= dataLength) && (!found)){
                     //console.log('ERROR, LABELS NOT FOUND');
                }
                
                labels = store.getAt(i).get("rendervalue");
                var labelsLength = labels.length 
                var gotAllLabels = false;

                //RETREIVE - EXTRACT THE LABELS AND BUILD THE COLUMNS
                i = 0;
                pathColumn = {xtype: 'gridcolumn', text: 'Path',  dataIndex: 'pathname', locked: true, sortable: false, width: 350, minWidth: 300, defaultWidth: 250  };
                // autoSizeColumn: true, width: 150 ,  
                mycolumns.push(pathColumn);
                
                //--------------------------

                labels1 = labels.replace(/"/g, "");
                labels2 = labels1.replace("{", "");
                labels3 = labels2.replace("}", "");
                labels4 = labels3.replace(/ /g, "");
                
                var newlables = [];
                newlables = labels4.split(",");
                
                for (l in newlables){
                    
                    var label = newlables[l];

                    gridLabels.push(label);
                    newColumn = { xtype: 'gridcolumn', text: '',  dataIndex: '',  sortable: false, width: 100, minWidth: 100, align: 'right', 
                                 renderer: function(value, meta) { 
                                     if (parseInt(value) == 0) { 
//                                         meta.tdCls = 'prescale-zero';
                                         meta.tdAttr = 'bgcolor=#FFB0C4';
                                         return value;
                                     }else if  (parseInt(value) == 1) { 
//                                         meta.tdCls = 'prescale-one';
                                         meta.tdAttr = 'bgcolor=#B0FFC5';
                                         return value;
                                     } else if (parseInt(value) > 1) {
//                                         meta.tdCls = 'prescale-gtone';
                                         meta.tdAttr = 'bgcolor=#FFFF99';
                                         return value;
                                     } 
                                 } 
                                };
                                //flex: 1, autoSizeColumn: true, 
                    newColumn.text = label;
                    newColumn.dataIndex = label;
//                    newColumn.render = function(v, meta, rec){ return 'ciccio'};
                    mycolumns.push(newColumn);
                }
                
                //return '<b>'+value+'<\b>'
                
                //--------------------------
                
//                while((i<labelsLength) && (!gotAllLabels)){
//                    var ch = labels.charAt(i);
//
//                    if(ch == '{'){
//                        //console.log("BEGIN LABELS");
//                    }
//                    
//                    
//                    
//                    
//                    else if(ch == '\"'){
//                        //console.log("BEGIN LABEL");
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
//                                newColumn = { xtype: 'gridcolumn', text: '',  dataIndex: '',  sortable: false, width: 100, minWidth: 100};
//                                //flex: 1, autoSizeColumn: true, 
//                                newColumn.text = label;
//                                newColumn.dataIndex = label;
//                                newColumn.render = function(v, meta, rec){ return 'ciccio'};
//                                mycolumns.push(newColumn);
//                                
//                                //console.log("FINISH LABEL");
//                                //console.log(label);
//                                done = true;
//                            }else{
//                                i++;
//                            }
//                        }
//                    }else if(ch == '}'){
//                        //console.log("FINISH LABELS");
//                        gotAllLabels = true;
//                    }
//                    else if(ch == ','){
//                        //console.log("MORE LABELS");
//                    }
//
//                    i++;
//                }
                
                //GET THE VPSET WITH THE PRESCALE TABLE
                i = 0;
                found = false;
                var myStore={fields:[], data:[]};
                while((i < dataLength) && (!found)){
                    if (store.getAt(i).get("name") == "prescaleTable"){
                        //console.log("LVL1: ");
                        //console.log(store.getAt(i).get("name"));
                        found = true;
                    }else {
                        i++;
                    }
                }
                if((i >= dataLength) && (!found)){
                     //console.log('ERROR, PRESCALE TABLE NOT FOUND');
                }
                
                var preTable = store.getAt(i);
                
                if(!preTable.hasChildNodes()){
                     //console.log('ERROR, PRESCALE TABLE EMPTY');
                }else{
                     
                    childrenLen = preTable.childNodes.length;
                    var child = null;
                    var pat_index = -1
                    
                    for(i=0;i<childrenLen;i++){
                        child = preTable.getChildAt(i);
                        
                        var path_name = child.getChildAt(0).data.rendervalue.replace(/\"/g,"");
                        
                        pat_index = paths_dict[path_name]
                        paths_dict[path_name] = -2;
                        var myRow = new row(path_name);  //("\"",""));   
                        
//                        row.pathname = child.getChildAt(0).data.value;
                        var prescaleArray = child.getChildAt(1).data.rendervalue;
//                        var splitted = prescaleArray.split(" ");
                        
                        var prescaleArray1 = prescaleArray.replace(/"/g, "");
                        var prescaleArray2 = prescaleArray1.replace(/ /g, "");
                        var prescaleArray3 = prescaleArray2.replace("}", "");
                        var prescaleArray4 = prescaleArray3.replace("{", "");

                        var splitted = prescaleArray4.split(",");
                        
                        var splittedLen = splitted.length;
                        var i2 = 0;
                        var values = [];
                        for(;i2<splittedLen;i2++){
                            var splitItem = splitted[i2];

                            if((splitItem.charAt(0)=='{') || (splitItem.search("}")!=-1) ){
                                
                            }
                            else{
//                                splitItem = splitItem.replace(",","");
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
                        var to = vm_paths[pat_index]
                        if(!to){
                            myRow.order = 10000
                        }
                        else {
                            myRow.order = to.order
                        }
                        
                        myStore.data.push(myRow);
                    }
                    
                    for(p in paths_dict) {
                        
                        if (paths_dict[p] != -2){
                            var myRow = new row(p);
                            
                            i2 = 0;
                            var gl = gridLabels.length    
                            for(;i2<gl;i2++){
                                var currLabel = gridLabels[i2];
                                myRow[currLabel] = 1;
                            }
                            myRow.order = vm_paths[paths_dict[p]].order
                            myStore.data.push(myRow);

                        }
                            
                    }
 
                }
//                var preGrid = this.lookupReference("prescaleTab").lookupReference("prescaleGrid");
//                preGrid.setVisible(false);
//                preGrid.disable();
                var preGrid = Ext.create('Ext.grid.Panel',{
//                        xtype: 'grid',
                    
                        requires: [
                            'Ext.grid.selection.SpreadsheetModel',
                            'Ext.grid.plugin.Clipboard'
                        ],
                    
                        plugins: 'clipboard',
                        
                        reference: 'prescaleGrid',
                        region: 'center',
//                        flex: 1,
//                        layout: 'fit',
                        loadMask: true,
                        trackOver: false,
                        enableColumnMove : false,
                        
//                        viewConfig: {
//                            getRowClass: function(record, index) {
////                                var c = record.get('change');
//                                console.log(record.getFields());
//                                
////                                if (c == 0) {
////                                    return 'prescale-zero';
////                                } else if (c == 1) {
////                                    return 'prescale-one';
////                                } else if (c > 1) {
////                                    return 'prescale-gtone';
////                                }
//                            }
//                        },
                    
                        lockedGridConfig:{
                            minWidth: 300, 
                            defaultWidth: 300
                        },
                        
                        listeners: {
                            selectionchange: 'onSelectionChange'
//                            show: 'onPrescaleShow'
                        },    
                        
                        selModel: {
                            type: 'spreadsheet',
                            // Disables sorting by header click, though it will be still available via menu
                            columnSelect: true,            
                //                checkboxSelect: true,
                //                checkboxColumnIndex: 'last', 
                            pruneRemoved: false
                        },
                    
                        dockedItems: [{
                            xtype: 'toolbar',
                            reference: 'prescaleTabHeaderTooolBar',
                            dock: 'top',

                            items: [
                                { 
                                    xtype: 'tbtext',
                                    text: '<b>Prescales Tab</b>'
                                },
                                {
                                    xtype: 'tbseparator'
                                },
                                {
                                    labelWidth: 80,
                                    xtype: 'textfield',
                                    fieldLabel: 'Paths search',
                                    reference: 'pretrigfield',
                    //                triggerWrapCls: 'x-form-clear-trigger',
                                    triggers:{
                                        search: {
                                            reference: 'triggerSearch',
                                            cls: 'x-form-clear-trigger',
                                            handler: 'onPathPrescaleTriggerClick',
                                            listeners: {
                                                change: 'onPathPrescaleSearchChange'

                                            }
                                        }
                                    }, 
                                    listeners: {
                                        change: 'onPathPrescaleSearchChange'

                                    }
                                }
                                ,{
                                    xtype: 'displayfield',
                                    reference: 'preMatches',
                                    fieldLabel: 'Matches',

                                    // Use shrinkwrap width for the label
                                    labelWidth: null
//                                    listeners: {
//                                        beforerender: function() {
//                                            var me = this,
//                                                tree = me.up('gridpanel'),
//                                                root = tree.getRootNode(),
//                                                leafCount = 0;
//
//                                            tree.store.on('fillcomplete', function(store, node) {
//                                                if (node === root) {
//                                                    root.visitPostOrder('', function(node) {
//                                                        if (node.isLeaf()) {
//                                                            leafCount++;
//                                                        }
//                                                    });
//                                                    me.setValue(leafCount);
//                                                }
//                                            });
//                                        },
//                                        single: true
//                                    }
                                },
                                '-',
                                {
                                    xtype: 'tbtext',
//                                    text: '<b>Prescales Tab</b>'
//                                    xtype: 'component',
                                    html: 'Selectable: '
                                }, 
                                {
                                    text: 'Cells',
                                    enableToggle: true,
                                    toggleHandler: 'toggleCellSelect',
                                    pressed: true
                                }, 
                                {
                                    text: 'Columns',
                                    enableToggle: true,
                                    toggleHandler: 'toggleColumnSelect',
                                    pressed: true
                                }, 
                                    '->', 
                                {
                                    xtype: 'component',
                                    reference: 'status'
                                }
                            ]
                        }],
                    
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
                
                myStore.data.sort(function(a, b){return a.order - b.order});
                
                myStore.fields = gridLabels;
//                preGrid.enableLocking = true;
                
                //console.log('before reco');
                preGrid.reconfigure(myStore,mycolumns);
                //console.log('after reco');
                
                Ext.resumeLayouts(true);
                //console.log('after res');
//                preGrid.setConfig( 'scrollable', true ); 
//                console.log('after setc');
                
//                preGrid = this.lookupReference("prescaleTab").lookupReference("prescaleGrid");
//                console.log(preGrid);
                
//                preGrid.enable();
//                preGrid.setVisible(true);
                
//                preGrid.reconfigure(myStore,null);
                this.getViewModel().set('prescaleLoaded',true);
                this.lookupReference("prescaleTab").insert(1,preGrid);
                
                this.lookupReference('prescaleTab').enable();
                
            }

        }
     
    }
    
//    ,onPreGridRender: function(preGrid){
//     
//        preGrid.setConfig({ enableLocking:true}) ;
//    }
    ,onSrvparamsLoad: function(store, records, successful, operation, node, eOpts) {
        var id = operation.config.node.get('gid')
        if (id == -1){
           operation.config.node.expand() 
        }
        
//        this.lookupReference("srvParamsTree").setLoading(false);
        if(this.lookupReference('srvParamsTree').isMasked()){
            this.lookupReference('srvParamsTree').setLoading(false);
        }

    }
    
    ,onServicesLoad: function(store, records, successful, operation, node, eOpts){
//                    this.getViewModel().getStore('pathitems').getRoot().expand();
                    
        var root_vid  =  store.getRoot().get('vid');
        //console.log("ROOT_VID: ");
        //console.log(root_vid);

        //Check if Version id in Root is still default: set Version id in Root
        if(root_vid == -1){
            //Check if The path list is empty
            if(records.length > 0){

                    //console.log(records[0].get('vid'));
                    var verId = records[0].get('vid');
                    store.getRoot().set('vid',verId);
                    //console.log("NEW ROOT_VID: ");
                    //console.log(root_vid);
                }
        }

        store.getRoot().expand();
        
        if(this.lookupReference('servicesGrid').isMasked()){
            this.lookupReference('servicesGrid').setLoading(false);
        }
        
    }
    
//    ,getSelectionModel: function () {
//        var grid = this.getView().lookupReference('prescaleGrid');
//        return grid.getSelectionModel();
//    }
//    
//    ,onSelectionChange: function (grid, selection) {
//        var status = this.lookupReference('status'),
//            message = '??',
//            firstRowIndex,
//            firstColumnIndex,
//            lastRowIndex,
//            lastColumnIndex;
//
//        if (!selection) {
//            message = 'No selection';
//        }
//        else if (selection.isCells) {
//            firstRowIndex = selection.getFirstRowIndex();
//            firstColumnIndex = selection.getFirstColumnIndex();
//            lastRowIndex = selection.getLastRowIndex();
//            lastColumnIndex = selection.getLastColumnIndex();
//
//            message = 'Selected cells: ' + (lastColumnIndex - firstColumnIndex + 1) + 'x' + (lastRowIndex - firstRowIndex + 1) +
//                ' at (' + firstColumnIndex + ',' + firstRowIndex + ')';
//        }
//        else if (selection.isRows) {
//            message = 'Selected rows: ' + selection.getCount();
//        }
//        else if (selection.isColumns) {
//            message = 'Selected columns: ' + selection.getCount();
//        }
//
//        status.update(message);
//    },
//    
//    toggleCellSelect: function(button, pressed) {
//        var sel = this.getSelectionModel();
//        sel.setCellSelect(pressed);
//    },
//
//    toggleColumnSelect: function(button, pressed) {
//        var sel = this.getSelectionModel();
//        sel.setColumnSelect(pressed);
//    }
    
});






























