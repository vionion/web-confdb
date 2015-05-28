/**
 * The main application class. An instance of this class is created by app.js when it calls
 * Ext.application(). This is the ideal place to handle application launch and initialization
 * details.
 */
Ext.define('Demo110315.Application', {
    extend: 'Ext.app.Application',
    
    name: 'Demo110315',

    requires:['Demo110315.view.editor.Editor',
              'Demo110315.view.edsource.EDSource',
              'Demo110315.view.endpath.EndPath',
              'Demo110315.view.esmodule.ESModule',
              'Demo110315.view.essource.ESSource',
              'Demo110315.view.explorer.Explorer',
              'Demo110315.view.globalpset.GlobalPset',
              'Demo110315.view.home.Home',
              'Demo110315.view.main.Main',
              'Demo110315.view.module.Module',
              'Demo110315.view.path.Path',
              'Demo110315.view.sequence.Sequence',
              'Demo110315.view.service.Service',
              'Demo110315.view.streamdataset.StreamDataset',
                'Ext.util.DelayedTask'],
    
    stores: [
        // TODO: add global / shared stores here
    ],
    
    views:['Demo110315.view.editor.Editor',
          'Demo110315.view.edsource.EDSource',
          'Demo110315.view.endpath.EndPath',
          'Demo110315.view.esmodule.ESModule',
          'Demo110315.view.essource.ESSource',
          'Demo110315.view.explorer.Explorer',
          'Demo110315.view.globalpset.GlobalPset',
          'Demo110315.view.home.Home',
          'Demo110315.view.main.Main',
          'Demo110315.view.module.Module',
          'Demo110315.view.path.Path',
          'Demo110315.view.sequence.Sequence',
          'Demo110315.view.service.Service',
          'Demo110315.view.streamdataset.StreamDataset'],
    
        models: ['Demo110315.model.Base',
            'Demo110315.model.Confdetails',
            'Demo110315.model.Datasetitem',
            'Demo110315.model.EDSource',
            'Demo110315.model.EDSourceitem',
            'Demo110315.model.Endpathitem',
            'Demo110315.model.ESModule',
            'Demo110315.model.ESModuledetails',
            'Demo110315.model.ESModuleitem',
            'Demo110315.model.ESSource',
            'Demo110315.model.ESSourceitem',
            'Demo110315.model.Evcoitem',
            'Demo110315.model.Folderitem',
            'Demo110315.model.GlobalPset',
            'Demo110315.model.GlobalPsetItem',
            'Demo110315.model.Module',
            'Demo110315.model.Moduledetails',
            'Demo110315.model.Moduleitem',
            'Demo110315.model.OUTModuledetails',
            'Demo110315.model.Pathdetails',
            'Demo110315.model.Pathitem',
            'Demo110315.model.Sequenceitem',
            'Demo110315.model.Service',
            'Demo110315.model.Serviceitem',
            'Demo110315.model.Streamitem',
            'Demo110315.model.Version'],
    
    // create a reference in Ext.application so we can access it from multiple functions
    splashscreen: {},
    
    init: function() {
        var me = this;

        // Start the mask on the body and get a reference to the mask
        me.splashscreen = Ext.getBody().mask('Loading application', 'splashscreen');

        // Add a new class to this mask as we want it to look different from the default.
        me.splashscreen.addCls('splashscreen');

        // Insert a new div before the loading icon where we can place our logo.
        Ext.DomHelper.insertFirst(Ext.query('.x-mask-msg')[0], {
            cls: 'x-splash-icon'
        });
    },
    
    launch: function() {
        // TODO - Launch the application
        Ext.tip.QuickTipManager.init();
        
        var me = this;
        
        var task = new Ext.util.DelayedTask(function() {

//            Ext.getBody().unmask();
            // fade out the body mask
            me.splashscreen.fadeOut({
                duration: 1000
//                remove: true
            });
 
            // fade out the message
            me.splashscreen.next().fadeOut({
                duration: 1000,
//                remove: true, 
                listeners:{
                    afteranimate: function(el, startTime, eOpts){
                        Ext.getBody().unmask();
                        Ext.create('Demo110315.view.main.Main');
                    }
                }
            });
 
       });
 
       task.delay(2000);
        
//        Ext.create('Demo110315.view.main.Main');
    }

    
    
});
