Ext.define('CmsConfigExplorer.view.home.HomeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.home-home',
    
    onExploreDatabaseClick: function(){
            
            //console.log("In Home controller");
            var view = this.getView();
            view.fireEvent('exploreDatabase');
    }
    ,onImportPythonClick: function(){
            
            //console.log("In Home controller");
            var view = this.getView();
            view.fireEvent('importPython');
    }
});
