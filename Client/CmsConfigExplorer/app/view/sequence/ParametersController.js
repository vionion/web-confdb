Ext.define('CmsConfigExplorer.view.sequence.ParametersController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.sequence-parameters'
    
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
