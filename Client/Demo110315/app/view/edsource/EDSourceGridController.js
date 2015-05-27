Ext.define('Demo110315.view.edsource.EDSourceGridController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.edsource-edsourcegrid',
    
    onGridEDSourceClick: function( v, record, tr, rowIndex, e, eOpts) {
    
        var mid = record.get("gid");
        var view = this.getView();
        view.fireEvent('custGridEDSourceParams',mid);
    }
    
});
