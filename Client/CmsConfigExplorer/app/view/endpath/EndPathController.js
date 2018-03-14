Ext.define('CmsConfigExplorer.view.endpath.EndPathController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.endpath-endpath',
    
    onEndRender: function(){
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
            this.getViewModel().getStore('endpathitems').load({params: {cnf: idc, online:online}});
            view = this.getView();
            
            view.fireEvent( "cusEndPathTabRender", idc, idv, online);
        }
        else if (idv !=-1){
            this.getViewModel().getStore('endpathitems').load({params: {ver: idv, online:online}});
            view = this.getView();
            view.fireEvent( "cusEndPathTabRender", idc, idv, online);
        }
        else {
            //console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        var spgrid  = this.lookupReference("endSpGrid");
        spgrid.hide();
    },
    
    onEndModParamsForward: function(mid,pid){
        
        //Ext.Msg.alert('onForward');
        //console.log('in parent, got event');
        var grid = this.lookupReference('paramGrid');
        var online = this.getViewModel().get("online");
        var idv = this.getViewModel().get("idVer");
        
        //var cid = this.getViewModel().get('currentModule').id;
        this.getViewModel().getStore('parameters').load({params: {mid: mid, pid: pid, epit: "mod", online:online, verid:idv}});
        
        grid.setLoading("Modules parameters loading");
        
        var form = this.lookupReference('endModDetails');
        form.fireEvent( "cusEndDetLoaded", mid, pid, online, idv);
        
        //console.log(form);
        
        grid.fireEvent( "cusTooltipActivate", grid );
        
    },
    
    onEndOumModParamsForward: function(mid,pid){
        
        //Ext.Msg.alert('onForward');
        //console.log('in parent, got event');
        var grid = this.lookupReference('paramGrid');
        var online = this.getViewModel().get("online");
        var idv = this.getViewModel().get("idVer");
        
        //var cid = this.getViewModel().get('currentModule').id;
        this.getViewModel().getStore('parameters').load({params: {mid: mid, pid: pid, epit: "oum", online:online, verid:idv}});
        
        grid.setLoading("Output Modules parameters loading");
        
        var form = this.lookupReference('endModDetails');
        form.fireEvent( "cusEndOumDetLoaded", mid, pid, online, idv);
        
        grid.fireEvent( "cusTooltipActivate", grid );
        
        //console.log(form);

    },
    
    onEndPatDetForward: function(pid){
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        var form = this.lookupReference('endPathDetailsPanel');
        form.fireEvent( "cusEndPatDetLoaded", pid,  idc, idv, online);
        //console.log("cusEndPatDetLoaded FIRED");
        //console.log(form);
    },
    
    onPathColumnNameHeaderClickForward: function( ct, column, e, t, eOpts ){
        
        var store = this.getViewModel().getStore('endpathitems');        
        
        if (this.getViewModel().get('sortToogle')){
            //Sort By order
            
            var sorter = Ext.create('Ext.util.Sorter',{
                sorterFn: function(record1, record2) {
                    var ord1 = record1.data.order;
                    var ord2 = record2.data.order;

                    return ord1 > ord2 ? 1 : -1;
                },
//                    property: 'order',
                direction: 'ASC'
            });
            
            var sorters = [];
            sorters.push(sorter);
            
            store.setSorters(sorters);
            store.sort('sorterFn');
            
            this.getViewModel().set('sortToogle',false);
        }
        else{
            //Sort By Name
            
            var sorter = Ext.create('Ext.util.Sorter',{
                sorterFn: function(record1, record2) {
                var pit1 = record1.data.pit;
                var pit2 = record2.data.pit;

                if (pit1 == 'pat' && pit2 == 'pat') {

                    var name1 = record1.data.name;
                    var name2 = record2.data.name;

                    return name1 > name2 ? 1 : (name1 === name2) ? 0 : -1;
                }
                else {
                    var ord1 = record1.data.order;
                    var ord2 = record2.data.order;

                    return ord1 > ord2 ? 1 : -1;
                    }
                },
                direction: 'ASC'
            });
            
            var sorters = [];
            sorters.push(sorter);
            
            store.setSorters(sorters);
            store.sort('sorterFn');
            
            this.getViewModel().set('sortToogle',true);
        }
            
        
    },
    
    onEndNodeClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var pathView = this.getView();
        var central = this.lookupReference('endCentralPanel');
        var centralLayout = central.getLayout(); 
        var item_type = record.get("pit");
        
        var form = this.lookupReference('endModDetails');
        var params = this.lookupReference('paramGrid');
        var pathDet = this.lookupReference('endPathDetailsPanel');
        var online = this.getViewModel().get("online");
        
        var spgrid  = this.lookupReference("endSpGrid");
        
        if(item_type == "mod"){
            
            centralLayout.setActiveItem(0);

            var mid = record.get("gid");
            var pid = record.get("id_pathid");

            //console.log('in child, fwd event');
            //console.log(mid);
            var view = this.lookupReference('endpathTree');
            view.fireEvent('cusEndModParams',mid, pid,online);
        }
        else if(item_type == "oum"){
            
//            this.lookupReference("endCentralContainer").this.lookupReference("endSpGrid").hide();
            spgrid.hide(); 
            
            centralLayout.setActiveItem(0);

            var mid = record.get("gid");
            var pid = record.get("id_pathid");

            //console.log('in child, fwd event');
            //console.log(mid);
            var view = this.lookupReference('endpathTree');
            view.fireEvent('cusEndOumModParams',mid, pid, online);
        }
        else if(item_type == "pat"){
            
            spgrid.hide();
            
            var idc = this.getViewModel().get("idCnf");
            var idv = this.getViewModel().get("idVer");
            var pid = record.get("gid");

            pathDet.fireEvent( "cusEndPatDetLoaded", pid,  idc, idv, online);
            //console.log("cusEndPatDetLoaded FIRED");
            
            centralLayout.setActiveItem(1);
        }
        
    }
    
    ,onEndPathitemsLoad: function( store, records, successful, eOpts ){
        
//        if(this.lookupReference('endpathTree').isMasked()){
//            this.lookupReference('endpathTree').unmask();
//        }
        
        if(this.lookupReference('endpathTree').isMasked()){
            this.lookupReference('endpathTree').setLoading( false );
        }
        
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

//                    store.fireEvent('custSetVerId', verId);
        store.getRoot().expand();
    },
    
    onEndPathitemsBeforeLoad: function(store, operation, eOpts) {

        var pi_type = operation.config.node.get('pit');
        var online = this.getViewModel().get("online");
        
        operation.getProxy().setExtraParam('itype',pi_type);
        
        operation.getProxy().setExtraParam('online',online);
        //console.log(store.getRoot().get('vid'));
        operation.getProxy().setExtraParam('ver',store.getRoot().get('vid')); //operation.config.node.get('pit')
        
//        this.lookupReference('endpathTree').mask();
        
        this.lookupReference('endpathTree').setLoading( "Loading End Paths" );
    },
    
    onSortAlphaPaths: function(){
        
        var store = this.getViewModel().getStore('endpathitems');      
        
        var sorter = Ext.create('Ext.util.Sorter',{
            sorterFn: function(record1, record2) {
            var pit1 = record1.data.pit;
            var pit2 = record2.data.pit;

            if (pit1 == 'pat' && pit2 == 'pat') {

                var name1 = record1.data.Name;
                var name2 = record2.data.Name;

                return name1 > name2 ? 1 : (name1 === name2) ? 0 : -1;
            }
            else {
                var ord1 = record1.data.order;
                var ord2 = record2.data.order;

                return ord1 > ord2 ? 1 : -1;
                }
            },
            direction: 'ASC'
        });

        var sorters = [];
        sorters.push(sorter);
        
        store.setSorters(sorters);
        store.sort('sorterFn');
        
        var pathTree = this.lookupReference('endpathTree');
        var tool = pathTree.lookupReference('endPathHeaderTooolBar');

        var alphaButton = tool.items.getAt(2); 
        var origButton = tool.items.getAt(3);
        
        alphaButton.disable();
        origButton.enable();
        
    },
    
    onSortOriginalPaths: function(){
        
        var store = this.getViewModel().getStore('endpathitems');        
        
        //Sort By order

        var sorter = Ext.create('Ext.util.Sorter',{
            sorterFn: function(record1, record2) {
                var ord1 = record1.data.order;
                var ord2 = record2.data.order;

                return ord1 > ord2 ? 1 : -1;
            },
//                    property: 'order',
            direction: 'ASC'
        });

        var sorters = [];
        sorters.push(sorter);

        store.setSorters(sorters);
        store.sort('sorterFn');
        
        var pathTree = this.lookupReference('endpathTree');
        var tool = pathTree.lookupReference('endPathHeaderTooolBar');
        
        var alphaButton = tool.items.getAt(2); 
        var origButton = tool.items.getAt(3);
        
        alphaButton.enable();
        origButton.disable();
    }
    
    ,onSmartPrescaleClick: function(spmodName) {
        
        var container = this.lookupReference("endCentralContainer");
        var model = this.getViewModel(); //.getStore('parameters');
        model.set("trf",true);
        model.set("spname",spmodName);
        
    }
    
    ,onNotSmartPrescaleClick: function(){
        
        var container = this.lookupReference("endCentralContainer");
        var model = this.getViewModel(); //.getStore('parameters');
        model.set("trf",false);
        
//        this.lookupReference("endCentralContainer").this.lookupReference("endSpGrid").hide();
        var spgrid  = this.lookupReference("endSpGrid");
        spgrid.hide(); 
        
    }
    
    ,onEndparametersLoad: function(store, records, successful, operation, node, eOpts) {
        
        var model = this.getViewModel();
        var trf = model.get("trf");
        var triCond = false;

        if(this.lookupReference('paramGrid').isMasked()){
            this.lookupReference('paramGrid').setLoading( false );
        }
        
        var spgrid  = this.lookupReference("endSpGrid");
        
//        if (trf){
            
            try{
            
//              this.lookupReference("endCentralContainer").this.lookupReference("endSpGrid").show();
                var found = false, i = 0, records_len = records.length, sp_store, counter = 1;

    //            console.log(records_len);

                while(!found && i<records_len){

    //                console.log(i);
    //                console.log(found);

                    var rec = records[i];//.getAt(i);

    //                console.log(rec);

                    if (rec.get("name") == "triggerConditions") {
    //                    console.log("found");    
                        found = true;
                        triCond = true;
                    }else {
                        i++;
                    }
                }

                if (found){

                    var sp_store = this.lookupReference("endSpGrid").getViewModel().getStore('endspexpressions');

    //                sp_store = model.getStore('endspexpressions');

                    sp_store.removeAll(); 

                    var trf_expression  = records[i].get("rendervalue");

    //                trf_expression = trf_expression.replace(/{/gi, "");
    //                trf_expression = trf_expression.replace(/}/gi, "");
    //                trf_expression = trf_expression.replace(/\s/gm, '');
    //                trf_expression = trf_expression.replace(/["]+/g,"");

                    var expressions = trf_expression.split(',');
                    var prescale = 1, e, parts, pre_str, part_one, terms, ter;

                    for (e in expressions){

                        prescale = 1;

                        parts = expressions[e].split('/');

                            if (parts.length == 2){

                                pre_str = parts[1];
                                pre_str = pre_str.replace(/{/gi, "");
                                pre_str = pre_str.replace(/}/gi, "");
                                pre_str = pre_str.replace(/\s/gm, '');
                                pre_str = pre_str.replace(/["]+/g,"");

                                prescale = parseInt(pre_str, 10);
                            }

                            part_one = parts[0]; 

                            part_one = part_one.replace(/\(/g,"");
                            part_one = part_one.replace(/\)/g,"");

                            part_one = part_one.replace(/"/g,"");  

                            terms = part_one.split(' OR ');

                            for (ter in terms) {
                                var sp_item = {};
                                term = terms[ter];
                                term = term.replace(/{/gi, "");
                                term = term.replace(/}/gi, "");
                                term = term.replace(/\s/gm, '');
                                term = term.replace(/["]+/g,"");

                                sp_item['gid'] = counter;
    //                            sp_item['path'] = terms[ter];
                                sp_item['path'] = term;
                                sp_item['smprescale'] = prescale;
                                counter++;
                                sp_store.add(sp_item);

                            }
                    }                          
                }
                if (triCond){
                    
                    spgrid.show();
                    var label = spgrid.lookupReference('epsmatches');
                    label.setValue(sp_store.getCount());
                    
                }

    //            spgrid.collapse(); 

                
            } catch (e) {
                console.log(e);
            }   
            
//        }
        
        var id = operation.config.node.get('gid');
        if (id == -1){
           operation.config.node.expand(); 
        }
        
    }
    

    
});
