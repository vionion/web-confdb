Ext.define('Demo110315.view.essource.ESSourceGridController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.essource-essourcegrid',
    
        onGridESSourceClick: function( v, record, tr, rowIndex, e, eOpts) {
    
        var mid = record.get("gid");
        var view = this.getView();
        view.fireEvent('custGridESSourceParams',mid);
    }
    
});
