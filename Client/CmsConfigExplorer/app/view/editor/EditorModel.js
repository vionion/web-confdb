Ext.define('CmsConfigExplorer.view.editor.EditorModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.editor-editor',
    
    requires: ['CmsConfigExplorer.model.Confdetails',
              'CmsConfigExplorer.model.Export'],
    
    data: {
        name: 'CmsConfigExplorer',
        idCnf: -1,
        idVer: -1,
        online: "False",
        appversion: 'v1.2.2',
        cnfname: "",
        link: "",
        expLink: '/download/?filepath=/Users/vdaponte/Dropbox/dossier sans titre/DomainConceptsDescriptons.pdf'
    },
    stores:
    {        
        cnfdetails:{
            
            model:'CmsConfigExplorer.model.Confdetails',
            autoLoad: false,
            listeners:{
                load: 'onCnfDetailsLoad',
                scope: 'controller'
            }
        },
        
        exported:{
            
            model:'CmsConfigExplorer.model.Export',
            autoLoad: false,
            listeners:{
                load: 'onExportedsLoad',
                scope: 'controller'
            }
        }
    }
    

});
