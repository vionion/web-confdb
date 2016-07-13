/**
 * The main application class. An instance of this class is created by app.js when it calls
 * Ext.application(). This is the ideal place to handle application launch and initialization
 * details.
 */
Ext.define('CmsConfigExplorer.Application', {
    extend: 'Ext.app.Application',
    
    name: 'CmsConfigExplorer',

    stores: [
        // TODO: add global / shared stores here
    ],
    
    requires:['CmsConfigExplorer.view.main.Main',
             'Ext.Ajax',
             'CmsConfigExplorer.model.Confname',
             'Ext.data.Store',
             'Ext.JSON'],
    
    // create a reference in Ext.application so we can access it from multiple functions
//    splashscreen: {},
    
//    autoCreateViewport: 'CmsConfigExplorer.view.main.Main'
    
//    ,defaultToken : 'home'
    
//    enableQuickTips: true,
//    init: function() {
//        var me = this;
//        
//        // Start the mask on the body and get a reference to the mask
//        me.splashscreen = Ext.getBody().mask('Loading application', 'splashscreen');
//
//        // Add a new class to this mask as we want it to look different from the default.
//        me.splashscreen.addCls('splashscreen');
//
//        // Insert a new div before the loading icon where we can place our logo.
//        Ext.DomHelper.insertFirst(Ext.query('.x-mask-msg')[0], {
//            cls: 'x-splash-icon'
//        });
//        
//        Ext.tip.QuickTipManager.init();
//        
//        Ext.Ajax.setTimeout(60000);
//    },
    
    listen : {
        controller : {
            '#' : {
                unmatchedroute : 'onUnmatchedRoute'
            }
        }
    },

    onUnmatchedRoute : function(hash) {
//        console.log(hash);
//        console.log(action);
        
        var splittedHash = hash.split("=");
        
        if (splittedHash[0] == "config"){
            
            var me = this;
            var redirect = "";
            
            Ext.Ajax.request({
                url     : 'confname',
                method: 'GET',
                headers: {'Content-Type': "application/json" },
                async: false,
                params: {
                    name: hash
                },
                success: function(response){
                    var text = response.responseText;
                    var results = Ext.JSON.decode(text);
                    
                    if(results.success){
//                        console.log("URL CORRECT");
                        var url = 'menu/' + results.children[0].url;
                        redirect = url;
//                        console.log("HERE");
//                        console.log(redirect);
//                        me.redirectTo(url);
                    }
                    else{
//                        console.log("HERE ELSE");
                        Ext.Msg.alert('Error 9', 'The URL is not correct, please try again.');
                        
                    }
     
                },
                failure : function(response) {
//                    var text = response.responseText;
//                    console.log(text);
//                    console.log("HERE FAILURE");
                    Ext.Msg.alert('Error 7', 'The URL is not correct, please try again.');
//                    this.redirectTo('menu/2000427_True', true);
                }
            });
            
//            console.log("REDIRECT BEFORE IF");
//            console.log(redirect);
            
            if (redirect == ""){
//                console.log("HERE IF REDIRECT");
                Ext.Msg.alert('Error 5', 'The URL is not correct, please try again.');
            }
            else {
                this.redirectTo(redirect);
            }

        }
        // get version ID
        
        // if doesnt exist display error
        
        //else return the page
    },
    
    
    launch: function () {
//        // TODO - Launch the application
//        
//        var me = this;
//        Ext.Ajax.setTimeout(60000);
//        
//        var task = new Ext.util.DelayedTask(function() {
//
////            Ext.getBody().unmask();
//            // fade out the body mask
//            me.splashscreen.fadeOut({
//                duration: 1000
////                remove: true
//            });
// 
//            // fade out the message
//            me.splashscreen.next().fadeOut({
//                duration: 1000,
////                remove: true, 
//                listeners:{
//                    afteranimate: function(el, startTime, eOpts){
//                        Ext.getBody().unmask();
//                        Ext.tip.QuickTipManager.init();
                        Ext.create('CmsConfigExplorer.view.main.Main');
//                    }
//                }
//            });
// 
//       });
// 
//       task.delay(1500);
    }
});
