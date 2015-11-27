Ext.define('CmsConfigExplorer.view.path.ModuleDetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.path-moduledetails',
    
    onModDetailsLoad: function(store, records, successful, operation, node, eOpts){
//        var form = this.lookupReference('modDetails');
//        var form_vm = form.getViewModel();
        
        var first = records[0];
        
//        form_vm.set( "name", first.get('name') );
//        form_vm.set( "author", first.get('author') );
//        form_vm.set( "class", first.get('mclass') );
//        form_vm.set( "type", first.get('mt') );
        
        var name = this.lookupReference('modDetailsName');
        var author = this.lookupReference('modDetailsAuthor');
        var mclass = this.lookupReference('modDetailsClass');
        var mtype = this.lookupReference('modDetailsType');
        
        name.setValue( first.get('name') );
        author.setValue( first.get('author') );
        mclass.setValue( first.get('mclass') );
        mtype.setValue( first.get('mt')  );
    },
    
    onDetLoaded: function(mid,pid,online,idv){
        this.getViewModel().getStore('moddetails').load({params: {mid: mid, pid: pid, online:online, verid:idv}});
    }
    
});
