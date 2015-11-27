Ext.define('CmsConfigExplorer.view.importconf.ImportController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.importconf-import',
    
    onHomeClick: function(){
            //console.log("In Explorer controller");
            var view = this.getView();
            view.fireEvent('backHome');
    },
    
    onUploadedConfiguration: function(newId){
        
        var view = this.getView();
        view.fireEvent('cusOpenImportedFile', newId);
    }
    
});
