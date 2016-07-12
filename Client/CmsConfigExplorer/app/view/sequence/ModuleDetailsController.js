Ext.define('CmsConfigExplorer.view.sequence.ModuleDetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.sequence-moduledetails',
    
    onSeqModDetailsLoad: function(store, records, successful, operation, node, eOpts){
        
        var first = records[0];
        
        var name = this.lookupReference('seqModDetailsName');
        var author = this.lookupReference('seqModDetailsAuthor');
        var mclass = this.lookupReference('seqModDetailsClass');
        var mtype = this.lookupReference('seqModDetailsType');
        
        name.setValue( first.get('name') );
        author.setValue( first.get('author') );
        mclass.setValue( first.get('mclass') );
        mtype.setValue( first.get('mt')  );
    },
    
    onSeqModDetLoaded: function( mid, pid, online,idv, idc){
        this.getViewModel().getStore('seqmoddetails').load({params: {mid: mid, pid: pid, online:online,verid:idv}});
    }
    
});
