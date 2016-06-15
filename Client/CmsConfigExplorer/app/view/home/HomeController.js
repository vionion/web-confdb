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

    ,onEnterKey: function(field, e){

    if (e.getKey() == e.ENTER) {

                    var path = field.getSubmitValue();

                    var cnf_path = "#config=" + path

                    this.getViewModel().getStore('confnames').load({params: {name: cnf_path} });
                }
    }

    ,onConfnamesLoaded: function(store ,records, success, operation) {
        if (success == true){

            var cnf_id = records[0].get("url");
            store.removeAll();

            this.getView().fireEvent("pathEntered", cnf_id);

        }
        else {
            Ext.Msg.alert('Error', 'The Path is not correct, please try again.');
        }
    }

});
