Ext.define('CmsConfigExplorer.view.globalpset.GlobalPsetParamsTreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.globalpset-globalpsetparamstree',
        
    onTooltipActivate: function ( grid ){    
        
        var view = grid.getView();
        var tip = Ext.create('Ext.tip.ToolTip', {
            // The overall target element.
            target: view.el,
            // Each grid row causes its own separate show and hide.
            delegate: view.itemSelector,
            // Moving within the row should not hide the tip.
            trackMouse: true,
            // Render immediately so that tip.body can be referenced prior to the first show.
    
            listeners: {
                // Change content dynamically depending on which element triggered the show.
                beforeshow: function updateTipBody(tip) {
                    tip.update(view.getRecord(tip.triggerElement).get('rendervalue'));
                }
            }
           
           });

    }
    
    ,onBeforeCellEdit: function( editor, context, eOpts ){
        
        var col = context.column;
        var value = context.value;
        var editor_area = new Ext.grid.plugin.CellEditing( {
            xtype: 'textarea',
            editable : false,
            grow: true,
            growMin : 0
        } ); 
        
        var editor_field = new Ext.grid.plugin.CellEditing( {
            xtype: 'textfield',
            editable : false
        } ); 
        
        if (value.length > 70){

            col.setEditor( editor_area );
        } else {
            
            col.setEditor( editor_field );
        }       
        return true;
    }
});
