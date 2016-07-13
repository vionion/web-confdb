Ext.define('CmsConfigExplorer.view.service.ServicePrescaleTabController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.service-serviceprescaletab'
    
    ,onPreGridRender: function(preGrid){

        preGrid.setConfig({ enableLocking:true}) ;
    }
    
    ,onPathPrescaleTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('pretrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onPathPrescaleSearchChange: function( form, newValue, oldValue, eOpts ) {
        var tree = this.lookupReference("prescaleGrid"),
//        var tree = this.getView(),
            v = null,
            matches = 0;

        tree.store.clearFilter();

        try {
            v = new RegExp(form.getValue(), 'i');
            Ext.suspendLayouts();
            tree.store.filter({
                filterFn: function(record) {
                    
                    var visible = true;
                    
                    visible = v.test(record.get('pathname'));
                    
                    if(visible) {
                            matches++;
                    }
                    
// 
//                    if (node.get('pit') == "pat"){
//                        
//                        visible = v.test(node.get('Name'));
//                        
//                        if(visible) {
//                            matches++;
//                        }
//                        
//                    }
//                    else if (node.isRoot()){
//                        
//                        visible = true;
//                    }
//                    else {
//  
//                        var found = false;
//                        var parent = node;
//                        
//                        while(!found){
//                            parent = parent.parentNode;
//                            if (parent.get('pit') == 'pat'){
//                                found = true;
//                            }
//                        }
//  
//                        visible = v.test(parent.get('Name'));
//                        
//                    }
                    
                    return visible;
                }

            });
            var mat = this.lookupReference('preMatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
    ,getSelectionModel: function () {
        var grid = this.getView().lookupReference('prescaleGrid');
        return grid.getSelectionModel();
    }
    
    ,onSelectionChange: function (grid, selection) {
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
    
    toggleCellSelect: function(button, pressed) {
        var sel = this.getSelectionModel();
        sel.setCellSelect(pressed);
    },

    toggleColumnSelect: function(button, pressed) {
        var sel = this.getSelectionModel();
        sel.setColumnSelect(pressed);
    }
//    
//    ,onPrescaleShow: function(view){
//        if (this.lookupReference("prescaleGrid")){
//            
//            console.log("HERE");
//            this.lookupReference("prescaleGrid").getColumns()[0].setWidth(300);
//            this.lookupReference("prescaleGrid").getColumns()[0].autoSize();
//            view.updateLayout();
//            Ext.resumeLayouts(true);
//            
//        } 
//    }        
    
    
});
