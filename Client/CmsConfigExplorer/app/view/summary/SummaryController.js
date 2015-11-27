Ext.define('CmsConfigExplorer.view.summary.SummaryController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.summary-summary',
    
    requires:['Ext.util.Collection', 
              'CmsConfigExplorer.model.Summaryitem', 
              'CmsConfigExplorer.model.Summarycolumn'],
    
    onSummaryRender: function(){
        
        var view = this.getView();
        
        vm = this.getViewModel();
        var grid = this.lookupReference('firstgrid'); 
        
        cid = this.getViewModel().get("idCnf");
        vid = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        var columnsStore = vm.getStore('summarycolumns');
        var itemsStore = vm.getStore('summaryitems');
        
        columnsStore.load({params: {cnf: cid, ver: vid, online:online}});
        
        itemsStore.load({params: {cnf: cid, ver: vid, online:online}});
 
    }    
    
    ,onSummarycolumnsLoad: function( store, records, successful, eOpts ){
        
        var view = this.getView();
        vm = this.getViewModel();
        
        view.setLoading('Loading data');
        var count = store.count().valueOf();
        
        var grid = this.lookupReference('firstgrid'); 
        
        var mycolumns = [];
        var treecolumn = { 
                            xtype: 'treecolumn', 
                            header: 'Name', 
                            dataIndex: 'name', 
                            minWidth: 350,
                            width: 350,
//                            flex: 4,
                            sortable: false,
                            locked: true
            };
        var seedscolumn = { 
                            xtype: 'gridcolumn', 
                            header: 'Level_1_Seeds_Expression', 
                            dataIndex: 'Level_1_Seeds_Expression', 
                            minWidth: 200,
                            width: 270,
//                            flex: 2,
                            sortable: false,
                            align: 'right' 
            };
        mycolumns.push(treecolumn);
//        var group = { 
//                            text: 'Prescales',
//                            columns: []
//            };
        
        var smart_column = {
                            xtype: 'gridcolumn', 
                            header: 'Smart Prescale', 
                            dataIndex: 'smart_pre', 
                            minWidth: 120,
                            width: 130,
//                            flex: 2,
                            sortable: false,
                            align: 'right',
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
        
        mycolumns.push(smart_column);
        
        var group = { 
                            text: 'Prescales',
                            isGroupHeader : true,
                            sealed : true,
                            columns: []
            };
        
        for (i = 0; i < count; i++){
            var newColumn = { 
                            xtype: 'gridcolumn', 
                            text: '',  
                            dataIndex: '', 
                            width: 100, 
                            minWidth: 100,
//                            flex: 1,
                            sortable: false,
                            sealed : true,
                            render: '',
                            align: 'right',
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
            newColumn.text = store.getAt(i).get('name');
            newColumn.dataIndex = store.getAt(i).get('name');
//            newColumn.render = function(v, meta, rec){
//                        
//                        var value = parseInt(v);
//                
//                        if (value == 1) {
//                            return '<span style="color:green;">' + v + '</span>';
//                        } else if (value == 0) {
//                            return '<span style="color:red;">' + v + '</span>';
//                        }
//                        return '<span style="color:#FFFF00;">' + v + '</span>';
//                };
            group.columns.push(newColumn);
        }
        mycolumns.push(group);
        mycolumns.push(seedscolumn);
        
        vm.set('columns',mycolumns);
    }
    
    ,onSummaryitemsLoad: function( store, records, successful, eOpts ){
        
        var view = this.getView();
        vm = this.getViewModel();

        var biggrid = Ext.create('Ext.tree.Panel',{
            
            requires: [
                'Ext.grid.selection.SpreadsheetModel',
                'Ext.grid.plugin.Clipboard'
            ],
            
            region: 'center',
            reference: 'biggrid',
            header: false,
            useArrows: true,
            border: true,
            columnLines: true,
            enableLocking: true,
            trackOver: false,
            enableColumnMove : false,
            
            store: {},
            
//            plugins: 'clipboard',
            plugins: [
                {
                    ptype: 'clipboard'
                }
            ],

            listeners: {
                selectionchange: 'onSelectionChange'
            },
            selModel: {
                type: 'spreadsheet',
                // Disables sorting by header click, though it will be still available via menu
                columnSelect: true,            
//                checkboxSelect: true,
//                checkboxColumnIndex: 'last', 
                pruneRemoved: false
            },
            tbar: [
                {
                    xtype: 'tbtext',
                    text: '<b>Summary View</b>'
                },
                    '-',
                {
                    xtype: 'component',
                    html: 'Selectable: '
                }, 
//                {
//                    text: 'Rows',
//                    enableToggle: true,
//                    toggleHandler: 'toggleRowSelect',
//                    pressed: true
//                }, 
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
                '-',
                {
                    labelWidth: 80,
                    xtype: 'textfield',
                    fieldLabel: 'Ssearch ',
                    reference: 'trigfield',                    
    //                triggerWrapCls: 'x-form-clear-trigger',
                    triggers:{
                        search: {
                            reference: 'triggerSearch',
                            cls: 'x-form-clear-trigger',
                            handler: 'onTriggerClick',
                            listeners: {
                                change: 'onSearchChange'

                            }
                        }
                    }, 
                    listeners: {
                        change: 'onSearchChange'

                    }
                },
                ,{
                    xtype: 'displayfield',
                    reference: 'matches',
                    fieldLabel: 'Matches',

                    // Use shrinkwrap width for the label
                    labelWidth: null
//                    listeners: {
//                        beforerender: function() {
//                            var me = this,
//                                tree = me.up('treepanel'),
//                                root = tree.getRootNode(),
//                                leafCount = 0;
//
//                            tree.store.on('fillcomplete', function(store, node) {
//                                if (node === root) {
//                                    root.visitPostOrder('', function(node) {
//                                        if (node.isLeaf()) {
//                                            leafCount++;
//                                        }
//                                    });
//                                    me.setValue(leafCount);
//                                }
//                            });
//                        },
//                        single: true
//                    }
                },
                '->', 
                {
                    xtype: 'component',
                    reference: 'status'
                }
            ],
            columns: [
                    { 
                        xtype: 'treecolumn', 
                        header: 'Name', 
                        dataIndex: 'name', 
                        width: 350, 
//                        flex: 4,
                        sortable: false 
                    }
            ]
            ,viewConfig: {
                columnLines: true,
                trackOver: false
            }
            
            
        });
  
        var columns = vm.get('columns'); 
        
        store.getRoot().cascadeBy( function(record) {
                        if(record.get('icon') == 'resources/Path_3.ico'){
                            var values = record.get('values');
                            var count = values.length;
                            for (index = 0; index < count; index++){
                                var val = values[index];
                                var val_res = val.split("###");
//                                record.data[val.label] = val.value;
                                record.data[val_res[0]] = val_res[1];
                            } 
                        }
 
                    },this);
        
        
        store.getRoot().expand();
        
        biggrid.reconfigure(store,columns);
        Ext.resumeLayouts(true);
        
        view.insert(1,biggrid);        
        view.setLoading(false);
        
    }
    
    ,getSelectionModel: function () {
        var grid = this.getView().lookupReference('biggrid');
        return grid.getSelectionModel();
    },
    
    onSelectionChange: function (grid, selection) {
        var status = this.lookupReference('status'),
            message = '??',
            firstRowIndex,
            firstColumnIndex,
            lastRowIndex,
            lastColumnIndex;

        if (!selection) {
            message = 'No selection';
        }
        else if (selection.isCells) {
            firstRowIndex = selection.getFirstRowIndex();
            firstColumnIndex = selection.getFirstColumnIndex();
            lastRowIndex = selection.getLastRowIndex();
            lastColumnIndex = selection.getLastColumnIndex();

            message = 'Selected cells: ' + (lastColumnIndex - firstColumnIndex + 1) + 'x' + (lastRowIndex - firstRowIndex + 1) +
                ' at (' + firstColumnIndex + ',' + firstRowIndex + ')';
        }
        else if (selection.isRows) {
            message = 'Selected rows: ' + selection.getCount();
        }
        else if (selection.isColumns) {
            message = 'Selected columns: ' + selection.getCount();
        }

        status.update(message);
    },

//    toggleRowSelect: function(button, pressed) {
//        var sel = this.getSelectionModel();
//        sel.setRowSelect(pressed);
//    },

    toggleCellSelect: function(button, pressed) {
        var sel = this.getSelectionModel();
        sel.setCellSelect(pressed);
    },

    toggleColumnSelect: function(button, pressed) {
        var sel = this.getSelectionModel();
        sel.setColumnSelect(pressed);
    },
    
    onTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('trigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
//        tf.focus();
        
    },
    
    onSearchChange: function( form, newValue, oldValue, eOpts ) {
        
//        var tree = this.getView().lookupReference('biggrid');
//        tree.filter(newValue);
//
        var tree = this.getView(),
            store = this.getViewModel().getStore("summaryitems"),
            v = null,
            matches = 0;
        
        this.getViewModel().getStore("summaryitems").clearFilter();
//        tree.store.clearFilter();
        
        try{
            v = new RegExp(form.getValue(), 'i');
            Ext.suspendLayouts();
            store.filter({
                filterFn: function(node) {
                    if (!node.isRoot()){
                    
                        var children = node.childNodes,
                            len = children && children.length,
    //                        visible = node.isLeaf() ? v.test(node.get('name')) : false,
                            visible = (v.test(node.get('name'))),
                            i;
//                        

                        for (i = 0; i < len && !(visible = children[i].get('visible')); i++);

    //                    if (visible && node.isLeaf()) {
                        if (visible) {
                            matches++;
                        }
                        
                        if (node.parentNode){
                            visible = (visible || v.test(node.parentNode.get('name'))); 
                        }
                        
                        if (node.parentNode.parentNode){ // NOT SO NICE
                            visible = (visible || v.test(node.parentNode.parentNode.get('name'))); // NOT SO NICE
                        }
                        
                        return visible;
                    }
                }    
//                id: 'titleFilter'
            });
            this.lookupReference("matches").setValue(matches);
//            tree.down('#matches').setValue(matches);
            Ext.resumeLayouts(true);
            
                
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
    
});
