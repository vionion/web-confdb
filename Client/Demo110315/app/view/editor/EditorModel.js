Ext.define('Demo110315.view.editor.EditorModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.editor-editor',
    
    requires: ['Demo110315.model.Confdetails'],
    
    data: {
        name: 'Demo110315',
        idCnf: -1,
        idVer: -1,
        
        cnfname: ""
    },
    stores:
    {        
        cnfdetails:{
            
            model:'Demo110315.model.Confdetails',
            autoLoad: false,
            listeners:{
                load: 'onCnfDetailsLoad',
                scope: 'controller'
            }
        }
    }
    

});
