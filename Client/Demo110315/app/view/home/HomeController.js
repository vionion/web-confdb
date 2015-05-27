Ext.define('Demo110315.view.home.HomeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.home-home',
    
    onExploreBatabaseClick: function(){
            
            console.log("In Home controller");
            var view = this.getView();
            view.fireEvent('exploreDatabase');
    }
    
});
