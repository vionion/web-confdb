Ext.define('Demo110315.view.service.ServicePrescaleTabController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.service-serviceprescaletab'
    
    ,onPreGridRender: function(preGrid){

        preGrid.setConfig({ enableLocking:true}) ;
    }
    
});
