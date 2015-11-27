Ext.define('CmsConfigExplorer.view.sequence.ModuleDetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.sequence-moduledetails',
    
    onSeqModDetailsLoad: function(store, records, successful, operation, node, eOpts){
//        var form = this.lookupReference('modDetails');
//        var form_vm = form.getViewModel();
        
        var first = records[0];
        
//        form_vm.set( "name", first.get('name') );
//        form_vm.set( "author", first.get('author') );
//        form_vm.set( "class", first.get('mclass') );
//        form_vm.set( "type", first.get('mt') );
        
        var name = this.lookupReference('seqModDetailsName');
        var author = this.lookupReference('seqModDetailsAuthor');
        var mclass = this.lookupReference('seqModDetailsClass');
        var mtype = this.lookupReference('seqModDetailsType');
        
        name.setValue( first.get('name') );
        author.setValue( first.get('author') );
        mclass.setValue( first.get('mclass') );
        mtype.setValue( first.get('mt')  );
    },
    
    onSeqModDetLoaded: function(mid,pid){
        this.getViewModel().getStore('seqmoddetails').load({params: {mid: mid, pid: pid}});
    }
    
});
